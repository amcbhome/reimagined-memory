import streamlit as st
import pandas as pd
import re

# Load structured IFRS data
@st.cache_data
def load_data():
    return pd.read_csv("ifrs_smes_structured.csv")

df = load_data()

# App Title
st.title("📚 IFRS for SMEs Search (2025 Edition)")

# Search Bar
query = st.text_input("🔎 Enter your search term:")

# Options
case_sensitive = st.checkbox("Case Sensitive", value=False)
max_results = st.slider("Max Results to Display", min_value=1, max_value=50, value=10)

def keyword_search(query, df, case_sensitive=False):
    if not case_sensitive:
        query = query.lower()
        mask = df['Content'].str.lower().str.contains(query)
    else:
        mask = df['Content'].str.contains(query)
    return df[mask]

def highlight_text(text, query):
    pattern = re.compile(f"({re.escape(query)})", re.IGNORECASE)
    return pattern.sub(r"**\1**", text)

# Perform Search
if query:
    results = keyword_search(query, df, case_sensitive)
    st.write(f"### 📝 Found {len(results)} results:")
    
    for idx, row in results.head(max_results).iterrows():
        highlighted = highlight_text(row['Content'], query)
        st.markdown(f"#### 📌 {row['Section']}")
        st.markdown(highlighted[:2000] + "..." if len(highlighted) > 2000 else highlighted)
        st.markdown("---")
else:
    st.info("Enter a search term to begin.")

