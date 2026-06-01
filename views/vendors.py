import streamlit as st
import pandas as pd
from database import get_vendors, add_vendor, update_vendor, delete_vendor
from auth import is_admin

def show():
    st.header("🏭 Vendors")
    vendors = get_vendors()

    if is_admin():
        with st.expander("➕ Add New Vendor"):
            with st.form("add_vendor"):
                name = st.text_input("Name*")
                phone = st.text_input("Phone")
                email = st.text_input("Email")
                address = st.text_area("Address", height=70)
                if st.form_submit_button("Add Vendor") and name:
                    add_vendor(name, phone, email, address)
                    st.success("Vendor added!")
                    st.rerun()

    if not vendors:
        st.info("No vendors yet.")
        return

    df = pd.DataFrame(vendors)[["name", "phone", "email", "address", "id"]]
    st.dataframe(df.drop(columns=["id"]), use_container_width=True, hide_index=True)

    if is_admin():
        st.subheader("Edit / Delete")
        names = {v["name"]: v for v in vendors}
        selected = st.selectbox("Select vendor", list(names.keys()))
        v = names[selected]
        with st.form("edit_vendor"):
            name = st.text_input("Name", v["name"])
            phone = st.text_input("Phone", v["phone"] or "")
            email = st.text_input("Email", v["email"] or "")
            address = st.text_area("Address", v["address"] or "", height=70)
            c1, c2 = st.columns(2)
            if c1.form_submit_button("Update"):
                update_vendor(v["id"], {"name": name, "phone": phone, "email": email, "address": address})
                st.success("Updated!")
                st.rerun()
            if c2.form_submit_button("🗑 Delete", type="secondary"):
                delete_vendor(v["id"])
                st.warning("Deleted.")
                st.rerun()
