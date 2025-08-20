from typing import Optional
from pydantic import BaseModel

class Pant_Category_Schema(BaseModel):
    category: str
    pant_size: int
    pant_colour: str
    pant_price: float
    product_id: str 
    quantity: int 
    image: Optional[str]= None

class Shirt_Category_Schema(BaseModel):
    category: str
    shirt_size: int
    shirt_colour: str
    shirt_price: float
    product_id: str 
    quantity: int 
    image: Optional[str]= None

class Category_filter(BaseModel):
    category: str = None
    shirt_size: int = None
    shirt_colour: str = None
    shirt_price: float = None
    product_id: str = None
    quantity: int = None
    pant_size: int = None
    pant_colour: str = None
    pant_price: float = None
