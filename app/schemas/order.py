from typing import  Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Order_Schema(BaseModel):
    order_unique_id :str   
    delivery_address: str
    pincode: int
    mobile: int       
    shop_owner_id:str
    vendor_owner_id :str
    total_amount :float
    total_quantity :int
    status:str= Field(default='order placed')
    shop_id:str

class Order_filter(BaseModel):
    category_id: str = None
    product_id :str = None    
    mobile: int = None   
    product_name: str = None   
    shop_owner_id:str =  None
    status:str= None
    shop_id:str = None
    vendor_owner_id :str = None