from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Clean URL without the extra ssl parameters at the end
DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_7IzoHwht5lpCN-IR042@bead-textile-db-bead-textile-project.h.aivencloud.com:24399/defaultdb"

# 2. Create the Engine with explicit SSL instructions in connect_args
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {}}, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()