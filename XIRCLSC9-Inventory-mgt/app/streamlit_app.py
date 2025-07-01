import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go

# 🔧 Configuration
API_BASE_URL = "http://127.0.0.1:8000"  # Update this to your FastAPI server URL

# 🎨 Page Configuration
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        padding: 0.5rem;
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-message {
        padding: 0.5rem;
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 🔧 Helper Functions
def make_api_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """Make API request to FastAPI backend"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"API Error: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Error: Unable to connect to API server"}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}

def display_success(message: str):
    """Display success message"""
    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)

def display_error(message: str):
    """Display error message"""
    st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)

# 📊 Dashboard Functions
def show_dashboard():
    """Display dashboard with key metrics and charts"""
    st.markdown('<h1 class="main-header">📊 Inventory Management Dashboard</h1>', unsafe_allow_html=True)
    
    # Fetch data
    items_response = make_api_request("GET", "/inventory/items/")
    categories_response = make_api_request("GET", "/inventory/categories/")
    suppliers_response = make_api_request("GET", "/inventory/suppliers/")
    
    if not items_response["success"]:
        display_error("Unable to load dashboard data")
        return
    
    items = items_response["data"]
    categories = categories_response["data"] if categories_response["success"] else []
    suppliers = suppliers_response["data"] if suppliers_response["success"] else []
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Items", len(items))
    
    with col2:
        total_quantity = sum(item["quantity"] for item in items)
        st.metric("Total Stock", total_quantity)
    
    with col3:
        total_value = sum(item["quantity"] * item["price"] for item in items)
        st.metric("Total Value", f"₹{total_value:,.2f}")
    
    with col4:
        low_stock_items = [item for item in items if item["quantity"] < 10]
        st.metric("Low Stock Items", len(low_stock_items), delta=f"-{len(low_stock_items)}")
    
    # Charts
    if items:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Stock Quantity by Item")
            df_items = pd.DataFrame(items)
            fig = px.bar(df_items.head(10), x="name", y="quantity", 
                        title="Top 10 Items by Quantity")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💰 Value Distribution")
            df_items["total_value"] = df_items["quantity"] * df_items["price"]
            fig = px.pie(df_items.head(10), values="total_value", names="name",
                        title="Top 10 Items by Value")
            st.plotly_chart(fig, use_container_width=True)
        
        # Low Stock Alert
        if low_stock_items:
            st.subheader("⚠️ Low Stock Alert")
            df_low_stock = pd.DataFrame(low_stock_items)
            st.dataframe(df_low_stock[["name", "quantity", "price"]], use_container_width=True)

# 📦 Items Management
def show_items():
    """Display items management interface"""
    st.markdown('<h1 class="main-header">📦 Items Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 View Items", "➕ Add Item", "✏️ Edit Item"])
    
    with tab1:
        st.subheader("Current Inventory Items")
        response = make_api_request("GET", "/inventory/items/")
        
        if response["success"]:
            items = response["data"]
            if items:
                df = pd.DataFrame(items)
                st.dataframe(df, use_container_width=True)
                
                # Item details
                if st.checkbox("Show Item Details"):
                    selected_item = st.selectbox("Select Item", 
                                               options=[f"{item['id']} - {item['name']}" for item in items])
                    if selected_item:
                        item_id = int(selected_item.split(" - ")[0])
                        item_detail = make_api_request("GET", f"/inventory/items/{item_id}")
                        if item_detail["success"]:
                            item = item_detail["data"]
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**Name:**", item["name"])
                                st.write("**Description:**", item.get("description", "N/A"))
                                st.write("**Quantity:**", item["quantity"])
                                st.write("**Price:**", f"${item['price']:.2f}")
                            with col2:
                                st.write("**Category ID:**", item["category_id"])
                                st.write("**Supplier ID:**", item["supplier_id"])
                                st.write("**Created:**", item["created_at"])
                                st.write("**Updated:**", item["updated_at"])
            else:
                st.info("No items found in inventory")
        else:
            display_error(response["error"])
    
    with tab2:
        st.subheader("Add New Item")
        
        # Get categories and suppliers for dropdowns
        categories_response = make_api_request("GET", "/inventory/categories/")
        suppliers_response = make_api_request("GET", "/inventory/suppliers/")
        
        categories = categories_response["data"] if categories_response["success"] else []
        suppliers = suppliers_response["data"] if suppliers_response["success"] else []
        
        with st.form("add_item_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Item Name*", placeholder="Enter item name")
                description = st.text_area("Description", placeholder="Optional description")
                quantity = st.number_input("Quantity*", min_value=0, value=0)
            
            with col2:
                price = st.number_input("Price*", min_value=0.0, value=0.0, format="%.2f")
                
                if categories:
                    category_options = {f"{cat['id']} - {cat['name']}": cat['id'] for cat in categories}
                    selected_category = st.selectbox("Category*", options=list(category_options.keys()))
                    category_id = category_options[selected_category]
                else:
                    st.warning("No categories available. Please add categories first.")
                    category_id = st.number_input("Category ID*", min_value=1, value=1)
                
                if suppliers:
                    supplier_options = {f"{sup['id']} - {sup['name']}": sup['id'] for sup in suppliers}
                    selected_supplier = st.selectbox("Supplier*", options=list(supplier_options.keys()))
                    supplier_id = supplier_options[selected_supplier]
                else:
                    st.warning("No suppliers available. Please add suppliers first.")
                    supplier_id = st.number_input("Supplier ID*", min_value=1, value=1)
            
            submitted = st.form_submit_button("Add Item", type="primary")
            
            if submitted:
                if name and quantity >= 0 and price >= 0:
                    item_data = {
                        "name": name,
                        "description": description,
                        "quantity": quantity,
                        "price": price,
                        "category_id": category_id,
                        "supplier_id": supplier_id
                    }
                    
                    response = make_api_request("POST", "/inventory/items/", item_data)
                    if response["success"]:
                        display_success("Item added successfully!")
                        st.rerun()
                    else:
                        display_error(response["error"])
                else:
                    display_error("Please fill in all required fields")
    
    with tab3:
        st.subheader("Edit Item")
        
        # Get items for selection
        items_response = make_api_request("GET", "/inventory/items/")
        if items_response["success"]:
            items = items_response["data"]
            if items:
                item_options = {f"{item['id']} - {item['name']}": item for item in items}
                selected_item_key = st.selectbox("Select Item to Edit", options=list(item_options.keys()))
                
                if selected_item_key:
                    selected_item = item_options[selected_item_key]
                    
                    with st.form("edit_item_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            name = st.text_input("Item Name", value=selected_item["name"])
                            description = st.text_area("Description", value=selected_item.get("description", ""))
                            quantity = st.number_input("Quantity", value=selected_item["quantity"])
                        
                        with col2:
                            price = st.number_input("Price", value=selected_item["price"], format="%.2f")
                            category_id = st.number_input("Category ID", value=selected_item["category_id"])
                            supplier_id = st.number_input("Supplier ID", value=selected_item["supplier_id"])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            update_submitted = st.form_submit_button("Update Item", type="primary")
                        with col2:
                            delete_submitted = st.form_submit_button("Delete Item", type="secondary")
                        
                        if update_submitted:
                            item_data = {
                                "name": name,
                                "description": description,
                                "quantity": quantity,
                                "price": price,
                                "category_id": category_id,
                                "supplier_id": supplier_id
                            }
                            
                            response = make_api_request("PUT", f"/inventory/items/{selected_item['id']}", item_data)
                            if response["success"]:
                                display_success("Item updated successfully!")
                                st.rerun()
                            else:
                                display_error(response["error"])
                        
                        if delete_submitted:
                            if st.session_state.get("confirm_delete", False):
                                response = make_api_request("DELETE", f"/inventory/items/{selected_item['id']}")
                                if response["success"]:
                                    display_success("Item deleted successfully!")
                                    st.session_state["confirm_delete"] = False
                                    st.rerun()
                                else:
                                    display_error(response["error"])
                            else:
                                st.session_state["confirm_delete"] = True
                                st.warning("Click Delete again to confirm deletion")
            else:
                st.info("No items available to edit")

# 🏷️ Categories Management
def show_categories():
    """Display categories management interface"""
    st.markdown('<h1 class="main-header">🏷️ Categories Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View Categories", "➕ Add Category"])
    
    with tab1:
        st.subheader("Current Categories")
        response = make_api_request("GET", "/inventory/categories/")
        
        if response["success"]:
            categories = response["data"]
            if categories:
                df = pd.DataFrame(categories)
                st.dataframe(df, use_container_width=True)
                
                # Category details
                if st.checkbox("Show Category Details"):
                    selected_category = st.selectbox("Select Category", 
                                                   options=[f"{cat['id']} - {cat['name']}" for cat in categories])
                    if selected_category:
                        cat_id = int(selected_category.split(" - ")[0])
                        cat_detail = make_api_request("GET", f"/inventory/categories/{cat_id}")
                        if cat_detail["success"]:
                            cat = cat_detail["data"]
                            st.write("**Name:**", cat["name"])
                            st.write("**Description:**", cat.get("description", "N/A"))
            else:
                st.info("No categories found")
        else:
            display_error(response["error"])
    
    with tab2:
        st.subheader("Add New Category")
        
        with st.form("add_category_form"):
            name = st.text_input("Category Name*", placeholder="Enter category name")
            description = st.text_area("Description", placeholder="Optional description")
            
            submitted = st.form_submit_button("Add Category", type="primary")
            
            if submitted:
                if name:
                    category_data = {
                        "name": name,
                        "description": description
                    }
                    
                    response = make_api_request("POST", "/inventory/categories/", category_data)
                    if response["success"]:
                        display_success("Category added successfully!")
                        st.rerun()
                    else:
                        display_error(response["error"])
                else:
                    display_error("Please enter a category name")

# 🚚 Suppliers Management
def show_suppliers():
    """Display suppliers management interface"""
    st.markdown('<h1 class="main-header">🚚 Suppliers Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 View Suppliers", "➕ Add Supplier"])
    
    with tab1:
        st.subheader("Current Suppliers")
        response = make_api_request("GET", "/inventory/suppliers/")
        
        if response["success"]:
            suppliers = response["data"]
            if suppliers:
                df = pd.DataFrame(suppliers)
                st.dataframe(df, use_container_width=True)
                
                # Supplier details
                if st.checkbox("Show Supplier Details"):
                    selected_supplier = st.selectbox("Select Supplier", 
                                                   options=[f"{sup['id']} - {sup['name']}" for sup in suppliers])
                    if selected_supplier:
                        sup_id = int(selected_supplier.split(" - ")[0])
                        sup_detail = make_api_request("GET", f"/inventory/suppliers/{sup_id}")
                        if sup_detail["success"]:
                            sup = sup_detail["data"]
                            st.write("**Name:**", sup["name"])
                            st.write("**Contact Info:**", sup.get("contact_info", "N/A"))
                            st.write("**Address:**", sup.get("address", "N/A"))
            else:
                st.info("No suppliers found")
        else:
            display_error(response["error"])
    
    with tab2:
        st.subheader("Add New Supplier")
        
        with st.form("add_supplier_form"):
            name = st.text_input("Supplier Name*", placeholder="Enter supplier name")
            contact_info = st.text_input("Contact Info", placeholder="Phone/Email")
            address = st.text_area("Address", placeholder="Full address")
            
            submitted = st.form_submit_button("Add Supplier", type="primary")
            
            if submitted:
                if name:
                    supplier_data = {
                        "name": name,
                        "contact_info": contact_info,
                        "address": address
                    }
                    
                    response = make_api_request("POST", "/inventory/suppliers/", supplier_data)
                    if response["success"]:
                        display_success("Supplier added successfully!")
                        st.rerun()
                    else:
                        display_error(response["error"])
                else:
                    display_error("Please enter a supplier name")

# 📊 Reports
def show_reports():
    """Display reports and analytics"""
    st.markdown('<h1 class="main-header">📊 Reports & Analytics</h1>', unsafe_allow_html=True)
    
    # Get all data
    items_response = make_api_request("GET", "/inventory/items/")
    
    if not items_response["success"]:
        display_error("Unable to load reports data")
        return
    
    items = items_response["data"]
    
    if not items:
        st.info("No data available for reports")
        return
    
    df = pd.DataFrame(items)
    df["total_value"] = df["quantity"] * df["price"]
    
    # Report tabs
    tab1, tab2, tab3 = st.tabs(["📈 Stock Analysis", "💰 Value Analysis", "⚠️ Alerts"])
    
    with tab1:
        st.subheader("Stock Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Stock distribution
            fig = px.histogram(df, x="quantity", nbins=20, title="Stock Quantity Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top items by stock
            top_stock = df.nlargest(10, "quantity")
            fig = px.bar(top_stock, x="name", y="quantity", title="Top 10 Items by Stock")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Value Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Value distribution
            fig = px.histogram(df, x="total_value", nbins=20, title="Item Value Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Price vs Quantity scatter
            fig = px.scatter(df, x="quantity", y="price", size="total_value", 
                           hover_data=["name"], title="Price vs Quantity")
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Price", f"${df['price'].mean():.2f}")
        with col2:
            st.metric("Average Quantity", f"{df['quantity'].mean():.0f}")
        with col3:
            st.metric("Total Items", len(df))
        with col4:
            st.metric("Total Value", f"${df['total_value'].sum():,.2f}")
    
    with tab3:
        st.subheader("Inventory Alerts")
        
        # Low stock items
        low_stock = df[df["quantity"] < 10]
        if not low_stock.empty:
            st.warning(f"⚠️ {len(low_stock)} items have low stock (< 10 units)")
            st.dataframe(low_stock[["name", "quantity", "price", "total_value"]], use_container_width=True)
        else:
            st.success("✅ All items have adequate stock levels")
        
        # High value items
        st.subheader("High Value Items (Top 10%)")
        high_value_threshold = df["total_value"].quantile(0.9)
        high_value_items = df[df["total_value"] >= high_value_threshold]
        if not high_value_items.empty:
            st.dataframe(high_value_items[["name", "quantity", "price", "total_value"]], use_container_width=True)

# 🎛️ Main App
def main():
    """Main application function"""
    # Sidebar navigation
    st.sidebar.title("📦 Inventory System")
    st.sidebar.markdown("---")
    
    # Navigation menu
    pages = {
        "📊 Dashboard": show_dashboard,
        "📦 Items": show_items,
        "🏷️ Categories": show_categories,
        "🚚 Suppliers": show_suppliers,
        "📊 Reports": show_reports
    }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    
    # API Configuration
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ API Configuration")
    new_api_url = st.sidebar.text_input("API Base URL", value=API_BASE_URL)
    
    if new_api_url != API_BASE_URL:
        globals()["API_BASE_URL"] = new_api_url
        st.sidebar.success("API URL updated!")
    
    # Connection status
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔌 Connection Status")
    
    # Test API connection
    test_response = make_api_request("GET", "/inventory/items/")
    if test_response["success"]:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Disconnected")
        st.sidebar.caption(test_response["error"])
    
    # Display selected page
    pages[selected_page]()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        "Inventory Management System | Built with Streamlit & FastAPI"
        "</div>", 
        unsafe_allow_html=True
    )

# 🚀 Run the app
if __name__ == "__main__":
    main()