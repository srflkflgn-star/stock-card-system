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
        
        # Extract Month for Ethiopian Date / Standard Date parsing
        date_col = [c for c in df.columns if 'date' in c][0] if any('date' in c for c in df.columns) else None
        if date_col:
            def get_month_num(d_str):
                try:
                    s = str(d_str).strip()
                    # If date formatted as YYYY-MM-DD or YYYY/MM/DD
                    parts = s.replace('/', '-').split('-')
                    if len(parts) >= 2:
                        m = int(parts[1])
                        if 1 <= m <= 13:
                            return m
                except:
                    pass
                return 1

            df['eth_month_num'] = df[date_col].apply(get_month_num)
            df['eth_month'] = df['eth_month_num'].map(ETHIOPIAN_MONTHS)
        else:
            df['eth_month'] = "መስከረም (Meskerem)"

        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "📦 View Registered Items", 
    "📥📤 Record Stock Movement (In/Out)", 
    "📊 View Stock Cards",
    "📅 Monthly Stock Movement Report"
])

# ==========================================
# PAGE 1: VIEW REGISTERED ITEMS
# ==========================================
if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    
    components.html("<button onclick='window.print()' style='background-color:#008CBA; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print This Page</button>", height=50)
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# ==========================================
# PAGE 2: RECORD MOVEMENT
# ==========================================
elif page == "📥📤 Record Stock Movement (In/Out)":
    st.markdown("### 📥📤 Stock Movement Helper")
    st.info("🔗 [በቀጥታ ወደ Google Sheet ለመሄድና ገቢ/ወጪ ለመጻፍ እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit#gid=0)")

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
        
        date_col = [c for c in df.columns if 'date' in c][0] if any('date' in c for c in df.columns) else None
        if date_col:
            def get_month_num(d_str):
                try:
                    s = str(d_str).strip()
                    parts = s.replace('/', '-').split('-')
                    if len(parts) >= 2:
                        m = int(parts[1])
                        if 1 <= m <= 13:
                            return m
                except:
                    pass
                return 1

            df['eth_month_num'] = df[date_col].apply(get_month_num)
            df['eth_month'] = df['eth_month_num'].map(ETHIOPIAN_MONTHS)
        else:
            df['eth_month'] = "መስከረም (Meskerem)"

        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "📦 View Registered Items", 
    "📥📤 Record Stock Movement (In/Out)", 
    "📊 View Stock Cards",
    "📅 Monthly Stock Movement Report"
])

# PAGE 1: VIEW REGISTERED ITEMS
if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    components.html("<button onclick='window.print()' style='background-color:#008CBA; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print This Page</button>", height=50)
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 2: RECORD MOVEMENT
elif page == "📥📤 Record Stock Movement (In/Out)":
    st.markdown("### 📥📤 Stock Movement Helper")
    st.info("🔗 [በቀጥታ ወደ Google Sheet ለመሄድና ገቢ/ወጪ ለመጻፍ እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit#gid=0)")

# PAGE 3: VIEW STOCK CARDS
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
            display_df = trans_df.drop(columns=['clean_code', 'eth_month_num', 'eth_month'], errors='ignore')
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

# PAGE 4: MONTHLY REPORT & TEXT ANALYSIS
elif page == "📅 Monthly Stock Movement Report":
    st.markdown("### 📅 ወርኃዊ የገቢና ወጪ ዕቃዎች ማጠቃለያ እና የጽሁፍ ትንተና ሪፖርት")
    
    all_trans = load_transactions()
    items_df = load_items()
    
    if all_trans.empty:
        st.warning("ምንም የገቢና ወጪ መዝገብ አልተገኘም።")
    else:
        selected_month = st.selectbox("ሪፖርት የሚፈልጉበትን ወር ይምረጡ፦", list(ETHIOPIAN_MONTHS.values()))
        
        filtered_df = all_trans[all_trans['eth_month'] == selected_month]
        
        if filtered_df.empty:
            st.info(f"በ {selected_month} ወር ምንም የተቀሰቀሰ ገቢ ወይም ወጪ የለም።")
        else:
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
        
        date_col = [c for c in df.columns if 'date' in c][0] if any('date' in c for c in df.columns) else None
        if date_col:
            def get_month_num(d_str):
                try:
                    s = str(d_str).strip()
                    parts = s.replace('/', '-').split('-')
                    if len(parts) >= 2:
                        m = int(parts[1])
                        if 1 <= m <= 13:
                            return m
                except:
                    pass
                return 1

            df['eth_month_num'] = df[date_col].apply(get_month_num)
            df['eth_month'] = df['eth_month_num'].map(ETHIOPIAN_MONTHS)
        else:
            df['eth_month'] = "መስከረም (Meskerem)"

        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to", 
    [
        "📦 View Registered Items", 
        "📥📤 Record Stock Movement (In/Out)", 
        "📊 View Stock Cards",
        "📅 Monthly Stock Movement Report"
    ],
    key="main_navigation_radio"
)

