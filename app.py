import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION (TITLE & LOGO) ---
st.set_page_config(
    page_title="AMG Steel Factory - Inventory Control",
    page_icon="logo.png",
    layout="wide"
)

# --- HIDE STREAMLIT BRANDING / WATERMARKS ---
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    .viewerBadge_container__1s5D3 {display: none !important;}
    .styles_viewerBadge__1y-oN {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- HEADER WITH AMG LOGO ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        st.image("logo.png", width=140)
    except:
        st.write("🏭")

with col_title:
    st.title("🏭 AMG STEEL FACTORY")
    አጠቃላይ ሁኔታን ያሳያል። ለኃላፊዎች እና ለቅርብ ክትትል እንዲመች ይህ ሪፖርት በጽሁፍና በሰንጠረዥ ተዘጋጅቷል።
            """
            
            st.info(analysis_text)

            col1, col2 = st.columns(2)
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Report & Analysis</button>", height=50)
            with col2:
                csv_m = display_summary.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv_m, file_name=f"Monthly_Report_{selected_month}.csv", mime="text/csv", key="download_monthly_summary")
