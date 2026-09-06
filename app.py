import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="AMG Steel Factory - Multi-Item Inventory System", layout="wide")

st.title("🏭 AMG STEEL FACTORY")
st.subheader("Inventory Control & Multi-Item Stock Card Management System")

# --- DATABASE SETUP ---
DB_NAME = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table for storing items
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_code TEXT PRIMARY KEY,
            item_name TEXT,
            item_group TEXT,
            sn TEXT,
            location TEXT,
            um TEXT,
            max_level REAL,
            min_level REAL
        )
    ''')
    # Table for storing transactions
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT,
            trans_date TEXT,
            ref_no TEXT,
            trans_type TEXT,
            qty REAL,
            unit_cost REAL,
            qty_in REAL,
            qty_out REAL,
            balance_qty REAL,
            val_in REAL,
            val_out REAL,
            balance_val REAL,
            FOREIGN KEY (item_code) REFERENCES items (item_code)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- HELPER FUNCTIONS ---
def get_items():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM items", conn)
    conn.close()
    return df

def get_item_transactions(item_code):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT trans_date AS Date, ref_no AS 'Ref No', qty_in AS 'Qty In', qty_out AS 'Qty Out', balance_qty AS 'Balance Qty', val_in AS 'Value In (ETB)', val_out AS 'Value Out (ETB)', balance_val AS 'Balance Value (ETB)', unit_cost AS 'Unit Cost (ETB)' FROM transactions WHERE item_code = ? ORDER BY id ASC", conn, params=(item_code,))
    conn.close()
    return df

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["📦 Add New Item", "📥📤 Add Transaction (In/Out)", "📊 View Stock Cards"])

# ==========================================
# PAGE 1: ADD NEW ITEM
# ==========================================
if page == "📦 Add New Item":
    st.markdown("### 📦 Register a New Item")
    with st.form("new_item_form"):
        col1, col2 = st.columns(2)
        with col1:
            item_code = st.text_input("Item Code (Unique ID)*")
            item_name = st.text_input("Item Name*")
            item_group = st.text_input("Item Group")
            sn = st.text_input("Serial Number (SN)")
        with col2:
            location = st.text_input("Location in Store")
            um = st.text_input("Unit of Measurement (UM)")
            max_level = st.number_input("Max Stock Level", min_value=0.0, value=0.0)
            min_level = st.number_input("Min Stock Level", min_value=0.0, value=0.0)
            
        submit_item = st.form_submit_button("Save Item")
        
    if submit_item:
        if not item_code or not item_name:
            st.error("Please fill in required fields: Item Code and Item Name!")
        else:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            try:
                c.execute("""
                    INSERT INTO items (item_code, item_name, item_group, sn, location, um, max_level, min_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (item_code, item_name, item_group, sn, location, um, max_level, min_level))
                conn.commit()
                st.success(f"Item '{item_name}' registered successfully!")
            except sqlite3.IntegrityError:
                st.error("Error: An item with this Item Code already exists!")
            finally:
                conn.close()

    st.markdown("---")
    st.markdown("### 📋 Existing Registered Items")
    items_df = get_items()
    st.dataframe(items_df, use_container_width=True)

# ==========================================
# PAGE 2: ADD TRANSACTION
# ==========================================
elif page == "📥📤 Add Transaction (In/Out)":
    st.markdown("### 📥📤 Record Stock Movement (In / Out)")
    items_df = get_items()
    
    if items_df.empty:
        st.warning("No items found. Please add an item first from 'Add New Item' page.")
    else:
        # Item selector dropdown
        item_list = [f"{row['item_code']} - {row['item_name']}" for _, row in items_df.iterrows()]
        selected_item_str = st.selectbox("Select Item", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
