import streamlit as st
import pandas as pd
from database import get_customers, get_parts, record_sale, get_sales
from datetime import date, timedelta

def show():
    st.header("💵 Sales (Sell to Customer)")

    customers = get_customers()
    parts = get_parts()

    if not customers or not parts:
        st.warning("Add at least one customer and one part first.")
        return

    with st.expander("➕ Record Sale", expanded=True):
        with st.form("sale_form"):
            c1, c2 = st.columns(2)
            cust_map = {c["name"]: c["id"] for c in customers}
            part_map = {f"{p['part_id']} — {p['name']} (Stock: {p['quantity']})": p for p in parts}
            cust_sel = c1.selectbox("Customer", list(cust_map.keys()))
            part_sel = c2.selectbox("Part", list(part_map.keys()))
            p = part_map[part_sel]
            c1, c2, c3 = st.columns(3)
            qty = c1.number_input("Quantity", 1, max_value=p["quantity"], step=1)
            price = c2.number_input("Sale Price ₨", value=float(p["sale_price"]), step=1.0)
            c3.metric("Total", f"₨{qty * price:,.0f}")
            note = st.text_input("Note (optional)")
            if st.form_submit_button("Record Sale"):
                try:
                    record_sale(cust_map[cust_sel], p["id"], qty, price, note)
                    st.success("Sale recorded. Stock updated.")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    st.subheader("Sales History")
    c1, c2 = st.columns(2)
    start = c1.date_input("From", date.today() - timedelta(days=30), key="ss")
    end = c2.date_input("To", date.today(), key="se")
    rows = get_sales(start.isoformat(), (end + timedelta(days=1)).isoformat())

    if not rows:
        st.info("No sales in this period.")
        return

    df = pd.DataFrame([{
        "Date": r["created_at"][:10],
        "Customer": r["customers"]["name"],
        "Part": r["parts"]["name"],
        "Part ID": r["parts"]["part_id"],
        "Qty": r["quantity"],
        "Sale ₨": r["sale_price"],
        "Total ₨": r["total"],
        "Note": r.get("note", ""),
    } for r in rows])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.metric("Total Revenue", f"₨{df['Total ₨'].sum():,.0f}")
