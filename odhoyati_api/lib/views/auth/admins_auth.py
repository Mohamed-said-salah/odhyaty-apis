from fastapi.routing import APIRouter

from fastapi import Body, Response, Depends

import json

import bcrypt


from fastapi_jwt_auth import AuthJWT

from security.token_settings import Settings

from core.redis.redis_conn import redis_conn as redis

from core.schemas.admins_schema import AdminSchema, AdminLoginModel


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

from controllers.notifications.notification import send_fcm_notification


TOKEN_SETTINGS = Settings()


router = APIRouter()



# todo: login
@router.post("/login")
async def login(admin: AdminLoginModel = Body(...), Authorize: AuthJWT = Depends()):

    current_admin = await get_admin_by_phone_number(admin.phone_number)
    
    if not current_admin:
        return Response(status_code=404, content="admin not found")
    
    
    
    if not bcrypt.checkpw(admin.password.encode('utf-8'), current_admin["password"].encode('utf-8')):
        return Response(status_code=401, content="invalid phone number or password")
    
    try:
        updatesMap = {}
        
        if admin.notification_token:
            updatesMap["notification_token"] = admin.notification_token
            current_admin["notification_token"] = admin.notification_token
        
        updatesMap["is_active"] = True
        
        await update_admin_by_id(current_admin["id"], updatesMap)

        admins = await get_all_admins()
        for admin in admins:
            
            await send_fcm_notification(token=admin["notification_token"], title= "fastapi", body =  "first notification trial")

    except:
        pass
    
    current_admin["is_active"] = True
    
    current_admin.pop("password")
    
    current_admin["created_at"] = current_admin["created_at"].isoformat()
    
    current_admin["updated_at"] = current_admin["updated_at"].isoformat()
    
    access_token = Authorize.create_refresh_token(
            subject=str(current_admin["id"]),
            user_claims={
                "user_type": current_admin["user_type"],
                "is_active": current_admin["is_active"],
            }
        )
    
    
    return Response(
            status_code=200,
            content=json.dumps({"message": "admin logged in successfully", "data": current_admin}),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )


# todo: logout
@router.delete("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="admin already signed out")
    
    
    
    jti = Authorize.get_raw_jwt().get('jti')
    
    with redis.client() as redis_client:
        redis_client.setex(jti, TOKEN_SETTINGS.refresh_expires, "true")
        redis_client.save()

    
    return Response(status_code=200, content="admin logged out successfully")
