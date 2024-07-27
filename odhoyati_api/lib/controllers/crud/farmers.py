from bson.objectid import ObjectId

from core.database.mongo_db import farmers_collection, farmers_helper


from typing import Optional



# crud operations for farmers

# add farmer to database
async def add_farmer(farmer_data: dict) -> dict:
    farmer = await farmers_collection.insert_one(farmer_data)
    new_farmer = await farmers_collection.find_one({"_id": farmer.inserted_id})
    return farmers_helper(new_farmer)


# get all farmers
async def get_all_farmers() -> list:
    farmers = []
    async for farmer in farmers_collection.find():
        farmers.append(farmers_helper(farmer))
    return farmers


# get farmer by id
async def get_farmer_by_id(id: str) -> Optional[dict]:
    farmer = await farmers_collection.find_one({"_id": ObjectId(id)})
    if farmer:
        return farmers_helper(farmer)
    return None


# get farmer by phone number
async def get_farmer_by_phone_number(phone_number: str) -> Optional[dict]:
    farmer = await farmers_collection.find_one({"phone_number": phone_number})
    if farmer:
        return farmers_helper(farmer)
    return None


# update farmer with id
async def update_farmer_by_id(id: str, data: dict) -> Optional[dict]:
    farmer = await farmers_collection.find_one({"_id": ObjectId(id)})
    if farmer:
        updated_farmer = await farmers_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if updated_farmer:
            return farmers_helper(farmer)
        return None
    return None


# update farmer with phone number
async def update_farmer_by_phone_number(phone_number: str, data: dict) -> Optional[dict]:
    farmer = await farmers_collection.find_one({"phone_number": phone_number})
    if farmer:
        updated_farmer = await farmers_collection.update_one(
            {"phone_number": phone_number},
            {"$set": data}
        )
        if updated_farmer:
            return farmers_helper(farmer)
        return None
    return None


# delete farmer with id
async def delete_farmer_by_id(id: str) -> bool:
    farmer = await farmers_collection.find_one({"_id": ObjectId(id)})
    if farmer:
        await farmers_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False


# delete farmer with phone number
async def delete_farmer_by_phone_number(phone_number: str) -> bool:
    farmer = await farmers_collection.find_one({"phone_number": phone_number})
    if farmer:
        await farmers_collection.delete_one({"phone_number": phone_number})
        return True
    return False

