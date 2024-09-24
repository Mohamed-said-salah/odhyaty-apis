from bson.objectid import ObjectId

from core.database.mongo_db import notification_collection, notification_helper

from typing import Optional



# crud operations for notifications

# add notification to database
async def create_notification(notification_data: dict) -> dict:

    notification = await notification_collection.insert_one(notification_data)
    

    new_notification = await notification_collection.find_one({"_id": notification.inserted_id})
    if new_notification:
        return notification_helper(new_notification)
    
    return None


# get notifications by receiver id
async def get_notifications_by_receiver_id(receiver_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> list:
    notifications = []
    
    if page and limit:
        async for notification in notification_collection.find({"receiver_id": ObjectId(receiver_id)}).skip((page - 1) * limit).limit(limit):
            notifications.append(notification_helper(notification))
    else:
        async for notification in notification_collection.find({"receiver_id": ObjectId(receiver_id)}):
            notifications.append(notification_helper(notification))

    return notifications


# todo: get notification by id
async def get_notification_by_id(notification_id: str) -> dict:
    notification = await notification_collection.find_one({"_id": ObjectId(notification_id)})
    if notification:
        return notification_helper(notification)

# update notification by id
async def update_notification(notification_id: str, notification_data: dict) -> dict:
    if len(notification_data) < 1:
        return None
    notification = await notification_collection.find_one({"_id": ObjectId(notification_id)})
    if notification:
        updated_notification = await notification_collection.update_one({"_id": ObjectId(notification_id)}, {"$set": notification_data})
        if updated_notification:
            return await notification_collection.find_one({"_id": ObjectId(notification_id)})
        return None
    return None

# delete notification by id
async def delete_notification(notification_id: str, receiver_id: str) -> bool:
    notification = await notification_collection.delete_one({"_id": ObjectId(notification_id), "receiver_id": ObjectId(receiver_id)})
    if notification.deleted_count > 0:
        return True
    return False

# delete all user notifications
async def delete_notifications_by_receiver_id(receiver_id: str) -> bool:
    notification = await notification_collection.delete_many({"receiver_id": ObjectId(receiver_id)})
    if notification.deleted_count > 0:
        return True
    return False