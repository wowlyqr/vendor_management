from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Credentials_Schema(BaseModel):    
    createdAt: datetime = Field(default=datetime.utcnow)
    password: str 
    email: EmailStr
    user_type: str    
    user_id: str    
    mobile: int
    update_password: bool = Field(default=False)
    country_code: int