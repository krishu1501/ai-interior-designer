from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    title: str
    url: str
    image: str
    price: str
    rating: str = ""
    reviews_count: str = ""
    mrp: str = ""
    discount: str = ""
    delivery_date: str = ""

class ProductSuggestion(BaseModel):
    oldProduct: Optional[str]
    newProduct: str
    amazonDetails: Optional[Product]

class RoomDesignResponse(BaseModel):
    suggestions: List[ProductSuggestion]
    newImage: str  # Base64 encoded image
