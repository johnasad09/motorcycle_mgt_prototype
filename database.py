import streamlit as st
from supabase import create_client, Client

# cache_resource tells streamlit, run this function once, save the result, 
# and reuse it every time instead of reconnecting repeatedly
@st.cache_resource
def get_db() -> Client:
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# calling the function and using it for every transaction below
db = get_db()

"""
db                    → use the database connection
.table("vendors")     → go to the vendors table
.select("*")          → select ALL columns (* means everything)
.order("name")        → sort results alphabetically by name
.execute()            → actually run this query
.data                 → extract just the results
eq means equals. So .eq("id", id) means "only affect the row where id matches." 
Without this, you'd update or delete every single row — disaster!
"""

# --- Vendors ---
def get_vendors():
    return db.table("vendors").select("*").order("name").execute().data

def add_vendor(name, phone, email, address):
    db.table("vendors").insert({"name": name, "phone": phone, "email": email, "address": address}).execute()

def update_vendor(id, data):
    db.table("vendors").update(data).eq("id", id).execute()

def delete_vendor(id):
    db.table("vendors").delete().eq("id", id).execute()

# --- Customers ---
def get_customers():
    return db.table("customers").select("*").order("name").execute().data

def add_customer(name, phone, email, address):
    db.table("customers").insert({"name": name, "phone": phone, "email": email, "address": address}).execute()

def update_customer(id, data):
    db.table("customers").update(data).eq("id", id).execute()

def delete_customer(id):
    db.table("customers").delete().eq("id", id).execute()

# --- Parts ---
def get_parts():
    return db.table("parts").select("*").order("name").execute().data

def get_part_by_uuid(uuid):
    r = db.table("parts").select("*").eq("id", uuid).execute().data
    return r[0] if r else None

def add_part(part_id, name, description, quantity, per_pack, cost_price, sale_price):
    db.table("parts").insert({
        "part_id": part_id, "name": name, "description": description,
        "quantity": quantity, "per_pack": per_pack,
        "cost_price": cost_price, "sale_price": sale_price
    }).execute()

def update_part(id, data):
    db.table("parts").update(data).eq("id", id).execute()

def delete_part(id):
    db.table("parts").delete().eq("id", id).execute()

# --- Purchases (buy from vendor) ---
def record_purchase(vendor_id, part_id, quantity, cost_price, note):
    db.table("purchases").insert({
        "vendor_id": vendor_id, "part_id": part_id,
        "quantity": quantity, "cost_price": cost_price, "note": note
    }).execute()
    part = get_part_by_uuid(part_id)
    update_part(part_id, {"quantity": part["quantity"] + quantity})

def get_purchases(start=None, end=None):
    q = db.table("purchases").select("*, vendors(name), parts(name, part_id)")
    if start:
        q = q.gte("created_at", start)
    if end:
        q = q.lte("created_at", end)
    return q.order("created_at", desc=True).execute().data

# --- Sales (sell to customer) ---
def record_sale(customer_id, part_id, quantity, sale_price, note):
    part = get_part_by_uuid(part_id)
    if part["quantity"] < quantity:
        raise ValueError(f"Insufficient stock. Available: {part['quantity']}")
    db.table("sales").insert({
        "customer_id": customer_id, "part_id": part_id,
        "quantity": quantity, "sale_price": sale_price, "note": note
    }).execute()
    update_part(part_id, {"quantity": part["quantity"] - quantity})

def get_sales(start=None, end=None):
    q = db.table("sales").select("*, customers(name), parts(name, part_id)")
    if start:
        q = q.gte("created_at", start)
    if end:
        q = q.lte("created_at", end)
    return q.order("created_at", desc=True).execute().data

# --- Financials ---
def get_financials(start=None, end=None):
    purchases = get_purchases(start, end)
    sales = get_sales(start, end)
    total_spent = sum(p["total"] for p in purchases)
    total_revenue = sum(s["total"] for s in sales)
    profit = total_revenue - total_spent
    return {
        "total_spent": total_spent,
        "total_revenue": total_revenue,
        "profit": profit,
        "purchases": purchases,
        "sales": sales,
    }
