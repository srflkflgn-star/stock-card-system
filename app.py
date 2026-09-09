import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="AMG Steel Factory - Inventory", layout="wide")

st.title("🏭 AMG STEEL FACTORY")
st.subheader("Inventory Control & Multi-Item Stock Card Management System")

# --- GOOGLE SHEETS SETUP ---
SHEET_ID = "1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI"
ITEMS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=items"
TRANS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=transactions"

# Clean item codes helper
def clean_code(code):
    if pd.isna(code):
        return ""
    val = str(code).strip()
    if val.endswith(".0"):
        val = val[:-2]
    return val

@st.cache_data(ttl=5)
def load_items():
    try:
        df = pd.read_csv(ITEMS_URL)
        df = df.dropna(how="all")
        df.columns = [str(col).strip().lower() for col in df.columns]
        
        code_col = [c for c in df.columns if 'code' in c or 'item' in c][0]
        df['clean_code'] = df[code_col].apply(clean_code)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=5)
def load_transactions(item_code=None):
    try:
        df = pd.read_csv(TRANS_URL)
        df = df.dropna(how="all")
        df.columns = [str(col).strip().lower() for col in df.columns]
        
        if df.empty:
            return df

        code_col = [c for c in df.columns if 'code' in c or 'item' in c][0]
        df['clean_code'] = df[code_col].apply(clean_code)
        
        if item_code:
            target_code = clean_code(item_code)
            df = df[df['clean_code'] == target_code].copy()
        
        if df.empty:
            return df

        df['qty_in'] = pd.to_numeric(df['qty_in'], errors='coerce').fillna(0)
        df['qty_out'] = pd.to_numeric(df['qty_out'], errors='coerce').fillna(0)
        df['balance_qty'] = (df['qty_in'] - df['qty_out']).cumsum()
        
        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "📦 View Registered Items", 
    "📥📤 Record Stock Movement (In/Out)", 
    "📊 View Stock Cards"
])

if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    
    components.html("<button onclick='window.print()' style='background-color:#008CBA; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print This Page</button>", height=50)
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

elif page == "📥📤 Record Stock Movement (In/Out)":
    st.markdown("### 📥📤 Stock Movement Helper")
    st.info("🔗 [በቀጥታ ወደ Google Sheet ለመሄድና ገቢ/ወጪ ለመጻፍ እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit#gid=0)")

elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty:
        st.warning("No items found.")
    else:
        name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else 'clean_code'
        
        item_list = [f"{row['clean_code']} - {row[name_col]}" for _, row in items_df.iterrows() if row['clean_code'] != ""]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        
        if not trans_df.empty:
            display_df = trans_df.drop(columns=['clean_code'], errors='ignore')
            st.dataframe(display_df, use_container_width=True)
            current_balance = trans_df['balance_qty'].iloc[-1]
            st.success(f"📦 **Current Stock Balance for Item {selected_code}: {current_balance}**")
            
            col1, col2 = st.columns(2)
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Stock Card Report</button>", height=50)
            with col2:
                csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv, file_name=f"Stock_Card_{selected_code}.csv", mime="text/csv")
        else:
            st.info("No transaction records found for this item.")
            
    st.info("💡 **ማስታወሻ:** ገቢና ወጪ መረጃ ለመጻፍ በቀጥታ [Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")
