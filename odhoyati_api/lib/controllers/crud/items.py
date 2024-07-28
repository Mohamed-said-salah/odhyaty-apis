from bson.objectid import ObjectId

from core.database.mongo_db import items_collection, items_helper

from .farmers import get_farmer_by_id

from typing import Optional



# crud operations for items

# add item to database
async def add_item(item_data: dict) -> dict:

    farmer = await get_farmer_by_id(item_data["farmer_id"])
    if not farmer:
        return None
    item_data["farmer_id"] = ObjectId(item_data["farmer_id"])

    item = await items_collection.insert_one(item_data)

    new_item = await items_collection.find_one({"_id": item.inserted_id})
    if new_item:
        return items_helper(new_item)
    return None



# get item by id
async def get_item_by_id(id: str) -> Optional[dict]:
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item:
        return items_helper(item)
    return None


# get all items
async def get_items() -> list:
    items = []
    async for item in items_collection.find():
        items.append(items_helper(item))
    return items


# get items by filter
async def get_items_by_filter(filter: dict) -> list:
    items = []
    async for item in items_collection.find(filter):
        items.append(items_helper(item))
    return items

# todo: paginate items

# update item by id
async def update_item_by_id(id: str, data: dict) -> Optional[dict]:
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item:
        updated_item = await items_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if updated_item:
            return items_helper(item)
        return None
    return None


# delete item by id
async def delete_item_by_id(id: str) -> bool:
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item:
        await items_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

# delete item by farmer id
async def delete_item_by_farmer_id(id: str) -> bool:
    item = await items_collection.find_one({"farmer_id": ObjectId(id)})
    if item:
        await items_collection.delete_one({"farmer_id": ObjectId(id)})
        return True
    return False


