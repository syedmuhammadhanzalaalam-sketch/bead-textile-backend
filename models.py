from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from database import Base

# 1. Product Table: Updated for Luxury Image Support
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    category = Column(String(100))        # Pearl Bag, Jewelry, etc.
    price = Column(Float)                 # Selling Price
    stock_quantity = Column(Integer)
    material_cost = Column(Float)         # Cost to make/buy
    image_url = Column(Text)              # <--- ADD THIS: Stores paths to your photos

# 2. Order Table: Tracks every single sale
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    total_revenue = Column(Float)
    total_profit = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# 3. Expense Table: Tracks non-product costs
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    amount = Column(Float)
    category = Column(String(100))
    date = Column(DateTime, default=datetime.utcnow)