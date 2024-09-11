


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


from controllers.crud.orders import (
    query_orders_by_filter,
    get_orders_by_user_id,
    get_all_orders,
    update_orders_by_user_id,
    delete_orders_by_user_id,
    add_order,
)

from controllers.crud.orders import delete_orders_by_user_id

from controllers.notifications.notification import send_fcm_notification


TOKEN_SETTINGS = Settings()

router = APIRouter()


# todo: filter orders
@router.get('/orders')
async def get_orders( user_id: Optional[str] = None, farmer_id: Optional[str] = None, item_id: Optional[str] = None , status: Optional[str] = None , created_at: Optional[str] = None , page: Optional[int] = None, limit: Optional[int] = None, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    
    filter_ = {}
    
    if user_id:
        filter_["user_id"] = ObjectId(user_id)
    if farmer_id:
        filter_["farmer_id"] = ObjectId(farmer_id)
    if item_id:
        filter_["item_id"] = ObjectId(item_id)
    if status:
        filter_["status"] = status
    if created_at:
        filter_["created_at"] = {"$lte": created_at}
    
    orders = await query_orders_by_filter(filter_, page=page, limit=limit)
    
    orders_list = []
    
    for order in orders:
        
        orders_list.append(order)
    
    return {"message": "orders fetched successfully", "data": orders_list}

# todo: create update order by id 
@router.put('/orders/{id}')
async def update_order_by_id(order_id: str, order: dict, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    order = await update_orders_by_user_id(order_id, order)
    
    return {"message": "order updated successfully", "data": order}

# todo: delete order by id
@router.delete('/orders/{id}')
async def delete_order_by_id(order_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_type = Authorize.get_raw_jwt().get("user_type")
        if not is_admin(user_type):
            return Response(status_code=403, content="you are not authorized to take this action")
        
    except:
        return Response(status_code=401, content="user not authorized")
    
    order = await delete_orders_by_user_id(order_id)
    
    return {"message": "order deleted successfully", "data": order}

