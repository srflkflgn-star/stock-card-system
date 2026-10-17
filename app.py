import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION (TITLE & LOGO) ---
st.set_page_config(
    page_title="AMG Steel Factory - Inventory Management",
    page_icon="🏭",
    layout="wide"
)

# --- HEADER WITH AMG LOGO ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        st.image("logo.png", width=140)
    except:
        st.write("🏭")

with col_title:
    st.title("🏭 AMG STEEL FACTORY")
    st.subheader("Inventory Control & Multi-Item Stock Card Management System")

# --- GOOGLE SHEETS SETUP ---
SHEET_ID = "1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI"
ITEMS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=items"
TRANS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=transactions"

ETHIOPIAN_MONTHS = {
    1: "መስከረም (Meskerem)",
    2: "ጥቅምት (Tikimt)",
    3: "ኅዳር (Hidar)",
    4: "ታኅሣሥ (Tahsas)",
    5: "ጥር (Tir)",
    6: "የካቲት (Yekatit)",
    7: "መጋቢት (Megabit)",
    8: "ሚያዝያ (Miyazya)",
    9: "ግንቦት (Ginbot)",
    10: "ሰኔ (Sene)",
    11: "ሐምሌ (Hamle)",
    12: "ነሐሴ (Nehase)",
    13: "ጳጉሜ (Pagume)"
}

def clean_code(code):
    if pd.isna(code):
        return ""
    val = str(code).strip()
    if val.endswith(".0"):
        val = val[:-2]
    return val

@st.cache_data(ttl=2)
def load_items():
    try:

        "
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Report & Analysis</button>", height=50)
            with col2:
                csv_m = display_summary.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv_m, file_name=f"Monthly_Report_{selected_month}.csv", mime="text/csv", key="download_monthly_summary")
        
        
