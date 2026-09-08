import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="AMG Steel Factory - Inventory System", layout="wide")

st.title("🏭 AMG STEEL FACTORY")
st.subheader("Inventory Control & Multi-Item Stock Card Management System")

# --- GOOGLE SHEETS SETUP ---
SHEET_ID = "1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI"
ITEMS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=items"
TRANS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=transactions"

def load_items():
    try:
        df = pd.read_csv(ITEMS_URL)
        df = df.dropna(how="all")
        return df
    except Exception:
        return pd.DataFrame(columns=["item_code", "item_name", "item_group", "sn", "location", "um", "max_level", "min_level"])

def load_transactions(item_code=None):
    try:
        df = pd.read_csv(TRANS_URL)
        df = df.dropna(how="all")
        if item_code and not df.empty and "item_code" in df.columns:
            df = df[df["item_code"].astype(str) == str(item_code)]
        return df
    except Exception:
        return pd.DataFrame()

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["📦 View Registered Items", "📥📤 Add Transaction Details", "📊 View Stock Cards"])

# ==========================================
# PAGE 1: VIEW ITEMS
# ==========================================
if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List (From Google Sheets)")
    
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ ወይም ለማስተካከል በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# ==========================================
# PAGE 2: ADD TRANSACTION DETAILS
# ==========================================
elif page == "📥📤 Add Transaction Details":
    st.markdown("### 📥📤 Record Stock Movement (In / Out)")
    items_df = load_items()
    
    if items_df.empty or "item_code" not in items_df.columns:
        st.warning("No items found. Please add items in your Google Sheet first.")
    else:
        item_list = [f"{row['item_code']} - {row['item_name']}" for _, row in items_df.iterrows() if pd.notna(row['item_code'])]
        selected_item_str = st.selectbox("Select Item", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        item_data = items_df[items_df['item_code'].astype(str) == str(selected_code)].iloc[0]
        st.info(f"📍 Location: {item_data.get('location', '-')} | UM: {item_data.get('um', '-')} | Min Level: {item_data.get('min_level', 0)} | Max Level: {item_data.get('max_level', 0)}")

        st.markdown("#### Enter Movement Details:")
        trans_date = st.date_input("Date", datetime.now())
        ref_no = st.text_input("Ref / Voucher No")
        trans_type = st.radio("Movement Type", ["In (ገቢ)", "Out (ወጪ)"])
        unit_cost = st.number_input("Unit Cost (ETB)", min_value=0.0, step=0.01)
        qty = st.number_input("Quantity", min_value=0.0, step=1.0)
        
        st.write("---")
        st.markdown("🔗 **መረጃውን በቋሚነት ለመመዝገብ፦**")
        st.markdown(f"1. [እዚህ ይጫኑና Google Sheetዎን ይክፈቱ](https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit#gid=0)")
        st.markdown("2. **`transactions`** በሚለው ታብ ላይ የሚከተለውን መዝገብ በአዲስ መስመር ይጻፉ፦")
        
        if "In" in trans_type:
            q_in, q_out = qty, 0.0
        else:
            q_in, q_out = 0.0, qty
            
        st.code(f"Item Code: {selected_code} | Date: {trans_date} | Ref: {ref_no} | Qty In: {q_in} | Qty Out: {q_out} | Cost: {unit_cost}", language="text")

# ==========================================
# PAGE 3: VIEW STOCK CARDS
# ==========================================
elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty or "item_code" not in items_df.columns:
        st.warning("No items registered yet in Google Sheets.")
    else:
        item_list = [f"{row['item_code']} - {row['item_name']}" for _, row in items_df.iterrows() if pd.notna(row['item_code'])]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        st.dataframe(trans_df, use_container_width=True)