# PAGE 1: VIEW REGISTERED ITEMS
if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    components.html("<button onclick='window.print()' style='background-color:#008CBA; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print This Page</button>", height=50)
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 2: RECORD MOVEMENT
elif page == "📥📤 Record Stock Movement (In/Out)":
    st.markdown("### 📥📤 Stock Movement Helper")
    st.info("🔗 [በቀጥታ ወደ Google Sheet ለመሄድና ገቢ/ወጪ ለመጻፍ እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit#gid=0)")

# PAGE 3: VIEW STOCK CARDS
elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty:
        st.warning("No items found.")
    else:
        name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else 'clean_code'
        item_list = [f"{row['clean_code']} - {row[name_col]}" for _, row in items_df.iterrows() if row['clean_code'] != ""]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list, key="stock_card_selectbox")
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        
        if not trans_df.empty:
            display_df = trans_df.drop(columns=['clean_code', 'eth_month_num', 'eth_month'], errors='ignore')
            st.dataframe(display_df, use_container_width=True)
            current_balance = trans_df['balance_qty'].iloc[-1]
            st.success(f"📦 **Current Stock Balance for Item {selected_code}: {current_balance}**")
            
            col1, col2 = st.columns(2)
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Stock Card Report</button>", height=50)
            with col2:
                csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv, file_name=f"Stock_Card_{selected_code}.csv", mime="text/csv", key="download_stock_card")
        else:
            st.info("No transaction records found for this item.")
            
    st.info("💡 **ማስታወሻ:** ገቢና ወጪ መረጃ ለመጻፍ በቀጥታ [Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 4: MONTHLY REPORT & TEXT ANALYSIS
elif page == "📅 Monthly Stock Movement Report":
    st.markdown("### 📅 ወርኃዊ የገቢና ወጪ ዕቃዎች ማጠቃለያ እና የጽሁፍ ትንተና ሪፖርት")
    
    all_trans = load_transactions()
    items_df = load_items()
    
    if all_trans.empty:
        st.warning("ምንም የገቢና ወጪ መዝገብ አልተገኘም።")
    else:
        selected_month = st.selectbox("ሪፖርት የሚፈልጉበትን ወር ይምረጡ፦", list(ETHIOPIAN_MONTHS.values()), key="monthly_report_selectbox")
        
        filtered_df = all_trans[all_trans['eth_month'] == selected_month]
        
        if filtered_df.empty:
            st.info(f"በ {selected_month} ወር ምንም የተቀሰቀሰ ገቢ ወይም ወጪ የለም።")
        else:
            summary = filtered_df.groupby('clean_code').agg(
                Total_Qty_In=('qty_in', 'sum'),
                Total_Qty_Out=('qty_out', 'sum'),
                Total_Transactions=('qty_in', 'count')
            ).reset_index()
            
            name_col = 'clean_code'
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
        
        date_col = [c for c in df.columns if 'date' in c][0] if any('date' in c for c in df.columns) else None
        if date_col:
            def get_month_num(d_str):
                try:
                    s = str(d_str).strip()
                    parts = s.replace('/', '-').split('-')
                    if len(parts) >= 2:
                        m = int(parts[1])
                        if 1 <= m <= 13:
                            return m
                except:
                    pass
                return 1

            df['eth_month_num'] = df[date_col].apply(get_month_num)
            df['eth_month'] = df['eth_month_num'].map(ETHIOPIAN_MONTHS)
        else:
            df['eth_month'] = "መስከረም (Meskerem)"

        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to", 
    [
        "📦 View Registered Items", 
        "📥📤 Record Stock Movement (In/Out)", 
        "📊 View Stock Cards",
        "📅 Monthly Stock Movement Report"
    ],
    key="main_navigation_radio"
)

