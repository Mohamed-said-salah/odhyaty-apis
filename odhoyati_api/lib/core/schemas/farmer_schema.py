from typing import Optional, List
from pydantic import BaseModel, Field


from datetime import datetime

class FarmerSchema(BaseModel):
    name: str = Field(..., description="the full name of the user")
    bio: str = Field(None, description="the full name of the user")
    location: str = Field(..., description="the city user lives in")
    address: str = Field(None, description="descriptive address of the user")
    phone_number: str = Field(..., description="phone number of the user")
    password: str = Field(..., description="password of the user")
    notification_token: str = Field(None, description="notification token of the farmer")
    image: str = Field(None, description="password of the user")
    user_type: str =  Field("farmer", description="descriptive address of the user")
    has_slaughtering: bool = Field(False, description="status of slaughtering")
    has_delivering: bool = Field(False, description="status of delivering")
    work_hours: dict = Field({"start": "27-01-2022 06:00:00+00:00", "end": "27-01-2022 17:00:00+00:00"}, description="The hour farmer works on")
    work_days : List[int] = Field(..., description="The days farmer works on from 1 to 7")
    is_verified: bool = Field(False, description="status of the user account")
    is_active: bool = Field(True, description="status of the user account")
    created_at: str = Field(datetime.utcnow(), description="date and time of user creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of user update")
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mostafa Mahmoud",
                "bio": "I am a farmer",
                "location": "Cairo",
                "address": "21 Main Street, Cairo",
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789",
                "image": "https://example.com/image.png",
                "user_type": "farmer",
                "has_slaughtering": True,
                "has_delivering": True,
                "work_hours": {
                    "start": "27-01-2022 06:00:00+00:00",
                    "end": "27-01-2022 17:00:00+00:00"
                    },
                "work_days": [7,1,2,3,4],
                "is_verified": True,
                "is_active": True,
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
        

class FarmerLoginModel(BaseModel):
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

class UpdateFarmerModel(BaseModel):
    name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    password: Optional[str]
    notification_token: Optional[str]
    image: Optional[str]
    user_type: Optional[str] = "farmer"
    has_slaughtering: Optional[bool] = False
    has_delivering: Optional[bool] = False
    work_hours: Optional[dict] = {"start": "27-01-2022 06:00:00+00:00", "end": "27-01-2022 17:00:00+00:00"}
    work_days: Optional[List[int]] = [7,1,2,3,4]
    is_verified: Optional[bool] = True
    is_active: Optional[bool] = True
    updated_at: str = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mostafa Mahmoud",
                "bio": "I am a farmer",
                "location": "Cairo",
                "address": "21 Main Street, Cairo",
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789",
                "image": "https://example.com/image.png",
                "user_type": "farmer",
                "has_slaughtering": True,
                "has_delivering": True,
                "work_hours": {
                    "start": "27-01-2022 06:00:00+00:00",
                    "end": "27-01-2022 17:00:00+00:00"
                    },
                "work_days": [7,1,2,3,4],
                "is_verified": True,
                "is_active": True,
                "type": "farmer",
                "updated_at": "2022-01-01 00:00:00"
            }
        }