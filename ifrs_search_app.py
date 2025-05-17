import streamlit as st
import pandas as pd
import re
import os

# --- Load Data ---
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error("Data file not found. Please place 'ifrs_smes_full_text.csv' in the project directory.")
        return pd.DataFrame()

# Path to the CSV file
csv_file = "ifrs_smes_full_text.csv"
df = load_data(csv_file)

# --- App Layout ---
st.set_page_config(page_title="IFRS for SMEs Search", layout="wide")
st.title("📚 IFRS for SMEs Search App (2025 Edition)")

# --- Search Inputs ---
query = st.text_input("🔍 Enter your search term:")
case_sensitive = st.checkbox("Case Sensitive Search", value=False)
max_results = st.slider("Max Results to Display", min_value=1, max_value=100, value=10)

# --- Search Function ---
def keyword_search(query, dataframe, case_sensitive=False):
    if query.strip() == "":
        return pd.DataFrame()  # Empty search returns nothing
    return dataframe[dataframe['Content'].str.contains(
        query, case=case_sensitive, na=False, regex=True
    )]

def highlight_text(text, query):
    pattern = re.compile(f"({re.escape(query)})", re.IGNORECASE)
    return pattern.sub(r"**\1**", text)

# --- Perform Search ---
if query:
    results = keyword_search(query, df, case_sensitive)
    st.success(f"Found {len(results)} matching results.")

    for idx, row in results.head(max_results).iterrows():
        highlighted = highlight_text(row['Content'], query)
        st.markdown(f"#### 📖 Page {row['Page']}")
        st.markdown(highlighted[:2000] + "..." if len(highlighted) > 2000 else highlighted)
        st.markdown("---")
    
    # Option to Download Results
    if not results.empty:
        csv_download = results.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Search Results as CSV", csv_download, "search_results.csv", "text/csv")

else:
    st.info("Please enter a search term to begin.")