# PAGE 1: VIEW REGISTERED ITEMS
if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    components.html("<button onclick='window.print()' style='background-color:#008CBA; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print This Page</button>", height=50)
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 2: RECORD MOVEMENT
elif page == "📥📤 Record Stock Movement (In/Out)":
    st.markdown("### 📥📤 Stock Movement Helper")
    st.info("🔗 [በቀጥታ ወደ Google Sheet ለመሄድና ገቢ/ወጪ ለመጻፍ እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit#gid=0)")

# PAGE 3: VIEW STOCK CARDS
elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty:
        st.warning("No items found.")
    else:
        name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else 'clean_code'
        item_list = [f"{row['clean_code']} - {row[name_col]}" for _, row in items_df.iterrows() if row['clean_code'] != ""]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list, key="stock_card_selectbox")
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        
        if not trans_df.empty:
            display_df = trans_df.drop(columns=['clean_code', 'eth_month_num', 'eth_month'], errors='ignore')
            st.dataframe(display_df, use_container_width=True)
            current_balance = trans_df['balance_qty'].iloc[-1]
            st.success(f"📦 **Current Stock Balance for Item {selected_code}: {current_balance}**")
            
            col1, col2 = st.columns(2)
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Stock Card Report</button>", height=50)
            with col2:
                csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv, file_name=f"Stock_Card_{selected_code}.csv", mime="text/csv", key="download_stock_card")
        else:
            st.info("No transaction records found for this item.")
            
    st.info("💡 **ማስታወሻ:** ገቢና ወጪ መረጃ ለመጻፍ በቀጥታ [Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 4: MONTHLY REPORT & TEXT ANALYSIS
elif page == "📅 Monthly Stock Movement Report":
    st.markdown("### 📅 ወርኃዊ የገቢና ወጪ ዕቃዎች ማጠቃለያ እና የጽሁፍ ትንተና ሪፖርት")
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
        
        date_col = [c for c in df.columns if 'date' in c][0] if any('date' in c for c in df.columns) else None
        if date_col:
            def get_month_num(d_str):
                try:
                    s = str(d_str).strip()
                    parts = s.replace('/', '-').split('-')
                    if len(parts) >= 2:
                        m = int(parts[1])
                        if 1 <= m <= 13:
                            return m
                except:
                    pass
                return 1

            df['eth_month_num'] = df[date_col].apply(get_month_num)
            df['eth_month'] = df['eth_month_num'].map(ETHIOPIAN_MONTHS)
        else:
            df['eth_month'] = "መስከረም (Meskerem)"

        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to", 
    [
        "📦 View Registered Items", 
        "📥📤 Record Stock Movement (In/Out)", 
        "📊 View Stock Cards",
        "📅 Monthly Stock Movement Report"
    ],
    key="main_navigation_radio"
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
        
        date_col = [c for c in df.columns if 'date' in c][0] if any('date' in c for c in df.columns) else None
        if date_col:
            def get_month_num(d_str):
                try:
                    s = str(d_str).strip()
                    parts = s.replace('/', '-').split('-')
                    if len(parts) >= 2:
                        m = int(parts[1])
                        if 1 <= m <= 13:
                            return m
                except:
                    pass
                return 1

            df['eth_month_num'] = df[date_col].apply(get_month_num)
            df['eth_month'] = df['eth_month_num'].map(ETHIOPIAN_MONTHS)
        else:
            df['eth_month'] = "መስከረም (Meskerem)"

        return df
    except Exception:
        return pd.DataFrame()

# Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to", 
    [
        "📦 View Registered Items", 
        "📥📤 Record Stock Movement (In/Out)", 
        "📊 View Stock Cards",
        "📅 Monthly Stock Movement Report"
    ],
    key="main_navigation_radio"
)

