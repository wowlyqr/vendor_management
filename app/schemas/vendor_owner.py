from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

class Vendor_owner_Schema(BaseModel):
    name: str
    gender: Literal['Male', 'Female', 'Others']
    password: str 
    email: EmailStr
    brand_name: str
    address: str
    store_address:Optional[str] = None 
    pincode: int
    mobile: int
    dob: Optional[str] = None 
    country_code: int
    gst : Optional[str] = None 



class Update_Vendor_owner_Schema(BaseModel):
    gender:Optional[Literal['Male', 'Female', 'Others']]
    name: Optional[str]
    address:Optional [str]
    pincode: Optional[str]
    dob: Optional[str]

class Vendor_owner_filter(BaseModel):
    name: str = None
    gender: str = None   
    email: str = None
    brand_name:str = None
    address:str = None
    pincode:str = None
    mobile: int = None
    dob: str = None 
    country_code: int = None
