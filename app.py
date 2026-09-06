import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="AMG Steel Factory - Inventory System", layout="wide")

st.title("🏭 AMG STEEL FACTORY")
st.subheader("Inventory Control & Stock Card Management System")

# Initialize Session State for Data Persistence
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = pd.DataFrame(columns=[
        'Date', 'Ref No', 'Qty In', 'Qty Out', 'Balance Qty', 
        'Value In (ETB)', 'Value Out (ETB)', 'Balance Value (ETB)', 'Unit Cost (ETB)'
    ])

if 'item_info' not in st.session_state:
    st.session_state.item_info = {
        'group': '', 'name': '', 'sn': '', 'code': '', 
        'location': '', 'um': '', 'max_level': 0, 'min_level': 0
    }

# --- SECTION 1: Item Header Details ---
st.markdown("### 📋 Item Information")
col1, col2 = st.columns(2)

with col1:
    group = st.text_input("Item Group", value=st.session_state.item_info['group'])
    sn = st.text_input("Serial Number (SN)", value=st.session_state.item_info['sn'])
    location = st.text_input("Location", value=st.session_state.item_info['location'])
    max_level = st.number_input("Max. Stock Level", min_value=0, value=st.session_state.item_info['max_level'])

with col2:
    name = st.text_input("Item Name", value=st.session_state.item_info['name'])
    code = st.text_input("Item Code", value=st.session_state.item_info['code'])
    um = st.text_input("Unit of Measurement (UM)", value=st.session_state.item_info['um'])
    min_level = st.number_input("Minimum Stock Level", min_value=0, value=st.session_state.item_info['min_level'])

# --- SECTION 2: Transaction Entry Form ---
st.markdown("---")
st.markdown("### 📥📤 Stock Transaction Entry")

with st.form(key='transaction_form'):
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        trans_date = st.date_input("Date", datetime.now())
        ref_no = st.text_input("Ref. No")
        
    with f_col2:
        unit_cost = st.number_input("Unit Cost (ETB)", min_value=0.0, step=0.01)
        trans_type = st.radio("Transaction Type", ["In", "Out"])
        
    with f_col3:
        qty = st.number_input("Quantity", min_value=0, step=1)
        
    with f_col4:
        st.write("") # Formatting Spacer
        st.write("")
        submit_button = st.form_submit_button(label='Add Transaction')

# Processing Transaction Logic
if submit_button:
    # Get previous balance
    if not st.session_state.stock_data.empty:
        prev_balance_qty = st.session_state.stock_data.iloc[-1]['Balance Qty']
    else:
        prev_balance_qty = 0

    if trans_type == "In":
        qty_in = qty
        qty_out = 0
        new_balance_qty = prev_balance_qty + qty_in
    else:
        qty_in = 0
        qty_out = qty
        new_balance_qty = prev_balance_qty - qty_out

    val_in = qty_in * unit_cost
    val_out = qty_out * unit_cost
    val_balance = new_balance_qty * unit_cost

    # Append transaction record
    new_row = {
        'Date': trans_date.strftime('%Y-%m-%d'),
        'Ref No': ref_no,
        'Qty In': qty_in,
        'Qty Out': qty_out,
        'Balance Qty': new_balance_qty,
        'Value In (ETB)': val_in,
        'Value Out (ETB)': val_out,
        'Balance Value (ETB)': val_balance,
        'Unit Cost (ETB)': unit_cost
    }
    
    st.session_state.stock_data = pd.concat([st.session_state.stock_data, pd.DataFrame([new_row])], ignore_index=True)
    st.success("Transaction recorded successfully!")

# --- SECTION 3: Stock Card Table & Data Visualizer ---
st.markdown("---")
st.markdown("### 📊 Stock Card Ledger")

# Low/High Stock Inventory Alerts
if not st.session_state.stock_data.empty:
    current_stock = st.session_state.stock_data.iloc[-1]['Balance Qty']
    if min_level > 0 and current_stock <= min_level:
        st.warning(f"⚠️ **ALERT:** Stock level is at or below the Minimum Stock Threshold! (Current: {current_stock} | Min: {min_level})")
    elif max_level > 0 and current_stock >= max_level:
        st.info(f"ℹ️ **NOTICE:** Stock level has reached or exceeded the Maximum Limit. (Current: {current_stock} | Max: {max_level})")

st.dataframe(st.session_state.stock_data, use_container_width=True)

# Export Data Option
if not st.session_state.stock_data.empty:
    csv = st.session_state.stock_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Ledger to Excel/CSV",
        data=csv,
        file_name=f"Stock_Card_{code if code else 'Report'}.csv",
        mime='text/csv',
    )
