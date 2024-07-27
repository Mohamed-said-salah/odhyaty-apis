from fastapi.routing import APIRouter

from fastapi import Body, Response, Depends

import json

import bcrypt


from fastapi_jwt_auth import AuthJWT

from security.token_settings import Settings

from core.redis.redis_conn import redis_conn as redis

from core.schemas.user_schema import UserSchema, UserLoginModel


from controllers.crud.users import (
    add_user,
    get_user_by_id,
    get_user_by_phone_number,
    update_user_by_id,
    delete_user,
)


TOKEN_SETTINGS = Settings()

router = APIRouter()


# todo: register
@router.post("/register")
async def register(user: UserSchema = Body(...), Authorize: AuthJWT = Depends()):
    
    current_user = await get_user_by_phone_number(user.phone_number)
    
    if current_user:
        return Response(status_code=400, content="user already exists")
    
    user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user_dict = await add_user(user.dict())
    
    user_dict.pop("password")
    
    user_dict["created_at"] = user.created_at.isoformat()
    user_dict["updated_at"] = user.updated_at.isoformat()
    
    
    access_token = Authorize.create_refresh_token(
            subject=str(user_dict["id"]),
            user_claims={
                "user_type": user.user_type,
                "is_verified": user.is_verified,
                "is_active": user.is_active,
            }
        )
    
    return Response(
        status_code=201,
        content=json.dumps({"message": "user created successfully", "data": user_dict}),
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

# todo: login
@router.post("/login")
async def login(user: UserLoginModel = Body(...), Authorize: AuthJWT = Depends()):

    current_user = await get_user_by_phone_number(user.phone_number)
    
    if not current_user:
        return Response(status_code=404, content="user not found")
    
    if not bcrypt.checkpw(user.password.encode('utf-8'), current_user["password"].encode('utf-8')):
        return Response(status_code=401, content="invalid phone number or password")
    
    await update_user_by_id(current_user["id"], {"is_active": True})
    
    current_user["is_active"] = True
    
    current_user.pop("password")
    
    current_user["created_at"] = current_user["created_at"].isoformat()
    
    current_user["updated_at"] = current_user["updated_at"].isoformat()
    
    redis.set("me", json.dumps(current_user))
    
    access_token = Authorize.create_refresh_token(
            subject=str(current_user["id"]),
            user_claims={
                "user_type": current_user["user_type"],
                "is_verified": current_user["is_verified"],
                "is_active": current_user["is_active"],
            }
        )
    
    
    return Response(
            status_code=200,
            content=json.dumps({"message": "user logged in successfully", "data": current_user}),
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )


# todo: logout
@router.delete("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user already signed out")
    
    
    
    jti = Authorize.get_raw_jwt().get('jti')
    
    with redis.client() as redis_client:
        redis_client.setex(jti, TOKEN_SETTINGS.refresh_expires, "true")
        redis_client.save()

    
    return Response(status_code=200, content="user logged out successfully")

