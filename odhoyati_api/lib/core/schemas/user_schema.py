from typing import Optional
from pydantic import BaseModel, Field


from datetime import datetime

class UserSchema(BaseModel):
    name: str = Field(..., description="the full name of the user")
    location: str = Field(..., description="the city user lives in")
    address: str = Field(None, description="descriptive address of the user")
    phone_number: str = Field(..., description="phone number of the user")
    password: str = Field(..., description="password of the user")
    notification_token: str = Field(None, description="notification token of the user")
    is_verified: bool = Field(False, description="status of the user account")
    is_active: bool = Field(True, description="status of the user account")
    user_type: str = "user"
    created_at: str = Field(datetime.utcnow(), description="date and time of user creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of user update")
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mostafa Mahmoud",
                "location": "Cairo",
                "address": "21 Main Street, Cairo",
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789",
                "is_verified": True,
                "is_active": True,
                "type": "user",
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
        

class UserLoginModel(BaseModel):
    phone_number: str
    password: str
    notification_token: Optional[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789"
            }
        }

class UpdateUserModel(BaseModel):
    name: Optional[str]
    location: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    password: Optional[str]
    notification_token: Optional[str]
    is_verified: Optional[bool] = True
    is_active: Optional[bool] = True
    updated_at: str = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mostafa Mahmoud",
                "location": "Cairo",
                "address": "21 Main Street, Cairo",
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789",
                "is_verified": True,
                "is_active": True,
                "type": "user",
                "updated_at": "2022-01-01 00:00:00"
            }
        }