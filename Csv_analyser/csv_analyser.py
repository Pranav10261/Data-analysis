import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Analyser", layout="wide")
st.title("CSV Analyser")
st.subheader("Upload any CSV get a description about that csv file in moments")

up_file=st.file_uploader("",type=["csv"])

if up_file is not None:
    try: 
         df = pd.read_csv(up_file)
    
    except Exception as e:
        st.error(f"Couldn't read this file: {e}")
        st.stop()
    st.success("File uploaded successfully!")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Total Rows:",df.shape[0])
    with col2:
        st.write("Total Columns:",df.shape[1])
    with col3:
        st.write("Total null values:",df.isnull().sum().sum())

    st.divider()

    with st.expander("View Data Types & Nulls per Column"):
            # Create a quick summary dataframe for clean viewing
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