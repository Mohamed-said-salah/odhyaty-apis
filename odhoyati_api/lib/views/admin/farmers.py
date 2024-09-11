
from fastapi.routing import APIRouter

from typing import Optional, List

from fastapi import Body, Response, Depends

import json

import bcrypt

from ..auth.helpers.check_user_type import is_super_admin, is_admin

from fastapi_jwt_auth import AuthJWT

from security.token_settings import Settings

from core.redis.redis_conn import redis_conn as redis

from bson.objectid import ObjectId


from controllers.crud.farmers import (
    add_farmer,
    get_farmer_by_id,
    get_farmer_by_phone_number,
    get_all_farmers,
    get_farmers_by_filter,
    update_farmer_by_id,
    update_farmer_by_phone_number,
    delete_farmer_by_id, 
    delete_farmer_by_phone_number
)

from controllers.crud.orders import delete_orders_by_farmer_id

from controllers.notifications.notification import send_fcm_notification


TOKEN_SETTINGS = Settings()

router = APIRouter()

# todo: get non verified farmers
@router.get("/in-active-farmers")
async def get_in_activated_farmers(page: Optional[int] = None, limit: Optional[int] = None, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    

    farmers = await get_farmers_by_filter(filter_={"is_verified": False}, page=page, limit=limit)
    
    farmers_list = []
    
    for farmer in farmers:
        
        farmer.pop("password")
        
        farmers_list.append(farmer)
    
    return {"message": "farmers fetched successfully", "data": farmers_list}

# todo: verify farmer
@router.patch("/verify-farmer")
async def verify_farmer(farmer_id: str, Authorize: AuthJWT = Depends()):
    
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")

    farmer = await get_farmer_by_id(farmer_id)
    
    if not farmer:
        return Response(status_code=404, content="farmer not found")
    
    if farmer["is_verified"]:
        return Response(status_code=400, content="farmer is already verified")
    
    await update_farmer_by_id(farmer_id, {"is_verified": True})
    
    farmer.pop("password")
    farmer["is_verified"] = True
    
    return {"message": "farmer verified successfully", "data": farmer}


# todo: filter users
@router.get("/filter-farmers")
async def filter_users(page: Optional[int] = None, limit: Optional[int] = None, farmer_id: Optional[str] = None, phone_number: Optional[str] = None, location: Optional[str] = None, is_active: Optional[bool] = None, is_verified: Optional[bool] = None, has_slaughtering: Optional[bool] = None, has_delivering: Optional[bool] = None, rating: Optional[int] = None, work_days: Optional[List[int]] = None, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    filter_dict = {}
    
    if farmer_id:
        filter_dict["_id"] = ObjectId(farmer_id)
    
    if phone_number:
        filter_dict["phone_number"] = "+" + phone_number
    
    if location:
        filter_dict["location"] = location
    
    if is_active is not None:
        filter_dict["is_active"] = is_active
    
    if is_verified is not None:
        filter_dict["is_verified"] = is_verified
    
    if has_slaughtering is not None:
        filter_dict["has_slaughtering"] = has_slaughtering
    
    if has_delivering is not None:
        filter_dict["has_delivering"] = has_delivering
    
    if rating is not None:
        filter_dict["rating"] = rating
    
    if work_days:
        filter_dict["work_days"] = { "$in": work_days }


    farmers = await get_farmers_by_filter(page=page, limit=limit, filter_ = filter_dict)
    
    farmers_list = []
    
    for farmer in farmers:
        
        farmer.pop("password")
        
        farmers_list.append(farmer)
    
    return {"message": "farmers fetched successfully", "data": farmers_list}


# todo: delete user by id
@router.delete("/delete-farmer-by-id")
async def delete_farmer_by_id(farmer_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    await delete_farmer_by_id(farmer_id)
    
    return {"message": "farmer deleted successfully", "data": {"farmer_id": farmer_id}}

# todo: delete user by phone number
@router.delete("/delete-farmer-by-phone")
async def delete_farmer_by_phone_his_number(phone_number: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    
    farmer = await get_farmer_by_phone_number(phone_number)
    
    if not farmer:
        return Response(status_code=404, content="farmer not found")
    
    await delete_farmer_by_phone_number("+" + phone_number)
    
    await delete_orders_by_farmer_id(farmer["id"])
    
    return {"message": "farmer deleted successfully", "data": {"phone_number": phone_number}}

