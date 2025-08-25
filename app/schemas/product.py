from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Product_Schema(BaseModel):
    name: str
    product_unique_id: str
    image: Optional[str] = None
    category: str  
    vendor_owner_id:str    
    price: Optional[str] = None
    description: Optional[str] = None
    available_sizes : Optional[str] = None
    available_colors : Optional[str] = None
    available_quantity : Optional[str] = None

class Product_filter(BaseModel):
    name: str  = None
    product_unique_id: str  = None
    category:str  = None
    vendor_owner_id:str  = None
    price: str  = None
    available_sizes : str  = None
    available_colors : str  = None
    available_quantity :str  = None

