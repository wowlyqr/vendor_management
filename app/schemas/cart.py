from typing import Optional
from pydantic import BaseModel

class Cart_Schema(BaseModel):   
    product_id: str 
    product_name: str 
    category: str 
    price: float 
    selected_product_details:list
    shop_owner_id:str


class Cart_filter(BaseModel):
    product_id: str = None
    product_name: str  = None
    category: str = None
    price: float    = None
    shop_owner_id:str = None