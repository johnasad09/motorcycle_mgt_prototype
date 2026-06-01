import streamlit as st
from auth import login, logout, is_admin

# import modules/python files from pages directory
from views import dashboard, vendors, customers, parts, purchases, sales, financials

st.set_page_config(page_title="MotoParts Manager", page_icon="🔧", layout="wide")

# call login function
if not login():
    st.stop()

# calling log out function that shows the log out button if the user is loged in
logout()
# if the user is logged in, it shows the username and the role
st.sidebar.markdown(f"**{st.session_state['username']}** `{st.session_state['role']}`")
st.sidebar.divider()

# dictionary of Pages to show and their python files
PAGES = {
    "Dashboard": dashboard,
    "Purchases": purchases,
    "Sales": sales,
    "Parts & Stock": parts,
    "Financials": financials,
    "Vendors": vendors,
    "Customers": customers,
}

# Staff cannot access Vendors/Customers management pages
if not is_admin():
    # returns all the pages except vendors and customers
    PAGES = {k: v for k, v in PAGES.items() if k not in ["Vendors", "Customers"]}

# shows a radio buttons with pages list and stores the current page 
page = st.sidebar.radio("Navigation", list(PAGES.keys()))

# calls the show() function available in all the python pages
PAGES[page].show()
