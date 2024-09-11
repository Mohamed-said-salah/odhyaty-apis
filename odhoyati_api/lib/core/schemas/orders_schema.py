

from typing import Optional
from pydantic import BaseModel, Field


from datetime import datetime

class OrderSchema(BaseModel):
    user_id: str = Field(..., description="the id of the user")
    farmer_id: str = Field(..., description="the id of the farmer")
    item_id: str = Field(..., description="the id of the item")
    # title # description # category # weight # gender # pricePerKilo # age # is_slaughtering # is_delivering # image
    part_of_the_item: Optional[dict] = {}
    status: str = Field("PENDING", description="the status of the order") # PENDING, COMPLETED, CANCELLED, UNVERIFIED
    created_at: str = Field(datetime.utcnow(), description="date and time of order creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of order update")
    reviewed: Optional[bool] = False
    farmer_sent_notification : Optional[bool] = False
    closed_by: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123456789",
                "farmer_id": "123456789",
                "item_id": "123456789",
                "part_of_the_item": {
                    "image": "https://example.com/image.png",
                    "title": "Item Title",
                    "description": "Item Description",
                    "category": "CAMEL",
                    "weight": 5.0,
                    "gender": "MALE",
                    "pricePerKilo": 10.0,
                    "age": 5.0,
                    "is_slaughtering": True,
                    "is_delivering": True
                },
                "status": "pending",
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00",
                "reviewed": False,
                "farmer_sent_notification": False
            }
        }
        


class UpdateOrderModel(BaseModel):
    status: Optional[str]
    reviewed: Optional[bool]
    updated_at: str = datetime.utcnow()

    class Config:
        json_schema_extra = {
            "example": {
                "status": "pending",
                "reviewed": False,
                "farmer_sent_notification": False,
                "updated_at": "2022-01-01 00:00:00",
            }
        }