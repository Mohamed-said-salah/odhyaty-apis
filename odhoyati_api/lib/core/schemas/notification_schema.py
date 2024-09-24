


from typing import Optional
from pydantic import BaseModel, Field


from datetime import datetime

class NotificationSchema(BaseModel):
    sender_id: str = Field(..., description="the id of the user/farmer notification came from") # user who gave the review
    receiver_id: str = Field(..., description="the id of the user/farmer notification sent to") # farmer user received the review
    sender_name: str = Field(..., description="Name of the sender")
    receiver_name: str = Field(..., description="Name of the receiver")
    notification_type: str = Field(..., description="type of the notification") # new_user / new_order(for admin and farmer) / completed_order(for admin and user and farmer) / canceled_order (for admin and user and farmer) / review (for admin and user and farmer) / new_admin / new_farmer / verified_user / verified_farmer
    message: str = Field(None, description="message for user who received the notification")
    load: Optional[dict] = {}
    status: str = Field("new", description="the status of the notification") # opened / new / unsent
    created_at: str = Field(datetime.utcnow(), description="date and time of order creation")
    updated_at: str = Field(datetime.utcnow(), description="date and time of order update")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sender_id": "123456789",
                "receiver_id": "123456789",
                "notification_type": "review",
                "message": "Good item",
                "load": {
                    "item_id": "123456789",
                    "farmer_id": "123456789",
                    "order_id": "123456789"
                },
                "status": "new",
                "created_at": "2022-01-01 00:00:00",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
        


class UpdateNotificationModel(BaseModel):
    status: Optional[str] = Field("read", description="the status of the notification")
    updated_at: str = datetime.utcnow()
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "read",
                "updated_at": "2022-01-01 00:00:00"
            }
        }
