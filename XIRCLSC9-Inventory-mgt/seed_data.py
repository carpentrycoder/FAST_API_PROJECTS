# seed_data.py
from app.database import SessionLocal
from app import models
from datetime import datetime

db = SessionLocal()

# -------------------------
# 📦 Add Categories
# -------------------------
categories = [
    models.Category(name="Electronics", description="Electronic Items"),
    models.Category(name="Stationery", description="Office supplies and papers"),
    models.Category(name="Furniture", description="Chairs, tables, and desks"),
    models.Category(name="Groceries", description="Daily grocery essentials"),
]
db.add_all(categories)
db.commit()

# -------------------------
# 🚚 Add Suppliers
# -------------------------
suppliers = [
    models.Supplier(name="ABC Corp", contact_info="abc@example.com", address="123 Tech Road"),
    models.Supplier(name="XYZ Traders", contact_info="xyz@example.com", address="45 Market Lane"),
    models.Supplier(name="GlobalTech", contact_info="global@example.com", address="78 Silicon Ave"),
    models.Supplier(name="OfficeNeeds", contact_info="office@example.com", address="23 Stationery St"),
]
db.add_all(suppliers)
db.commit()

# -------------------------
# 📦 Add Items
# -------------------------
items = [
    models.Item(name="Laptop", description="HP EliteBook", quantity=10, price=75000, category_id=1, supplier_id=1),
    models.Item(name="Notebook", description="200 pages", quantity=100, price=30, category_id=2, supplier_id=2),
    models.Item(name="Office Chair", description="Ergonomic", quantity=15, price=4500, category_id=3, supplier_id=3),
    models.Item(name="LED Monitor", description="24 inch full HD", quantity=8, price=12000, category_id=1, supplier_id=3),
    models.Item(name="Pen Pack", description="10 blue pens", quantity=50, price=120, category_id=2, supplier_id=4),
    models.Item(name="Rice Bag", description="10kg Basmati", quantity=25, price=650, category_id=4, supplier_id=2),
]
db.add_all(items)
db.commit()

# -------------------------
# 👥 Add Users
# -------------------------
users = [
    models.User(username="admin", hashed_password="admin123", role="admin"),
    models.User(username="viewer", hashed_password="viewer123", role="viewer"),
]
db.add_all(users)
db.commit()

# -------------------------
# 🔄 Stock Transactions
# -------------------------
transactions = [
    models.StockTransaction(item_id=1, change_type="add", quantity=5, user_id=1, notes="Initial stock"),
    models.StockTransaction(item_id=2, change_type="add", quantity=50, user_id=1, notes="Notebook arrival"),
    models.StockTransaction(item_id=3, change_type="remove", quantity=2, user_id=2, notes="Damaged chairs"),
    models.StockTransaction(item_id=4, change_type="add", quantity=3, user_id=1, notes="New monitor shipment"),
    models.StockTransaction(item_id=5, change_type="adjust", quantity=1, user_id=1, notes="Inventory correction"),
    models.StockTransaction(item_id=6, change_type="remove", quantity=5, user_id=2, notes="Customer purchase"),
]
db.add_all(transactions)
db.commit()

db.close()
print("✅ Seed data inserted successfully!")
