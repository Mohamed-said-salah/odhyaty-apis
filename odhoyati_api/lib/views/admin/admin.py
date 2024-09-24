from fastapi.routing import APIRouter

from fastapi import Body, Response, Depends

import json

import bcrypt


from fastapi_jwt_auth import AuthJWT

from security.token_settings import Settings

from core.redis.redis_conn import redis_conn as redis

from core.schemas.admins_schema import AdminSchema, AdminLoginModel

from core.schemas.notification_schema import NotificationSchema

from ..auth.helpers.check_user_type import is_super_admin

from controllers.crud.admins import (
    add_admin,
    get_all_admins,
    get_admin_by_id,
    get_admin_by_phone_number,
    update_admin_by_id,
    update_admin_by_phone_number,
    delete_admin_by_id,
    delete_admin_by_phone_number,
)

from controllers.crud.notifications import create_notification


from controllers.notifications.notification import send_fcm_notification


TOKEN_SETTINGS = Settings()


router = APIRouter()


# todo: add
@router.post("/add")
async def add(admin: AdminSchema = Body(...), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        
        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_super_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    current_admin = await get_admin_by_phone_number(admin.phone_number)
    
    if current_admin:
        return Response(status_code=400, content="admin already exists")
    
    admin.password = bcrypt.hashpw(admin.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    admin_dict = await add_admin(admin.dict())
    
    admin_dict.pop("password")
    admin_dict["created_at"] = admin_dict["created_at"].isoformat()
    admin_dict["updated_at"] = admin_dict["updated_at"].isoformat()
    
    try:
        admins = await get_all_admins()
        for admin in admins:
            try:
                await send_fcm_notification(token=admin["notification_token"], title= "إشعار أضحيتي", body =  "تم انشاء حساب ادمن جديد", load= {"type": "new_admin", "account_id": admin_dict["id"]}) # todo: edit the notification body
                notification_data = NotificationSchema(sender_id = Authorize.get_jwt_subject(), receiver_id = "admin", sender_name = "super admin account", receiver_name = "all admins", type = "new_admin", message = "تم انشاء حساب ادمن جديد", load= {"type": "new_admin", "account_id": admin_dict["id"]},  status = "new")
                await create_notification(notification_data.dict())
            except:
                pass
    except:
        pass
    
    return Response(status_code=201, content=json.dumps({"message": "admin created successfully", "data": admin_dict}))

# todo: remove
@router.delete("/remove")
async def remove(admin_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        
        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_super_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    await delete_admin_by_id(admin_id)
    
    return {"message": "admin removed successfully", "data": {"admin_id": admin_id}}


# todo: get admins
@router.get("/admins")
async def get_admins(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_super_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")

    except:
        return Response(status_code=401, content="user not authorized")
    
    admins = await get_all_admins()

    for admin in admins:
        
        admin.pop("password")

    return {"message": "admins retrieved successfully", "data": admins}
