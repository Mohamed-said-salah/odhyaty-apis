

from typing import Optional
from pydantic import BaseModel, Field


from datetime import datetime

class ReviewSchema(BaseModel):
    user_id: str = Field(..., description="the id of the user gave the review") # user who gave the review
    farmer_id: str = Field(..., description="the id of the farmer user reviewed") # farmer user received the review
    item_id: str = Field(..., description="the id of the item user gave the review after confirming buying it") # item which the user gave the review on
    order_id: str = Field(..., description="the id of the order the order user gave the id after completing it") # order which the user gave the review on
    # title # description # category # weight # gender # pricePerKilo # age # is_slaughtering # is_delivering # image
    part_of_user: Optional[dict] = {} # image and name
    part_of_farmer: Optional[dict] = {} # image and name
    part_of_item: Optional[dict] = {} # image , title and category
    rate: int = Field(..., description="the rate of the user on the item")
    review: Optional[str] = None
    created_at: str = Field(datetime.utcnow(), description="date and time of order creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of order update")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123456789",
                "farmer_id": "123456789",
                "item_id": "123456789",
                "order_id": "123456789",
                "part_of_user": {
                    "image": "https://example.com/image.png",
                    "name": "User Name"
                },
                "part_of_farmer": {
                    "image": "https://example.com/image.png",
                    "name": "Farmer Name"
                },
                "part_of_item": {
                    "image": "https://example.com/image.png",
                    "title": "Item Title",
                    "category": "CAMEL"
                },
                "rate": 5,
                "review": "Good item",
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
        


class UpdateReviewModel(BaseModel):
    rate: Optional[int]
    review: Optional[str]
    updated_at: str = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "rate": 5,
                "review": "Good item",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
        
        