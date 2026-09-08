import streamlit as st
import pandas as pd

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
        # Standardize column names
        df.columns = [str(col).strip().lower() for col in df.columns]
        return df
    except Exception:
        return pd.DataFrame()

def load_transactions(item_code=None):
    try:
        df = pd.read_csv(TRANS_URL)
        df = df.dropna(how="all")
        df.columns = [str(col).strip().lower() for col in df.columns]
        
        # Flexibly locate columns regardless of exact header syntax
        in_col = [c for c in df.columns if 'in' in c and 'val' not in c]
        out_col = [c for c in df.columns if ('out' in c or 'qnt' in c) and 'val' not in c]
        code_col = [c for c in df.columns if 'code' in c or 'item' in c]
        
        if item_code and code_col and not df.empty:
            df = df[df[code_col[0]].astype(str) == str(item_code)]
            
        # Clean numerical values
        q_in_name = in_col[0] if in_col else 'qty_in'
        q_out_name = out_col[0] if out_col else 'qty_out'
        
        df['Qty In'] = pd.to_numeric(df[q_in_name], errors='coerce').fillna(0)
        df['Qty Out'] = pd.to_numeric(df[q_out_name], errors='coerce').fillna(0)
        
        # Calculate Running Balance Automatically
        df['Balance Qty'] = (df['Qty In'] - df['Qty Out']).cumsum()
        
        return df
    except Exception as e:
        return pd.DataFrame()

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["📦 View Registered Items", "📊 View Stock Cards"])

if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)

elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty:
        st.warning("No items found in Google Sheets.")
    else:
        code_col = [c for c in items_df.columns if 'code' in c or 'item' in c][0]
        name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else code_col
        
        item_list = [f"{row[code_col]} - {row[name_col]}" for _, row in items_df.iterrows() if pd.notna(row[code_col])]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        
        if not trans_df.empty:
            st.dataframe(trans_df, use_container_width=True)
            current_balance = trans_df['Balance Qty'].iloc[-1]
            st.success(f"📦 **Current Balance Qty for {selected_code}: {current_balance}**")
        else:
            st.info("No transaction records found for this item.")
