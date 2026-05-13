from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Set up logging to catch connection errors in Railway logs
logger = logging.getLogger(__name__)

# --- DATABASE CONFIGURATION ---
# Ensure this URI is copied exactly from your Aiven 'Service URI' field.
# It should look like: mysql+pymysql://avnadmin:password@host:port/defaultdb
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_6V_eQO8zN7X_z2R4K_q@mysql-246e6a1d-hanzala-bead-textile.l.aivencloud.com:21359/defaultdb"

try:
    # pool_recycle: Closes connections older than 1 hour to prevent 'Server has gone away' errors.
    # pool_pre_ping: Checks if the connection is alive before sending a query.
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        pool_recycle=3600, 
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
except Exception as e:
    logger.error(f"Failed to initialize SQLAlchemy engine: {e}")