from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Shop_Schema(BaseModel):
    shop_name: str
    shop_unique_id: str
    expected_open_date:Optional[str] = None
    vendor_owner_id: str
    address: str
    city: str
    state: str
    pincode: int  

class Update_shop_Schema(BaseModel):
    shop_name:Optional[str]
    address: Optional[str]
    pincode: Optional[int]  

class Shop_filter(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    shop_name: str = None
    vendor_owner_id: str = None
    address: str = None
    pincode: int  = None 