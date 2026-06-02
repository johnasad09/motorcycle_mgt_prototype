import streamlit as st
import pandas as pd
from database import get_financials
from datetime import date, timedelta

def show():
    st.header("📑 Profit & Loss Statement")

    c1, c2 = st.columns(2)
    start = c1.date_input("From", date.today().replace(day=1))
    end = c2.date_input("To", date.today())

    data = get_financials(start.isoformat(), (end + timedelta(days=1)).isoformat())

    st.subheader("Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"₨{data['total_revenue']:,.0f}")
    c2.metric("Total Cost (Purchases)", f"₨{data['total_spent']:,.0f}")
    profit = data["profit"]
    c3.metric("Net Profit / Loss", f"₨{profit:,.0f}", delta=f"₨{profit:,.0f}", delta_color="normal" if profit >= 0 else "inverse")

    st.divider()
    tab1, tab2 = st.tabs(["Sales Ledger", "Purchase Ledger"])

    with tab1:
        if data["sales"]:
            df = pd.DataFrame([{
                "Date": r["created_at"][:10],
                "Customer": r["customers"]["name"],
                "Part": r["parts"]["name"],
                "Qty": r["quantity"],
                "Rate ₨": r["sale_price"],
                "Amount ₨": r["total"],
            } for r in data["sales"]])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"**Total: ₨{df['Amount ₨'].sum():,.0f}**")
        else:
            st.info("No sales in this period.")

    with tab2:
        if data["purchases"]:
            df = pd.DataFrame([{
                "Date": r["created_at"][:10],
                "Vendor": r["vendors"]["name"],
                "Part": r["parts"]["name"],
                "Qty": r["quantity"],
                "Rate ₨": r["cost_price"],
                "Amount ₨": r["total"],
            } for r in data["purchases"]])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"**Total: ₨{df['Amount ₨'].sum():,.0f}**")
        else:
            st.info("No purchases in this period.")
