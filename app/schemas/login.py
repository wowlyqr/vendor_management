from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    password: str
    email: EmailStr 
