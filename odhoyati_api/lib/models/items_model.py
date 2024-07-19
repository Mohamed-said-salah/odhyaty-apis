# import base model
from pydantic import BaseModel

# import datetime
from datetime import datetime

# Create item model
class Item(BaseModel):
    # image url
    image_url: str = None
    # category
    category: str = None
    # weight
    weight: int = 0
    # gender
    gender: str = None
    # age
    age: int = None
    # price
    price: float = None
    # price per kg / float or optional / equal price over weight
    price_per_kg: float = None
    # is_odhoia
    is_odohia: bool = False
    # is_slaughtering avilability
    is_slaughtering: bool = False
    # is_delivering
    is_delivering: bool = False
    # description
    description: str = None
    # created_at time equals to current time by default
    created_at: str = datetime.now(datetime.UTC)
    
    # categories are cow / buffalo / goat / sheep / camel
    # validation for category that is in the list
    class Config:
        schema_extra = {
            "example": {
                "image_url": "https://example.com/image.png",
                "category": "cow",
                "weight": 100,
                "gender": "male",
                "age": 10,
                "price": 1000.0,
                "price_per_kg": 10.0,
                "is_odohia": True,
                "is_slaughtering": True,
                "is_delivering": True,
                "description": "description",
                "created_at": "2022-01-01 00:00:00"
            }
        }
