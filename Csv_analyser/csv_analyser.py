import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Analyser", layout="wide")
st.title("CSV Analyser")
st.subheader("Upload any CSV get a description about that csv file in moments")
MAX_MB_SIZE = 200 



def columns(df):
    col1, col2, col3 = st.columns(3)
    with col1:
            st.write("Total Rows:",df.shape[0])
    with col2:
            st.write("Total Columns:",df.shape[1])
    with col3:
            st.write("Total null values:",df.isnull().sum().sum())
    
    st.divider()

def numerical_des(df):
    with st.expander("View Data Types & Nulls per Column"):
        summary_df = pd.DataFrame({
                     'Data Type': df.dtypes,
                     'Null Values': df.isnull().sum()
                 })
        st.dataframe(summary_df, use_container_width=True)
         
    st.subheader("Statistical Summary")
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        st.info("No numeric columns found to summarize.")
    else:
        summary_stats = df.describe().loc[['count', 'mean', 'min', 'max']]
        st.dataframe(summary_stats, use_container_width=True)

def plot_charts(df, styled_df):
    with st.expander("View nulls values in each column"):
     x = df.columns
     if x.empty:
        st.info("No numeric columns found to plot.")
    
     y = df.isnull().sum()
     fig, ax = plt.subplots(figsize=(10, 5))
     ax.bar(x, y)    
     ax.set_title("Data Types vs Null Values") 
     ax.set_xlabel("Data Types")
     ax.set_ylabel("Null Values")
     ax.tick_params(axis="x", labelrotation=45)
     plt.setp(ax.get_xticklabels(), ha="right")
     fig.tight_layout()
     st.pyplot(fig)

    with st.expander("View Distribution of Numeric Columns"):
     numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns

     for col in numeric_columns:
       st.write(f"Distribution of {col}")
       fig, ax = plt.subplots(figsize=(10, 5))
       ax.hist(df[col].dropna(), bins=30, edgecolor='black')
       ax.tick_params(axis="x", labelrotation=45)
       st.pyplot(fig)

    with st.expander("View Top 5 Categories in Text Columns"):
     text_columns = df.select_dtypes(include=['object']).columns

     for col in text_columns:
       st.write(f"Top 5 categories in {col}")
       st.bar_chart(df[col].value_counts().head(5))

def main():
    up_file=st.file_uploader("",type=["csv"])
    if up_file is not None:
        
        file_size_mb = up_file.size / (1024 * 1024)
    
        if file_size_mb > MAX_MB_SIZE:
           st.error(f"❌ File too large! Your file is {file_size_mb:.1f} MB, but this app only supports up to {MAX_MB_SIZE} MB.")
        else:
         try:
             df = pd.read_csv(up_file)
         except Exception as e:
             st.error(f"❌ Could not read this file as a CSV: {e}")
             return

         if df.empty:
             st.warning("⚠️ The uploaded CSV has no rows.")
             return

         styled_df = df.style.set_table_styles([
            {
                'selector': 'th',
                'props': [('font-size', '18px'), ('font-weight', 'bold')]
            }
         ])
         st.success("File uploaded successfully!")
         st.divider()
         columns(df)
         numerical_des(df)
         plot_charts(df,styled_df)

if __name__ == "__main__":
    main()