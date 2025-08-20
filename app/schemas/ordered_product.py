from typing import  Optional
from pydantic import BaseModel

class Ordered_product_Schema(BaseModel):  
     
    product_id :str   
    product_name: str
    category: str
    product_image: Optional[str] =None
    selected_product_details:list
    order_id:str   
    product_amount :float
    product_quantity :int   