from bson.objectid import ObjectId

from core.database.mongo_db import reviews_collection, reviews_helper

from .farmers import get_farmer_by_id
from .users import get_user_by_id
from .items import get_item_by_id
from .orders import get_order_by_id

from typing import Optional

# crud operations for orders

# add order to database
async def create_review(review_data: dict) -> dict:
    farmer = await get_farmer_by_id(review_data["farmer_id"])
    if not farmer:
        return None
    
    farmer = {
        "name": farmer["name"],
        "image": farmer["image"]
    }

    user = await get_user_by_id(review_data["user_id"])
    if not user:
        return None
    
    user = {
        "name": user["name"],
    }
    
    item = await get_item_by_id(review_data["item_id"])
    if not item:
        return None
    
    item = {
        "image": item["image"],
        "title": item["title"],
        "category": item["category"]
    }

    order = await get_order_by_id(review_data["order_id"])
    if not order:
        return None


    review_data["farmer_id"] = ObjectId(review_data["farmer_id"])
    review_data["user_id"] = ObjectId(review_data["user_id"])
    review_data["item_id"] = ObjectId(review_data["item_id"])
    review_data["order_id"] = ObjectId(review_data["order_id"])
    review_data["part_of_user"] = user
    review_data["part_of_farmer"] = farmer
    review_data["part_of_item"] = item

    review = await reviews_collection.insert_one(review_data)

    new_review = await reviews_collection.find_one({"_id": review.inserted_id})
    if new_review:
        return reviews_helper(new_review)
    return None



async def get_reviews_by_farmer_id(farmer_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    reviews = []
    
    if page and limit:
        async for review in reviews_collection.find({"farmer_id": ObjectId(farmer_id)}).skip((page - 1) * limit).limit(limit):
            reviews.append(reviews_helper(review))
    else:
        async for review in reviews_collection.find({"farmer_id": ObjectId(farmer_id)}):
            reviews.append(reviews_helper(review))

    return reviews


async def get_reviews_by_user_id(user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    reviews = []
    
    if page and limit:
        async for review in reviews_collection.find({"user_id": ObjectId(user_id)}).skip((page - 1) * limit).limit(limit):
            reviews.append(reviews_helper(review))
    else:
        async for review in reviews_collection.find({"user_id": ObjectId(user_id)}):
            reviews.append(reviews_helper(review))

    return reviews

async def get_reviews_by_item_id(item_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    reviews = []
    
    if page and limit:
        async for review in reviews_collection.find({"item_id": ObjectId(item_id)}).skip((page - 1) * limit).limit(limit):
            reviews.append(reviews_helper(review))
    else:
        async for review in reviews_collection.find({"item_id": ObjectId(item_id)}):
            reviews.append(reviews_helper(review))

    return reviews


async def get_review_by_order_id(order_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    review = await reviews_collection.find_one({"order_id": ObjectId(order_id)})
    if review:
        return reviews_helper(review)
    return None



async def get_review_by_id(review_id: str) -> dict:
    review = await reviews_collection.find_one({"_id": ObjectId(review_id)})
    if review:
        return reviews_helper(review)
    return None


async def update_review(id: str, data: dict) -> Optional[dict]:
    if len(data) < 1:
        return None
    review = await reviews_collection.find_one({"_id": ObjectId(id)})
    if review:
        updated_review = await reviews_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_review:
            return await reviews_collection.find_one({"_id": ObjectId(id)})
        return None
    return None


async def get_all_reviews(page: Optional[int] = None, limit: Optional[int] = None) -> list:
    reviews = []
    
    if page and limit:
        async for review in reviews_collection.find().skip((page - 1) * limit).limit(limit):
            reviews.append(reviews_helper(review))
    else:
        async for review in reviews_collection.find():
            reviews.append(reviews_helper(review))

    return reviews


async def query_reviews_by_filter(filter_: dict, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    reviews = []
    
    # Case of Pagination
    if page and limit:
        async for review in reviews_collection.find(filter_).skip((page - 1) * limit).limit(limit):
            reviews.append(reviews_helper(review))
    
    # Case of No Pagination
    else :
        async for review in reviews_collection.find(filter_):
            reviews.append(reviews_helper(review))
    
    return reviews


async def delete_review(id: str) -> bool:
    review = await reviews_collection.find_one({"_id": ObjectId(id)})
    if review:
        await reviews_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

