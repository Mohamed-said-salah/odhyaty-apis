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