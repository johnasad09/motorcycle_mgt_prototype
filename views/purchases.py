import streamlit as st
import pandas as pd
from database import get_vendors, get_parts, record_purchase, get_purchases
from datetime import date, timedelta

def show():
    st.header("🛒 Purchases (Buy from Vendor)")

    vendors = get_vendors()
    parts = get_parts()

    if not vendors or not parts:
        st.warning("Add at least one vendor and one part first.")
        return

    with st.expander("➕ Record Purchase", expanded=True):
        with st.form("purchase_form"):
            c1, c2 = st.columns(2)
            vendor_map = {v["name"]: v["id"] for v in vendors}
            part_map = {f"{p['part_id']} — {p['name']}": p for p in parts}
            vendor_sel = c1.selectbox("Vendor", list(vendor_map.keys()))
            part_sel = c2.selectbox("Part", list(part_map.keys()))
            p = part_map[part_sel]
            c1, c2, c3 = st.columns(3)
            qty = c1.number_input("Quantity", 1, step=1)
            cost = c2.number_input("Cost Price ₨", value=float(p["cost_price"]), step=1.0)
            c3.metric("Total", f"₨{qty * cost:,.0f}")
            note = st.text_input("Note (optional)")
            if st.form_submit_button("Record Purchase"):
                record_purchase(vendor_map[vendor_sel], p["id"], qty, cost, note)
                st.success(f"Purchase recorded. Stock updated.")
                st.rerun()

    st.subheader("Purchase History")
    c1, c2 = st.columns(2)
    start = c1.date_input("From", date.today() - timedelta(days=30), key="ps")
    end = c2.date_input("To", date.today(), key="pe")
    rows = get_purchases(start.isoformat(), (end + timedelta(days=1)).isoformat())

    if not rows:
        st.info("No purchases in this period.")
        return

    df = pd.DataFrame([{
        "Date": r["created_at"][:10],
        "Vendor": r["vendors"]["name"],
        "Part": r["parts"]["name"],
        "Part ID": r["parts"]["part_id"],
        "Qty": r["quantity"],
        "Cost ₨": r["cost_price"],
        "Total ₨": r["total"],
        "Note": r.get("note", ""),
    } for r in rows])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.metric("Total Spent", f"₨{df['Total ₨'].sum():,.0f}")
