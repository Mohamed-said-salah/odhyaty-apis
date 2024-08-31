
from fastapi.routing import APIRouter

from fastapi import Response, Depends

from fastapi_jwt_auth import AuthJWT


from typing import Optional, Union

import json

from core.schemas.orders_schema import OrderSchema, UpdateOrderModel

from controllers.crud.farmers import get_farmer_by_id

from controllers.crud.items import get_item_by_id

from controllers.crud.orders import (
    add_order,
    get_order_by_id,
    get_orders_by_user_id,
    get_orders_by_farmer_id,
    get_all_orders,
    query_orders_by_filter,
    update_order,
    delete_order,
)

from ..auth.helpers.check_user_type import is_farmer, is_admin, is_super_admin, is_user

router = APIRouter()



# Todo: create order
@router.post("/add")
async def create(order: OrderSchema, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")
    

    if not is_user(Authorize.get_raw_jwt().get("user_type")):
        return Response(status_code=400, content="user type does not has privileges to take this action.")
    
    user_id = Authorize.get_jwt_subject()
    
    order.user_id = user_id
    
    if not Authorize.get_raw_jwt().get("is_verified"):
        order.status = "UNVERIFIED"
    
    
    farmer = await get_farmer_by_id(order.farmer_id)
    
    if not farmer:
        return Response(status_code=400, content="farmer not found")
    
    item = await get_item_by_id(order.item_id)
    
    if not item:
        return Response(status_code=400, content="item not found")
    
    if item.get("is_active"):
        part_of_the_item = {
            "title": item.get("title"),
            "description": item.get("description"),
            "category": item.get("category"),
            "weight": item.get("weight"),
            "gender": item.get("gender"),
            "pricePerKilo": item.get("pricePerKilo"),
            "age": item.get("age"),
            "is_slaughtering": item.get("is_slaughtering"),
            "is_delivering": item.get("is_delivering"),
            "image": item.get("image"),
        }
        
    else:
        return Response(status_code=400, content="item not available")
    
    order.part_of_the_item = part_of_the_item
    
    order_dict = await add_order(order.dict())
    
    order_dict["created_at"] = order.created_at.isoformat()
    order_dict["updated_at"] = order.updated_at.isoformat()
    
    return Response(status_code=201, content=json.dumps({"message": "order created successfully", "data": order_dict}))


# todo: get orders for user
@router.get("/user-orders")
async def get_all_orders(page: Optional[int] = None, limit: Optional[int] = None, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        
    except:
        return Response(status_code=401, content="user not authorized")

    user_id = Authorize.get_jwt_subject()
    
    orders = await get_orders_by_user_id(user_id, page, limit)
    
    return {"message": "orders fetched successfully", "data": orders}


# Todo: accept order (trader)

# Todo: decline order (trader)

# Todo: miss order (admin)

# Todo: failed (admin, customer)

# Todo: completed (admin, customer, trader)
