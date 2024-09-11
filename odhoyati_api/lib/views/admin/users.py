
from fastapi.routing import APIRouter

from typing import Optional

from fastapi import Body, Response, Depends

import json

import bcrypt

from ..auth.helpers.check_user_type import is_super_admin, is_admin

from fastapi_jwt_auth import AuthJWT

from security.token_settings import Settings

from core.redis.redis_conn import redis_conn as redis

from bson.objectid import ObjectId


from controllers.crud.users import (
    add_user,
    get_user_by_id,
    get_user_by_phone_number,
    get_users_by_filter,
    update_user_by_id,
    delete_user, 
    delete_user_by_phone_number,
)

from controllers.crud.orders import update_orders_by_user_id

from controllers.crud.orders import delete_orders_by_user_id

from controllers.notifications.notification import send_fcm_notification

from controllers.crud.farmers import get_farmer_by_id


TOKEN_SETTINGS = Settings()

router = APIRouter()

# todo: get non verified users
@router.get("/in-active-users")
async def get_in_activated_users(page: Optional[int] = None, limit: Optional[int] = None, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    

    users = await get_users_by_filter(filter_={"is_verified": False}, page=page, limit=limit)
    
    users_list = []
    
    for user in users:
        
        user.pop("password")
        
        users_list.append(user)
    
    return {"message": "users fetched successfully", "data": users_list}

# todo: verify user
@router.patch("/verify-user")
async def verify_user(user_id: str, Authorize: AuthJWT = Depends()):
    
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")

    user = await get_user_by_id(user_id)
    
    if not user:
        return Response(status_code=404, content="user not found")
    
    if user["is_verified"]:
        return Response(status_code=400, content="user is already verified")
    
    await update_user_by_id(user_id, {"is_verified": True})
    
    orders = await update_orders_by_user_id(user_id, {"status": "PENDING"})
    
    if orders:
        for order in orders:
            farmer_id = order["farmer_id"]
            farmer = await get_farmer_by_id(farmer_id)
            try:
                # todo: get the admins ids and loop throw them to send the notifications to the all admins accounts
                await send_fcm_notification(token=farmer["notification_token"], title= "fastapi", body =  "first notification trial")
            except:
                pass
    
    user.pop("password")
    user["is_verified"] = True
    
    return {"message": "user verified successfully", "data": user}


# todo: filter users
@router.get("/filter-users")
async def filter_users(page: Optional[int] = None, limit: Optional[int] = None, user_id: Optional[str] = None, phone_number: Optional[str] = None, location: Optional[str] = None, is_active: Optional[bool] = None, is_verified: Optional[bool] = None,   Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    filter_dict = {}
    
    if user_id:
        filter_dict["_id"] = ObjectId(user_id)
    
    if phone_number:
        filter_dict["phone_number"] = "+" + phone_number
    
    if location:
        filter_dict["location"] = location
    
    if is_active is not None:
        filter_dict["is_active"] = is_active
    
    if is_verified is not None:
        filter_dict["is_verified"] = is_verified
    

    users = await get_users_by_filter(page=page, limit=limit, filter_ = filter_dict)
    
    users_list = []
    
    for user in users:
        
        user.pop("password")
        
        users_list.append(user)
    
    return {"message": "users fetched successfully", "data": users_list}


# todo: delete user by id
@router.delete("/delete-user-by-id")
async def delete_user_by_id(user_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    await delete_user(user_id)
    
    await delete_orders_by_user_id(user_id)
    
    return {"message": "user deleted successfully", "data": {"user_id": user_id}}

# todo: delete user by phone number
@router.delete("/delete-user-by-phone")
async def delete_user_by_phone_his_number(phone_number: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    
    user = await get_user_by_phone_number(phone_number)
    
    if not user:
        return Response(status_code=404, content="user not found")
    
    await delete_user_by_phone_number("+" + phone_number)
    
    await delete_orders_by_user_id(user["id"])
    
    return {"message": "user deleted successfully", "data": {"phone_number": phone_number}}