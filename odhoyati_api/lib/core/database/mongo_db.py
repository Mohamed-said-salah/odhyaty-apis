import motor.motor_asyncio

MONGO_DETAILS = "mongodb+srv://mohamed_saied:UYf33fbctQSVTwW@odhaty.ximgoxe.mongodb.net/?retryWrites=true&w=majority&appName=odhaty"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.odhyaty

users_collection = database.get_collection("users")
farmers_collection = database.get_collection("farmers")

# todo: admins collection
# todo: appointments collection
# todo: items collection


def users_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "location": user["location"],
        "address": user["address"],
        "phone_number": user["phone_number"],
        "password": user["password"],
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
        "image": farmer["image"],
        "user_type": farmer["user_type"],
        "has_slaughtering": farmer["has_slaughtering"],
        "has_delivering": farmer["has_delivering"],
        "work_hours": farmer["work_hours"],
        "work_days": farmer["work_days"],
        "is_verified": farmer["is_verified"],
        "is_active": farmer["is_active"],
        "created_at": farmer["created_at"],
        "updated_at": farmer["updated_at"]
    }