from bson.objectid import ObjectId

from core.database.mongo_db import admins_collection, admins_helper


from typing import Optional

# crud operations for admins

# add admin to database
async def add_admin(admin_data: dict) -> dict:
    admin = await admins_collection.insert_one(admin_data)
    new_admin = await admins_collection.find_one({"_id": admin.inserted_id})
    return admins_helper(new_admin)


# get all admins
async def get_all_admins() -> list:
    admins = []
    async for admin in admins_collection.find():
        admins.append(admins_helper(admin))
    return admins


# get admin by id
async def get_admin_by_id(id: str) -> Optional[dict]:
    admin = await admins_collection.find_one({"_id": ObjectId(id)})
    if admin:
        return admins_helper(admin)
    return None


# get admin by phone number
async def get_admin_by_phone_number(phone_number: str) -> Optional[dict]:
    admin = await admins_collection.find_one({"phone_number": phone_number})
    if admin:
        return admins_helper(admin)
    return None

# update admin with id
async def update_admin_by_id(id: str, data: dict) -> Optional[dict]:
    admin = await admins_collection.find_one({"_id": ObjectId(id)})
    if admin:
        updated_admin = await admins_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if updated_admin:
            return admins_helper(admin)
        return None
    return None


# update admin with phone number
async def update_admin_by_phone_number(phone_number: str, data: dict) -> Optional[dict]:
    admin = await admins_collection.find_one({"phone_number": phone_number})
    if admin:
        updated_admin = await admins_collection.update_one(
            {"phone_number": phone_number},
            {"$set": data}
        )
        if updated_admin:
            return admins_helper(admin)
        return None
    return None


# delete admin with id
async def delete_admin_by_id(id: str) -> bool:
    admin = await admins_collection.find_one({"_id": ObjectId(id)})
    if admin:
        await admins_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False


# delete admin with phone number
async def delete_admin_by_phone_number(phone_number: str) -> bool:
    admin = await admins_collection.find_one({"phone_number": phone_number})
    if admin:
        await admins_collection.delete_one({"phone_number": phone_number})
        return True
    return False