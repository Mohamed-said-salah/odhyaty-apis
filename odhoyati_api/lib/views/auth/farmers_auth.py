
from fastapi.routing import APIRouter

from fastapi import Body, Response, Depends

import json

import bcrypt


from fastapi_jwt_auth import AuthJWT

from security.token_settings import Settings

from core.redis.redis_conn import redis_conn as redis

from core.schemas.farmer_schema import FarmerSchema, FarmerLoginModel


from controllers.crud.farmers import (
    add_farmer,
    get_farmer_by_id,
    get_farmer_by_phone_number,
    update_farmer_by_id,
    delete_farmer_by_id,
    delete_farmer_by_phone_number
)


TOKEN_SETTINGS = Settings()


router = APIRouter()



# todo: register
@router.post("/register")
async def register(farmer: FarmerSchema = Body(...), Authorize: AuthJWT = Depends()):
    
    current_farmer = await get_farmer_by_phone_number(farmer.phone_number)
    
    if current_farmer:
        return Response(status_code=400, content="farmer already exists")
    
    farmer.password = bcrypt.hashpw(farmer.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    farmer_dict = await add_farmer(farmer.dict())
    
    farmer_dict.pop("password")
    
    farmer_dict["created_at"] = farmer.created_at.isoformat()
    farmer_dict["updated_at"] = farmer.updated_at.isoformat()
    
    
    access_token = Authorize.create_refresh_token(
            subject=str(farmer_dict["id"]),
            user_claims={
                "user_type": farmer.user_type,
                "is_verified": farmer.is_verified,
                "is_active": farmer.is_active,
            }
        )
    
    return Response(
        status_code=201,
        content=json.dumps({"message": "farmer created successfully", "data": farmer_dict}),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    

# todo: login
@router.post("/login")
async def login(farmer: FarmerLoginModel = Body(...), Authorize: AuthJWT = Depends()):
    
    current_farmer = await get_farmer_by_phone_number(farmer.phone_number)
    
    if not current_farmer:
        return Response(status_code=404, content="farmer not found")
    
    if not bcrypt.checkpw(farmer.password.encode('utf-8'), current_farmer["password"].encode('utf-8')):
        return Response(status_code=401, content="invalid phone number or password")
    
    await update_farmer_by_id(current_farmer["id"], {"is_active": True})
    
    current_farmer["is_active"] = True
    
    current_farmer.pop("password")
    
    current_farmer["created_at"] = current_farmer["created_at"].isoformat()
    
    current_farmer["updated_at"] = current_farmer["updated_at"].isoformat()
    
    access_token = Authorize.create_refresh_token(subject=str(current_farmer["id"]))
    
    return Response(
        status_code=200,
        content=json.dumps({"message": "farmer logged in successfully", "data": current_farmer}),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    

# todo: logout
@router.delete("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="farmer already signed out")
    
    
    jti = Authorize.get_raw_jwt().get('jti')
    
    with redis.client() as redis_client:
        redis_client.setex(jti, TOKEN_SETTINGS.refresh_expires, "true")
        redis_client.save()
        
    return Response(status_code=200, content="farmer logged out successfully")


# todo: items
# todo: notifications
