from pydantic import BaseModel
from typing import Optional

# This defines what a Product looks like in your API
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    material_cost: float
    image_url: Optional[str] = None

# This is used when creating a new product (the "Product Add Portal")
class ProductCreate(ProductBase):
    pass

# This is used when reading data (the "Management Portal")
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True