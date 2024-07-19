from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from bson import ObjectId

# create mongo db schema from item model


class Item(BaseModel):
    image_url: str = Field(...)
    category: str = Field(...)
    weight: int = Field(...)
    gender: str = Field(...)
    age: int = Field(...)
    price: float = Field(...)
    price_per_kg: float = Field(...)
    is_odohia: bool = Field(...)
    is_slaughtering: bool = Field(...)
    is_delivering: bool = Field(...)
    description: str = Field(...)
    created_at: str = Field(...)

    class Config:
        allow_population_by_field_name = True    # allow populating by field name
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    class Collection:
        name = "items"
        
    
    # validation
    @validator("age")
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Age must be positive")
        return v
    
    @validator("price")
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Price must be positive")
        return v
    
    @validator("price_per_kg")
    def price_per_kg_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Price per kg must be positive")
        return v

    # validator for category is in the defined th