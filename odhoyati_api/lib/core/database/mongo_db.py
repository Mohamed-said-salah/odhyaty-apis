import motor.motor_asyncio

MONGO_DETAILS = "mongodb+srv://mohamed_saied:UYf33fbctQSVTwW@odhaty.ximgoxe.mongodb.net/?retryWrites=true&w=majority&appName=odhaty"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.odhyaty

users_collection = database.get_collection("users")

# todo: admins collection
# todo: appointments collection
# todo: farmers collection
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
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }