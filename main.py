from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Ensure these files exist in your folder
import models
import schemas
import database

app = FastAPI(title="BEAD TEXTILE API")

# --- CORS SETTINGS ---
# Using ["*"] allows your local frontend to talk to your cloud backend without security blocks
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
def read_root():
    return {"message": "Welcome to BEAD TEXTILE API - Cloud Edition"}

# Get all products for the Management Portal
@app.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

# Add a new product from the Product Add Portal
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product