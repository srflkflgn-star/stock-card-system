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
                
