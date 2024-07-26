from bson.objectid import ObjectId

from core.database.mongo_db import users_collection, users_helper


from typing import Optional

# crud operations for users

# add user to database
async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return users_helper(new_user)

# get all users
async def get_all_users() -> list:
    users = []
    async for user in users_collection.find():
        users.append(users_helper(user))
    return users

# get user by id
async def get_user_by_id(id: str) -> Optional[dict]:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        return users_helper(user)
    return None

# get user by phone number
async def get_user_by_phone_number(phone_number: str) -> Optional[dict]:
    user = await users_collection.find_one({"phone_number": phone_number})
    if user:
        return users_helper(user)
    return None

# update user with id
async def update_user_by_id(id: str, data: dict) -> Optional[dict]:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if updated_user:
            return users_helper(user)
        return None
    return None

# update user with phone number
async def update_user_by_phone_number(phone_number: str, data: dict) -> Optional[dict]:
    user = await users_collection.find_one({"phone_number": phone_number})
    if user:
        updated_user = await users_collection.update_one(
            {"phone_number": phone_number},
            {"$set": data}
        )
        if updated_user:
            return users_helper(user)
        return None
    return None

# delete user with id
async def delete_user(id: str) -> bool:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

# delete user with phone number
async def delete_user_by_phone_number(phone_number: str) -> bool:
    user = await users_collection.find_one({"phone_number": phone_number})
    if user:
        await users_collection.delete_one({"phone_number": phone_number})
        return True
    return False