# PAGE 1: VIEW REGISTERED ITEMS
if page == "📦 View Registered Items":
    st.markdown("### 📦 Registered Items List")
    items_df = load_items()
    st.dataframe(items_df, use_container_width=True)
    components.html("<button onclick='window.print()' style='background-color:#008CBA; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print This Page</button>", height=50)
    st.info("💡 **ማስታወሻ:** አዲስ ዕቃ ለመመዝገብ በቀጥታ [የሁሉንም መረጃዎች Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 2: RECORD MOVEMENT
elif page == "📥📤 Record Stock Movement (In/Out)":
    st.markdown("### 📥📤 Stock Movement Helper")
    st.info("🔗 [በቀጥታ ወደ Google Sheet ለመሄድና ገቢ/ወጪ ለመጻፍ እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit#gid=0)")

# PAGE 3: VIEW STOCK CARDS
elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = load_items()
    
    if items_df.empty:
        st.warning("No items found.")
    else:
        name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else 'clean_code'
        item_list = [f"{row['clean_code']} - {row[name_col]}" for _, row in items_df.iterrows() if row['clean_code'] != ""]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list, key="stock_card_selectbox")
        selected_code = selected_item_str.split(" - ")[0]
        
        trans_df = load_transactions(selected_code)
        
        if not trans_df.empty:
            display_df = trans_df.drop(columns=['clean_code', 'eth_month_num', 'eth_month'], errors='ignore')
            st.dataframe(display_df, use_container_width=True)
            current_balance = trans_df['balance_qty'].iloc[-1]
            st.success(f"📦 **Current Stock Balance for Item {selected_code}: {current_balance}**")
            
            col1, col2 = st.columns(2)
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Stock Card Report</button>", height=50)
            with col2:
                csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv, file_name=f"Stock_Card_{selected_code}.csv", mime="text/csv", key="download_stock_card")
        else:
            st.info("No transaction records found for this item.")
            
    st.info("💡 **ማስታወሻ:** ገቢና ወጪ መረጃ ለመጻፍ በቀጥታ [Google Sheet ለመክፈት እዚህ ይጫኑ](https://docs.google.com/spreadsheets/d/1zC7Wuzlwm-LKUxzFaIe83jLHlfwU9mro8hq2S9HM0YI/edit)።")

