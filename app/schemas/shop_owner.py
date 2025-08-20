from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class Shop_owner_Schema(BaseModel):
    name: str
    gender: Literal['Male', 'Female', 'Others']
    password: str 
    aadhar_number :Optional[str] = None
    email: EmailStr    
    mobile: int
    country_code: int
    shop_id: str
    vendor_id: str

class Update_shop_owner_Schema(BaseModel):
    name: Optional[str]
    gender: Optional[Literal['Male', 'Female', 'Others']]

class Shop_owner_filter(BaseModel):
    name: str = None
    gender: str = None  
    email: str = None
    mobile: int = None
    country_code: int = None
    shop_id: str = None
