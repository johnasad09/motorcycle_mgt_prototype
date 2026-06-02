import streamlit as st
import pandas as pd
from datetime import date, timedelta
from database import get_financials, get_parts

def show():
    st.header("📊 Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("From", date.today() - timedelta(days=30))
    with col2:
        end = st.date_input("To", date.today())

    data = get_financials(start.isoformat(), (end + timedelta(days=1)).isoformat())

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Total Revenue", f"₨{data['total_revenue']:,.0f}")
    c2.metric("🛒 Total Spent", f"₨{data['total_spent']:,.0f}")
    profit_color = "normal" if data["profit"] >= 0 else "inverse"
    c3.metric("📈 Net Profit", f"₨{data['profit']:,.0f}", delta=f"₨{data['profit']:,.0f}", delta_color=profit_color)

    st.divider()

    # Sales trend
    if data["sales"]:
        sales_df = pd.DataFrame(data["sales"])
        sales_df["date"] = pd.to_datetime(sales_df["created_at"]).dt.date
        daily = sales_df.groupby("date")["total"].sum().reset_index()
        st.subheader("Sales Trend")
        st.bar_chart(daily.set_index("date")["total"])

    # Low stock alert
    parts = get_parts()
    low = [p for p in parts if p["quantity"] <= 5]
    if low:
        st.subheader("⚠️ Low Stock Alert")
        st.dataframe(pd.DataFrame(low)[["part_id", "name", "quantity"]], width='stretch', hide_index=True)
