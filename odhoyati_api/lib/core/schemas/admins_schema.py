from typing import Optional, List
from pydantic import BaseModel, Field


from datetime import datetime

class AdminSchema(BaseModel):
    name: str = Field(..., description="the full name of the user")
    phone_number: str = Field(..., description="phone number of the user")
    password: str = Field(..., description="password of the user")
    notification_token: str = Field(None, description="notification token of the farmer")
    user_type: str =  Field("admin", description="super admin or normal admin or something else")  # super user, admin
    is_active: bool = Field(True, description="status of the user account")
    created_at: str = Field(datetime.utcnow(), description="date and time of user creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of user update")
    
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mostafa Mahmoud",
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789",
                "user_type": "admin",
                "is_active": True,
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
        

class AdminLoginModel(BaseModel):
    phone_number: str
    password: str
    notification_token: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789"
            }
        }

class UpdateAdminModel(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    notification_token: Optional[str] = None
    user_type: Optional[str] = "farmer"
    is_active: Optional[bool] = True
    updated_at: str = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mostafa Mahmoud",
                "phone_number": "+20111111111",
                "password": "password123",
                "notification_token": "123456789",
                "user_type": "farmer",
                "is_active": True,
                "updated_at": "2022-01-01 00:00:00"
            }
        }