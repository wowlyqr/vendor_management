from typing import  Literal, Optional
from pydantic import BaseModel

class Order_Tracking_Schema(BaseModel):
    order_id: str
    status :Literal["order placed", "confirmed","dispatched","delivered"]
    description: Optional[str] = None
   