from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- DATABASE CONFIGURATION ---
# This connects your Railway backend to your Aiven MySQL cloud instance.
# Replace the placeholders below with the 'Service URI' from your Aiven Console.
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_6V_eQO8zN7X_z2R4K_q@mysql-246e6a1d-hanzala-bead-textile.l.aivencloud.com:21359/defaultdb"

# Create the SQLAlchemy engine
# 'pool_recycle' and 'pool_pre_ping' help maintain the connection in a cloud environment
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_recycle=3600, 
    pool_pre_ping=True
)

# Create a SessionLocal class for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from
Base = declarative_base()