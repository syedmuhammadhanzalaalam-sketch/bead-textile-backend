import os
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

# Import your local database and models files
import models
import database
from database import engine

# Create the database tables in MySQL automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeadsTextile Business Intelligence API")

# 🛠️ 1. SETUP CORS
# This allows your Admin Portal (5173) and Dashboard (5174) to communicate with this API
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🖼️ 2. SETUP IMAGE STORAGE
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# This mounts the folder so your browser can see images at http://localhost:8000/uploads/filename.jpg
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 🚀 3. POST ROUTE: Add Product with Multiple Images
@app.post("/products")
async def create_product(
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    cost: float = Form(...),
    images: List[UploadFile] = File(None), # Accepts multiple files
    db: Session = Depends(database.get_db)
):
    try:
        image_urls = []
        if images:
            for image in images:
                # Create a safe file path
                file_path = os.path.join(UPLOAD_DIR, image.filename)
                with open(file_path, "wb") as buffer:
                    content = await image.read()
                    buffer.write(content)
                # Build the URL that the frontend will use to display the image
                image_urls.append(f"http://127.0.0.1:8000/uploads/{image.filename}")

        # Join multiple URLs into a single string separated by commas
        image_string = ",".join(image_urls)

        new_product = models.Product(
            name=name,
            category=category,
            price=price,
            stock_quantity=stock,
            material_cost=cost,
            image_url=image_string 
        )
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {"status": "success", "product_id": new_product.id}
    
    except Exception as e:
        print(f"Detailed Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 📊 4. GET ROUTE: Fetch all data for the Management Dashboard
@app.get("/products")
def get_products(db: Session = Depends(database.get_db)):
    # This sends the full list to your dashboard for quantity & profit tracking
    return db.query(models.Product).all()

# 🗑️ 5. DELETE ROUTE: Remove an article
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"status": "deleted"}