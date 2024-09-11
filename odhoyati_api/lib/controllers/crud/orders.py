from bson.objectid import ObjectId

from core.database.mongo_db import orders_collection, orders_helper

from .farmers import get_farmer_by_id
from .users import get_user_by_id
from .items import get_item_by_id

from typing import Optional

# crud operations for orders

# add order to database
async def add_order(order_data: dict) -> dict:
    farmer = await get_farmer_by_id(order_data["farmer_id"])
    if not farmer:
        return None

    user = await get_user_by_id(order_data["user_id"])
    if not user:
        return None

    item = await get_item_by_id(order_data["item_id"])
    if not item:
        return None

    order_data["farmer_id"] = ObjectId(order_data["farmer_id"])
    order_data["user_id"] = ObjectId(order_data["user_id"])
    order_data["item_id"] = ObjectId(order_data["item_id"])

    order = await orders_collection.insert_one(order_data)

    new_order = await orders_collection.find_one({"_id": order.inserted_id})
    if new_order:
        return orders_helper(new_order)
    return None



# get order by id
async def get_order_by_id(id: str) -> Optional[dict]:
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        return orders_helper(order)
    return None

# get orders by user id
async def get_orders_by_user_id(user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    orders = []
    
    if page and limit:
        async for order in orders_collection.find({"user_id": ObjectId(user_id)}).skip((page - 1) * limit).limit(limit):
            orders.append(orders_helper(order))
    else:
        async for order in orders_collection.find({"user_id": ObjectId(user_id)}):
            orders.append(orders_helper(order))

    return orders

# get orders by farmer id
async def get_orders_by_farmer_id(farmer_id: str, excludeNonVerified = True, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    orders = []
    
    filter_ = {}
    
    if excludeNonVerified:
        filter_ = {"farmer_id": ObjectId(farmer_id), "status": {"$ne": "UNVERIFIED"}}
    else:
        filter_ = {"farmer_id": ObjectId(farmer_id)}
    
    if page and limit:
        async for order in orders_collection.find(filter_).skip((page - 1) * limit).limit(limit):
            orders.append(orders_helper(order))
    else:
        async for order in orders_collection.find(filter_):
            orders.append(orders_helper(order))

    return orders

# get all orders
async def get_all_orders(is_active: bool = True, page: Optional[int] = None, limit: Optional[int] = None) -> list:

    orders = []
    
    # This is for pagination and limiting
    if page and limit:
        
        async for order in orders_collection.find().skip((page - 1) * limit).limit(limit):
            orders.append(orders_helper(order))
        
    
    else:
        async for order in orders_collection.find():
            orders.append(orders_helper(order))
    
    return orders

# get order by filter
async def query_orders_by_filter(filter_: dict, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    orders = []
    
    # Case of Pagination
    if page and limit:
        async for order in orders_collection.find(filter_).skip((page - 1) * limit).limit(limit):
            orders.append(orders_helper(order))
    
    # Case of No Pagination
    else :
        async for order in orders_collection.find(filter_):
            orders.append(orders_helper(order))
    
    return orders

# update order
async def update_order(id: str, data: dict) -> Optional[dict]:
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        updated_order = await orders_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_order:
            new_order = await orders_collection.find_one({"_id": ObjectId(id)})
            if new_order:
                return orders_helper(new_order)
    return None

# update order by user id
async def update_orders_by_user_id(user_id: str, data: dict) -> Optional[dict]:
    orders = await orders_collection.find({"user_id": ObjectId(user_id)})
    if orders:
        updated_orders = []
        async for order in orders:
            updated_order = await orders_collection.update_one({"_id": order["_id"]}, {"$set": data})
            if updated_order:
                new_order = await orders_collection.find_one({"_id": order["_id"]})
                if new_order:
                    updated_orders.append(orders_helper(new_order))
        return updated_orders
    return None

# delete order
async def delete_order(id: str) -> Optional[dict]:
    order = await orders_collection.find_one({"_id": ObjectId(id)})
    if order:
        deleted_order = await orders_collection.delete_one({"_id": ObjectId(id)})
        if deleted_order:
            return orders_helper(order)
    return None

# todo: delete orders by user id
async def delete_orders_by_user_id(user_id: str) -> Optional[dict]:
    deleted_orders = await orders_collection.delete_many({"user_id": ObjectId(user_id)})
    if deleted_orders:
        return deleted_orders
    return None

# todo: delete orders by farmer id
async def delete_orders_by_farmer_id(farmer_id: str) -> Optional[dict]:
    deleted_orders = await orders_collection.delete_many({"farmer_id": ObjectId(farmer_id)})
    if deleted_orders:
        return deleted_orders
    return None
