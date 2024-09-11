import motor.motor_asyncio

MONGO_DETAILS = "mongodb+srv://mohamed_saied:UYf33fbctQSVTwW@odhaty.ximgoxe.mongodb.net/?retryWrites=true&w=majority&appName=odhaty"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.odhyaty

users_collection = database.get_collection("users")
farmers_collection = database.get_collection("farmers")
items_collection = database.get_collection("items")
orders_collection = database.get_collection("orders")
reviews_collection = database.get_collection("reviews")
notification_collection = database.get_collection("notifications")
admins_collection = database.get_collection("admins")

# todo: admins collection
# todo: appointments collection



def users_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "location": user["location"],
        "address": user["address"],
        "phone_number": user["phone_number"],
        "password": user["password"],
        "notification_token": user["notification_token"],
        "is_verified": user["is_verified"],
        "is_active": user["is_active"],
        "user_type": user["user_type"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def farmers_helper(farmer) -> dict:
    return {
        "id": str(farmer["_id"]),
        "name": farmer["name"],
        "bio": farmer["bio"],
        "location": farmer["location"],
        "address": farmer["address"],
        "phone_number": farmer["phone_number"],
        "password": farmer["password"],
        "notification_token": farmer["notification_token"],
        "image": farmer["image"],
        "user_type": farmer["user_type"],
        "has_slaughtering": farmer["has_slaughtering"],
        "has_delivering": farmer["has_delivering"],
        "work_hours": farmer["work_hours"],
        "work_days": farmer["work_days"],
        "rating": farmer["rating"],
        "is_verified": farmer["is_verified"],
        "is_active": farmer["is_active"],
        "created_at": farmer["created_at"],
        "updated_at": farmer["updated_at"]
    }
    

def items_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "farmer_id": str(item["farmer_id"]),
        "image": item["image"],
        "title": item["title"],
        "description": item["description"],
        "category": item["category"],
        "weight": item["weight"],
        "gender": item["gender"],
        "pricePerKilo": item["pricePerKilo"],
        "age": item["age"],
        "quantity": item["quantity"],
        "is_slaughtering": item["is_slaughtering"],
        "is_delivering": item["is_delivering"],
        "is_active": item["is_active"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"]
    }
    
    
def orders_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "user_id": str(order["user_id"]),
        "farmer_id": str(order["farmer_id"]),
        "item_id": str(order["item_id"]),
        "part_of_the_item": order["part_of_the_item"],
        "status": order["status"],
        "created_at": order["created_at"],
        "updated_at": order["updated_at"],
        "reviewed": order["reviewed"],
        "farmer_sent_notification": order["farmer_sent_notification"],
        "closed_by": order["closed_by"]
    }


def reviews_helper(review) -> dict:
    return {
        "id": str(review["_id"]),
        "user_id": str(review["user_id"]),
        "farmer_id": str(review["farmer_id"]),
        "item_id": str(review["item_id"]),
        "order_id": str(review["order_id"]),
        "part_of_user": review["part_of_user"],
        "part_of_farmer": review["part_of_farmer"],
        "part_of_item": review["part_of_item"],
        "rate": review["rate"],
        "review": review["review"],
        "created_at": review["created_at"],
        "updated_at": review["updated_at"],
    }

def notification_helper(notification) -> dict:
    return {
        "id": str(notification["_id"]),
        "sender_id": notification["sender_id"],
        "receiver_id": notification["receiver_id"],
        "sender_name": notification["sender_name"],
        "receiver_name": notification["receiver_name"],
        "type": notification["type"],
        "message": notification["message"],
        "load": notification["load"],
        "status": notification["status"],
        "created_at": notification["created_at"],
        "updated_at": notification["updated_at"]
    }
    

def admins_helper(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "name": admin["name"],
        "phone_number": admin["phone_number"],
        "password": admin["password"],
        "notification_token": admin["notification_token"],
        "user_type": admin["user_type"],
        "is_active": admin["is_active"],
        "created_at": admin["created_at"],
        "updated_at": admin["updated_at"]
    }