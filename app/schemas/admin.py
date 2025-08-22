from pydantic import BaseModel, EmailStr
from typing import  Literal

class Admin_Schema(BaseModel):
    name: str
    gender: Literal['Male', 'Female', 'Others']
    password: str 
    email: EmailStr    
    mobile: int
    country_code: int  