# PAGE 4: MONTHLY REPORT & TEXT ANALYSIS
elif page == "📅 Monthly Stock Movement Report":
    st.markdown("### 📅 ወርኃዊ የገቢና ወጪ ዕቃዎች ማጠቃለያ እና የጽሁፍ ትንተና ሪፖርት")
    
    all_trans = load_transactions()
    items_df = load_items()
    
    if all_trans.empty:
        st.warning("ምንም የገቢና ወጪ መዝገብ አልተገኘም።")
    else:
        selected_month = st.selectbox("ሪፖርት የሚፈልጉበትን ወር ይምረጡ፦", list(ETHIOPIAN_MONTHS.values()), key="monthly_report_selectbox")
        
        filtered_df = all_trans[all_trans['eth_month'] == selected_month]
        
        if filtered_df.empty:
            st.info(f"በ {selected_month} ወር ምንም የተቀሰቀሰ ገቢ ወይም ወጪ የለም።")
        else:
            summary = filtered_df.groupby('clean_code').agg(
                Total_Qty_In=('qty_in', 'sum'),
                Total_Qty_Out=('qty_out', 'sum'),
                Total_Transactions=('qty_in', 'count')
            ).reset_index()
            
            name_col = 'clean_code'
            if not items_df.empty:
                name_col = [c for c in items_df.columns if 'name' in c][0] if any('name' in c for c in items_df.columns) else 'clean_code'
                summary = pd.merge(summary, items_df[['clean_code', name_col]], on='clean_code', how='left')
            else:
                summary['item_name'] = summary['clean_code']

            total_in_all = summary['Total_Qty_In'].sum()
            total_out_all = summary['Total_Qty_Out'].sum()
            active_items_count = len(summary)

            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("📦 የተንቀሳቀሱ ዕቃዎች ብዛት", f"{active_items_count} ዓይነት")
            col_m2.metric("📥 የወሩ አጠቃላይ ገቢ", f"{total_in_all:,.0f}")
            col_m3.metric("📤 የወሩ አጠቃላይ ወጪ", f"{total_out_all:,.0f}")

            st.markdown("---")
            st.markdown(f"#### 📊 የ {selected_month} ወር የሠንጠረዥ ማጠቃለያ")
            
            display_summary = summary.copy()
            display_summary.rename(columns={
                'clean_code': 'Item Code',
                name_col: 'Item Name',
                'Total_Qty_In': 'አጠቃላይ ገቢ (Total In)',
                'Total_Qty_Out': 'አጠቃላይ ወጪ (Total Out)',
                'Total_Transactions': 'የእንቅስቃሴ ብዛት'
            }, inplace=True)
            
            st.dataframe(display_summary, use_container_width=True)

            top_in_row = summary.loc[summary['Total_Qty_In'].idxmax()] if not summary.empty else None
            top_out_row = summary.loc[summary['Total_Qty_Out'].idxmax()] if not summary.empty else None

            st.markdown("---")
            st.markdown(f"### 📝 የ {selected_month} ወር የስቶክ እንቅስቃሴ የጽሁፍ ትንተና (Executive Summary)")
            
            top_in_name = top_in_row[name_col] if (top_in_row is not None and pd.notna(top_in_row[name_col])) else 'N/A'
            top_in_code = top_in_row['clean_code'] if top_in_row is not None else ''
            top_in_qty = top_in_row['Total_Qty_In'] if top_in_row is not None else 0

            top_out_name = top_out_row[name_col] if (top_out_row is not None and pd.notna(top_out_row[name_col])) else 'N/A'
            top_out_code = top_out_row['clean_code'] if top_out_row is not None else ''
            top_out_qty = top_out_row['Total_Qty_Out'] if top_out_row is not None else 0

            analysis_text = f"""
            **የ {selected_month} ወር የስቶክ እንቅስቃሴ ማጠቃለያ ትንተና፦**

            1. **አጠቃላይ እንቅስቃሴ፦** በያዝነው **{selected_month}** ወር ውስጥ በአጠቃላይ **{active_items_count}** በሚሆኑ የዕቃ ዓይነቶች ላይ የስቶክ እንቅስቃሴ ተመዝግቧል። በዚህም መሰረት በወሩ ውስጥ **{total_in_all:,.0f}** አጠቃላይ የዕቃ ገቢ የተደረገ ሲሆን፣ **{total_out_all:,.0f}** የዕቃ ወጪ ተደርጓል።

            2. **ከፍተኛ ገቢ የተደረገበት ዕቃ፦** በወሩ ውስጥ ከፍተኛ መጠን ያለው ገቢ የተመዘገበበት ዕቃ **{top_in_name}** (ኮድ: `{top_in_code}`) ሲሆን፣ አጠቃላይ የገባው ብዛት **{top_in_qty:,.0f}** ነው።

            3. **ከፍተኛ ወጪ የተደረገበት ዕቃ፦** በወሩ በብዛት ለምርት/ለስራ ወጪ የተደረገው ዕቃ **{top_out_name}** (ኮድ: `{top_out_code}`) ሲሆን፣ አጠቃላይ የወጣው ብዛት **{top_out_qty:,.0f}** ነው።

            4. **የስቶክ ሚዛን እና ማሳሰቢያ፦** የወሩ የወጪ እና የገቢ መጠን ሲነጻጸር የስቶክ ፍሰቱ አጠቃላይ ሁኔታን ያሳያል። ለኃላፊዎች እና ለቅርብ ክትትል እንዲመች ይህ ሪፖርት በጽሁፍና በሰንጠረዥ ተዘጋጅቷል።
            """
            
            st.info(analysis_text)

            col1, col2 = st.columns(2)
            with col1:
                components.html("<button onclick='window.print()' style='background-color:#4CAF50; color:white; padding:8px 16px; border:none; border-radius:4px; cursor:pointer;'>🖨️ Print Report & Analysis</button>", height=50)
            with col2:
                csv_m = display_summary.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Report as CSV", data=csv_m, file_name=f"Monthly_Report_{selected_month}.csv", mime="text/csv", key="download_monthly_summary")
