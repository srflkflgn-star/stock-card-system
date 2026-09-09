import streamlit as st
import pandas as pd

st.set_page_config(page_title="AMG Steel Factory - Inventory", layout="wide")

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
        df.columns = [str(col).strip().lower() for col in df.columns]
        return df
    except Exception:
        return pd.DataFrame()

def load_transactions(item_code):
    try:
        df = pd.read_csv(TRANS_URL)
        df = df.dropna(how="all")
        df.columns = [str(col).strip().lower() for col in df.columns]
        
        # Filter by selected item code
        code_col = [c for c in df.columns if 'code' in c or 'item' in c][0]
        df = df[df[code_col].astype(str) == str(item_code)].copy()
        
        if df.empty:
            return df

        # Clean numerical values
        df['qty_in'] = pd.to_numeric(df['qty_in'], errors='coerce').fillna(0)
        df['qty_out'] = pd.to_numeric(df['qty_out'], errors='coerce').fillna(0)
        
        # Calculate balance automatically (Cumulative Balance)
        df['balance_qty'] = (df['qty_in'] - df['qty_out']).cumsum()
        
        return df
    except Exception as e:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["📦 View Registered Items", "📊 View Stock Cards"])

if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    
    # ሰማያዊው ማስታወሻና የ Google Sheet ሊንክ
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ ወይም ለማስተካከል በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty:
        st.warning("No items found.")
    else:
        code_col = [c for c in items_df.columns if 'code' in c or 'item' in c][0]
        name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else code_col
        
        item_list = [f"{row[code_col]} - {row[name_col]}" for _, row in items_df.iterrows() if pd.notna(row[code_col])]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        
        if not trans_df.empty:
            st.dataframe(trans_df, use_container_width=True)
            current_balance = trans_df['balance_qty'].iloc[-1]
            st.success(f"📦 **Current Stock Balance for {selected_code}: {current_balance}**")
        else:
            st.info("No transaction records found for this item.")
            
    # ሰማያዊው ማስታወሻና የ Google Sheet ሊንክ
    st.info("💡 **ማስታወሻ:** ገቢና ወጪ መረጃ ለመጻፍ በቀጥታ [Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")
