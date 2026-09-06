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
    df = pd.read_sql_query("SELECT id AS 'ID', trans_date AS Date, ref_no AS 'Ref No', qty_in AS 'Qty In', qty_out AS 'Qty Out', balance_qty AS 'Balance Qty', val_in AS 'Value In (ETB)', val_out AS 'Value Out (ETB)', balance_val AS 'Balance Value (ETB)', unit_cost AS 'Unit Cost (ETB)' FROM transactions WHERE item_code = ? ORDER BY id ASC", conn, params=(item_code,))
    conn.close()
    return df

def recalculate_balances(item_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, qty_in, qty_out, unit_cost FROM transactions WHERE item_code = ? ORDER BY id ASC", (item_code,))
    rows = c.fetchall()
    
    current_balance = 0.0
    for row in rows:
        t_id, q_in, q_out, u_cost = row
        current_balance += (q_in - q_out)
        val_balance = current_balance * u_cost
        c.execute("UPDATE transactions SET balance_qty = ?, balance_val = ? WHERE id = ?", (current_balance, val_balance, t_id))
        
    conn.commit()
    conn.close()

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["📦 Add / Manage Items", "📥📤 Add Transaction (In/Out)", "📊 View Stock Cards"])

# ==========================================
# PAGE 1: ADD / MANAGE ITEMS & DELETE ITEM
# ==========================================
if page == "📦 Add / Manage Items":
    st.markdown("### 📦 Register a New Item")
    
    item_code = st.text_input("Item Code (Unique ID)*")
    item_name = st.text_input("Item Name*")
    item_group = st.text_input("Item Group")
    sn = st.text_input("Serial Number (SN)")
    location = st.text_input("Location in Store")
    um = st.text_input("Unit of Measurement (UM)")
    max_level = st.number_input("Max Stock Level", min_value=0.0, value=0.0)
    min_level = st.number_input("Min Stock Level", min_value=0.0, value=0.0)
        
    if st.button("Save Item", type="primary"):
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
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Error: An item with this Item Code already exists!")
            finally:
                conn.close()

    st.markdown("---")
    st.markdown("### 📋 Existing Registered Items & Delete Option")
    items_df = get_items()
    st.dataframe(items_df, use_container_width=True)
    
    if not items_df.empty:
        st.markdown("#### 🗑️ Delete an Item")
        delete_list = [f"{row['item_code']} - {row['item_name']}" for _, row in items_df.iterrows()]
        item_to_delete = st.selectbox("Select Item to Delete Permanently", delete_list)
        delete_code = item_to_delete.split(" - ")[0]
        
        if st.button("❌ Delete Selected Item & All Its Transactions"):
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM transactions WHERE item_code = ?", (delete_code,))
            c.execute("DELETE FROM items WHERE item_code = ?", (delete_code,))
            conn.commit()
            conn.close()
            st.success("Item and its transactions deleted successfully!")
            st.rerun()

# ==========================================
# PAGE 2: ADD TRANSACTION
# ==========================================
elif page == "📥📤 Add Transaction (In/Out)":
    st.markdown("### 📥📤 Record Stock Movement (In / Out)")
    items_df = get_items()
    
    if items_df.empty:
        st.warning("No items found. Please add an item first from 'Add / Manage Items' page.")
    else:
        item_list = [f"{row['item_code']} - {row['item_name']}" for _, row in items_df.iterrows()]
        selected_item_str = st.selectbox("Select Item", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        item_data = items_df[items_df['item_code'] == selected_code].iloc[0]
        st.info(f"📍 Location: {item_data['location']} | UM: {item_data['um']} | Min Level: {item_data['min_level']} | Max Level: {item_data['max_level']}")

        st.markdown("#### Enter Movement Details:")
        trans_date = st.date_input("Date", datetime.now())
        ref_no = st.text_input("Ref / Voucher No")
        trans_type = st.radio("Movement Type", ["In (ገቢ)", "Out (ወጪ)"])
        unit_cost = st.number_input("Unit Cost (ETB)", min_value=0.0, step=0.01)
        qty = st.number_input("Quantity", min_value=0.0, step=1.0)
        
        if st.button("📥📤 Record Transaction", type="primary"):
            trans_df = get_item_transactions(selected_code)
            prev_balance_qty = trans_df.iloc[-1]['Balance Qty'] if not trans_df.empty else 0.0

            if "In" in trans_type:
                qty_in = qty
                qty_out = 0.0
                new_balance_qty = prev_balance_qty + qty_in
            else:
                qty_in = 0.0
                qty_out = qty
                new_balance_qty = prev_balance_qty - qty_out

            val_in = qty_in * unit_cost
            val_out = qty_out * unit_cost
            val_balance = new_balance_qty * unit_cost

            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("""
                INSERT INTO transactions 
                (item_code, trans_date, ref_no, trans_type, qty, unit_cost, qty_in, qty_out, balance_qty, val_in, val_out, balance_val)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (selected_code, trans_date.strftime('%Y-%m-%d'), ref_no, trans_type, qty, unit_cost, qty_in, qty_out, new_balance_qty, val_in, val_out, val_balance))
            conn.commit()
            conn.close()
            st.success("Transaction recorded successfully!")
            st.rerun()

# ==========================================
# PAGE 3: VIEW STOCK CARDS & DELETE TRANSACTION
# ==========================================
elif page == "📊 View Stock Cards":
    st.markdown("### 📊 Stock Card Ledger by Item")
    items_df = get_items()
    
    if items_df.empty:
        st.warning("No items registered yet.")
    else:
        item_list = [f"{row['item_code']} - {row['item_name']}" for _, row in items_df.iterrows()]
        selected_item_str = st.selectbox("Select Item to View Stock Card", item_list)
        selected_code = selected_item_str.split(" - ")[0]
        
        item_data = items_df[items_df['item_code'] == selected_code].iloc[0]
        
        st.markdown(f"""
        **Item Code:** {item_data['item_code']} | **Item Name:** {item_data['item_name']} | **Group:** {item_data['item_group']}  
        **SN:** {item_data['sn']} | **Location:** {item_data['location']} | **UM:** {item_data['um']}  
        **Min Level:** {item_data['min_level']} | **Max Level:** {item_data['max_level']}
        """)
        
        trans_df = get_item_transactions(selected_code)
        
        if not trans_df.empty:
            current_stock = trans_df.iloc[-1]['Balance Qty']
            if item_data['min_level'] > 0 and current_stock <= item_data['min_level']:
                st.warning(f"⚠️ **ALERT:** Stock level is below minimum threshold! Current Stock: {current_stock}")
            elif item_data['max_level'] > 0 and current_stock >= item_data['max_level']:
                st.info(f"ℹ️ **NOTICE:** Stock level has reached maximum threshold. Current Stock: {current_stock}")

        st.dataframe(trans_df, use_container_width=True)
        
        if not trans_df.empty:
            st.markdown("---")
            csv = trans_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export This Item's Ledger to Excel/CSV",
                data=csv,
                file_name=f"Stock_Card_{selected_code}.csv",
                mime='text/csv'
            )
            
            st.markdown("#### 🗑️ Delete Specific Transaction")
            trans_id_to_del = st.selectbox("Select ID of Transaction to Delete", trans_df['ID'].tolist())
            if st.button("Delete Transaction"):
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("DELETE FROM transactions WHERE id = ?", (trans_id_to_del,))
                conn.commit()
                conn.close()
                
                # Recalculate remaining balances
                recalculate_balances(selected_code)
                st.success(f"Transaction ID {trans_id_to_del} deleted and balances updated!")
                st.rerun()
