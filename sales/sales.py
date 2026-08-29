import pandas as pd
from sqlalchemy import create_engine, text, String, Date
import os
from dotenv import load_dotenv


load_dotenv()


HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(connection_string)
query = "SELECT * FROM sales.superstoreorders;"  

def extract_data(engine, query):
    try:
        with engine.connect() as connection:
            df = pd.read_sql(query, con=connection)
            print(df.head())
            return df
    except Exception as e:
        print(f"An error occurred: {e}")
        raise       

def transform(df):
    df = df.drop_duplicates()  
    df = df.dropna(subset=['order_id', 'ship_date', 'order_date'])
    
    dupe_check = df.duplicated(subset=['order_id', 'product_id'], keep=False)
    if dupe_check.any():
        print(f"WARNING: {dupe_check.sum()} rows share a duplicate (order_id, product_id) pair.")
        print(df[dupe_check][['order_id', 'product_id', 'quantity']])
    
    df = df.drop_duplicates(subset=['order_id', 'product_id'])  

    df = df.reset_index(drop=True)
    df.insert(0, 'row_id', df.index + 1)
    df = df.drop_duplicates(subset=['order_id', 'product_id'])
    df = df.dropna(subset=['order_id', 'ship_date', 'order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'], format='mixed' , dayfirst=False, errors='coerce')
    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed' , dayfirst=False, errors='coerce')
    return df

def write_to_staging(df, engine):
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'])
    print("ship_date missing after conversion:", df['ship_date'].isna().sum())
    print("order_date missing after conversion:", df['order_date'].isna().sum())
    print(df)
    df.to_sql('superstore_cleaned_staging', con=engine, if_exists='replace', index=False,
        dtype={
            'order_id': String(50),
            'order_date': Date(),
            'ship_date': Date(),
        }
    )
    print(f"Staging table written: {len(df)} rows.")
 
 
def load_to_final_table(engine):
    insert_query = """
    INSERT INTO superstore_cleaned (
        order_id, order_date, ship_date, ship_mode, customer_name,
        segment, state, country, market, region, product_id,
        category, sub_category, product_name, sales, quantity,
        discount, profit, shipping_cost, order_priority, year
    )
    SELECT
        order_id, order_date, ship_date, ship_mode, customer_name,
        segment, state, country, market, region, product_id,
        category, sub_category, product_name, sales, quantity,
        discount, profit, shipping_cost, order_priority, year
    FROM superstore_cleaned_staging
    """

    try:
        with engine.begin() as connection:
            print("Loading cleaned data into superstore_cleaned...")
            connection.execute(text("TRUNCATE TABLE superstore_cleaned;"))
            connection.execute(text(insert_query))

            result = connection.execute(text("SELECT COUNT(*) FROM superstore_cleaned;"))
            row_count = result.scalar()
            print(f"Load completed. Total rows in superstore_cleaned: {row_count}")

            dtype_check = connection.execute(text("""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'superstore_cleaned'
                AND COLUMN_NAME IN ('order_date', 'ship_date');
            """))
            for row in dtype_check:
                print(f"  {row[0]} -> {row[1]}")

            connection.execute(text("DROP TABLE IF EXISTS superstore_cleaned_staging;"))
            print("Staging table successfully dropped.")

    except Exception as e:
        print(f"ERROR: The merge failed. Here is the message from MySQL:\n{e}")
        print("Because it failed, the staging table was NOT dropped.")
def main(engine, query):
    df = extract_data(engine, query)
    df = transform(df)
    write_to_staging(df, engine)
    load_to_final_table(engine)
    print(df['ship_date'].dtypes)
    print(df['order_date'].dtypes)


if __name__ == "__main__":
    main(engine, query)  
