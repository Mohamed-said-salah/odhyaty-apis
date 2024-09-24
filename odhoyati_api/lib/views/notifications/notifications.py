
from fastapi.routing import APIRouter

from fastapi import Response, Depends

from fastapi_jwt_auth import AuthJWT


from typing import Optional, Union

import json

from core.schemas.notification_schema import NotificationSchema



from controllers.crud.notifications import (
    create_notification,
    get_notification_by_id,
    get_notifications_by_receiver_id,
    update_notification,
    delete_notification,
    delete_notifications_by_receiver_id
    )



router = APIRouter()

# todo: paginate notifications
@router.get("/notifications")
async def get_notifications( page: Optional[int] = None, limit: Optional[int] = None, Authorize: AuthJWT = Depends(),):
    
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")
    
    receiver_id = Authorize.get_jwt_subject()
    
    notifications = await get_notifications_by_receiver_id(receiver_id=receiver_id, page=page, limit=limit)
    
    return {"message": "notifications fetched successfully", "data": notifications}



# todo: delete notification by id
@router.delete("/notifications/{notification_id}")
async def delete_notification_by_id(notification_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")
    
    receiver_id = Authorize.get_jwt_subject()
    
    deleted_notification = await delete_notification(notification_id=notification_id, receiver_id=receiver_id)
    
    return {"message": "notification deleted successfully", "data": deleted_notification}


# todo: delete all notifications

@router.delete("/notifications/delete-all")
async def delete_notification_by_id(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")
    
    receiver_id = Authorize.get_jwt_subject()
    
    if await delete_notifications_by_receiver_id(receiver_id=receiver_id):
        return {"message": "notifications deleted successfully"}
    
    return Response(status_code=400, content="no notifications found")


# todo: read notification
@router.patch("/notifications/read/{notification_id}")
async def delete_notification_by_id(notification_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")
    
    receiver_id = Authorize.get_jwt_subject()
    
    notification = await get_notification_by_id(notification_id=notification_id)
    
    if not notification:
        return Response(status_code=404, content="notification not found")
    
    if notification["receiver_id"] != receiver_id:
        return Response(status_code=403, content="you are not authorized to read this notification")
    
    read_notification = await update_notification(notification_id=notification_id, notification_data={"status": "opened"})
    
    return {"message": "notification deleted successfully", "data": read_notification}


