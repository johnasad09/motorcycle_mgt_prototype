import streamlit as st
import pandas as pd
from database import get_parts, add_part, update_part, delete_part
from auth import is_admin

def show():
    st.header("🔩 Parts & Stock")
    parts = get_parts()

    if is_admin():
        with st.expander("➕ Add New Part"):
            with st.form("add_part"):
                c1, c2 = st.columns(2)
                part_id = c1.text_input("Part ID*")
                name = c2.text_input("Name*")
                description = st.text_area("Description", height=60)
                c1, c2, c3, c4, c5 = st.columns(5)
                quantity = c1.number_input("Qty", 0, step=1)
                per_pack = c2.number_input("Per Pack", 1, step=1)
                cost_price = c3.number_input("Cost ₨", 0.0, step=1.0)
                sale_price = c4.number_input("Sale ₨", 0.0, step=1.0)
                if st.form_submit_button("Add Part") and part_id and name:
                    try:
                        add_part(part_id, name, description, quantity, per_pack, cost_price, sale_price)
                        st.success("Part added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    if not parts:
        st.info("No parts yet.")
        return

    df = pd.DataFrame(parts)[["part_id", "name", "description", "quantity", "per_pack", "cost_price", "sale_price"]]
    df.columns = ["Part ID", "Name", "Description", "Qty", "Per Pack", "Cost ₨", "Sale ₨"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    if is_admin():
        st.subheader("Edit / Delete")
        pmap = {f"{p['part_id']} — {p['name']}": p for p in parts}
        selected = st.selectbox("Select part", list(pmap.keys()))
        p = pmap[selected]
        with st.form("edit_part"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Name", p["name"])
            description = c2.text_input("Description", p["description"] or "")
            c1, c2, c3, c4 = st.columns(4)
            quantity = c1.number_input("Qty", value=p["quantity"], step=1)
            per_pack = c2.number_input("Per Pack", value=p["per_pack"], step=1)
            cost_price = c3.number_input("Cost ₨", value=float(p["cost_price"]), step=1.0)
            sale_price = c4.number_input("Sale ₨", value=float(p["sale_price"]), step=1.0)
            col1, col2 = st.columns(2)
            if col1.form_submit_button("Update"):
                update_part(p["id"], {
                    "name": name, "description": description, "quantity": quantity,
                    "per_pack": per_pack, "cost_price": cost_price, "sale_price": sale_price
                })
                st.success("Updated!")
                st.rerun()
            if col2.form_submit_button("🗑 Delete", type="secondary"):
                delete_part(p["id"])
                st.warning("Deleted.")
                st.rerun()
