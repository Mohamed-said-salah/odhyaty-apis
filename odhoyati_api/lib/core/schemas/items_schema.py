from typing import Optional, Union
from pydantic import BaseModel, Field

from datetime import datetime


ItemCatagories = {'cow': "COW", "buffalo": "BUFFALO", 'sheep': "SHEEP", 'goat': "GOAT", 'camel': "CAMEL"}
Gender = {"male": "MALE", "female": "FEMALE"}


class ItemSchema(BaseModel):
    farmer_id: str = Field(..., description="the id of the farmer")
    image: str = Field(None, description="the image of the item")
    title: str = Field(..., description="the title of the item")
    description: str = Field(None, description="the description of the item")
    category: str = Field(..., description="the category of the item")
    weight: Union[int, float] = Field(..., description="the average weight of the items")
    gender: str = Field(..., description="the gender of the item")
    pricePerKilo: float = Field(..., description="the average price per kilo of the item")
    age: Union[int, float] = Field(..., description="the average age of the items")
    quantity: int = Field(..., description="the quantity of the items")
    is_slaughtering: bool = Field(False, description="is slaughtering available at the trader")
    is_delivering: bool = Field(False, description="is delivering available at the trader")
    is_active: bool = Field(True, description="is the item active")
    created_at: str = Field(datetime.utcnow(), description="date and time of item creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of item update")
    
    class Config:
        json_schema_extra = {
            "example": {
                "farmer_id": "123456789",
                "image": "https://example.com/image.png",
                "title": "Item Title",
                "description": "Item Description",
                "category": "CAMEL",
                "weight": 5.0,
                "gender": "MALE",
                "pricePerKilo": 10.0,
                "age": 5.0,
                "quantity": 10,
                "is_slaughtering": True,
                "is_delivering": True,
                "is_active": True,
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00"
            }
        }



class UpdateItemModel(BaseModel):
    image: Optional[str]
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    weight: Optional[Union[int, float]]
    gender: Optional[str]
    pricePerKilo: Optional[float]
    age: Optional[Union[int, float]]
    quantity: Optional[int]
    is_slaughtering: Optional[bool]
    is_delivering: Optional[bool]
    is_active: Optional[bool]
    updated_at: str = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": "https://example.com/image.png",
                "title": "Item Title",
                "description": "Item Description",
                "category": "CAMEL",
                "weight": 5.0,
                "gender": "MALE",
                "pricePerKilo": 10.0,
                "age": 5.0,
                "quantity": 10,
                "is_slaughtering": True,
                "is_delivering": True,
                "is_active": True,
                "updated_at": "2022-01-01 00:00:00"
            }
        }

