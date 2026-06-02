import streamlit as st
import pandas as pd
from database import get_customers, add_customer, update_customer, delete_customer
from auth import is_admin


def show():
    """
    call the get_customers() from the database
    if the user is an admin, it shows the adding new customer form
    and then calls the add_customer() from the database
    """
    st.header("👥 Customers")
    customers = get_customers()

    if is_admin():
        with st.expander("➕ Add New Customer"):
            with st.form("add_customer"):
                name = st.text_input("Name*")
                phone = st.text_input("Phone")
                email = st.text_input("Email")
                address = st.text_area("Address", height=70)
                
                # checks if the button is clicked and the name field contains some data
                if st.form_submit_button("Add Customer") and name:
                    add_customer(name, phone, email, address)
                    st.success("Customer added!")
                    st.rerun()

    if not customers:
        st.info("No customers yet.")
        return

    # creates a dataframe of the returned list from the database
    df = pd.DataFrame(customers)[["name", "phone", "email", "address"]]
    # hide_index=True means it should hide the row numbers
    st.dataframe(df, width='stretch', hide_index=True)

    if is_admin():
        st.subheader("Edit / Delete")
        
        # adds a key with the name of the customer to a new dictionary for efficient retrievel
        # look up a full customer by just their name
        names = {c["name"]: c for c in customers}
        
        # the names are shown in the selectbox
        # keys of the dictionary are returned and converted to list
        selected = st.selectbox("Select customer", list(names.keys()))
        
        c = names[selected]
        with st.form("edit_customer"):
            name = st.text_input("Name", c["name"])
            phone = st.text_input("Phone", c["phone"] or "")
            email = st.text_input("Email", c["email"] or "")
            address = st.text_area("Address", c["address"] or "", height=70)
            
            col1, col2 = st.columns(2)
            if col1.form_submit_button("Update"):
                update_customer(c["id"], {"name": name, "phone": phone, "email": email, "address": address})
                st.success("Updated!")
                st.rerun()
            if col2.form_submit_button("🗑 Delete", type="secondary"):
                delete_customer(c["id"])
                st.warning("Deleted.")
                st.rerun()
