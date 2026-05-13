import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Import your local files
# If you get an 'ImportError', change these to: from . import models, schemas, database
import models
import schemas
import database

# --- LOGGING SETUP ---
# This ensures we see the real errors in your Railway "Deploy Logs"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BEAD TEXTILE API")

# --- CORS SETTINGS ---
# Using ["*"] is the safest way to ensure your local dashboard can connect to the cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/")
def health_check():
    """Route to verify the server is live"""
    return {
        "status": "online", 
        "brand": "BEAD TEXTILE",
        "database": "connected"
    }

@app.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    try:
        products = db.query(models.Product).all()
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))