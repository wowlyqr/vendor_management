from typing import Optional
from pydantic import BaseModel

class Brand_theme_Schema(BaseModel): 
    theme_color: Optional[str]=None 
    brand_logo:Optional[str]=None
    vendor_owner_id:str
