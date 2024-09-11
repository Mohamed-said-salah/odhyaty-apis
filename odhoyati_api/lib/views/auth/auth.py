from fastapi.routing import APIRouter

from fastapi import Response, Depends, Body

from fastapi_jwt_auth import AuthJWT

import json

from typing import Optional

from .helpers.check_user_type import is_farmer, is_admin, is_super_admin, is_user

from .users_auth import router as users_auth_router
from .farmers_auth import router as farmers_auth_router
from .admins_auth import router as admins_auth_router

from controllers.crud.farmers import get_farmer_by_id, update_farmer_by_id
from controllers.crud.users import get_user_by_id, update_user_by_id
from controllers.crud.admins import get_admin_by_id, update_admin_by_id


router = APIRouter()



@router.post('/refresh-profile')
async def refresh_profile(notification_token: dict = Body(None), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")

    current_user_id = Authorize.get_jwt_subject()
    
    user_type = Authorize.get_raw_jwt().get("user_type")
    
    user = None
    print('😰😰😰 1 ')
    if is_farmer(user_type):
        user = await get_farmer_by_id(current_user_id)
    elif is_user(user_type):
        user = await get_user_by_id(current_user_id)  
    elif is_admin(user_type) or is_super_admin(user_type):
        user = await get_admin_by_id(current_user_id) 
    else :
        return Response(status_code=400, content="user type is not valid")
    
    print('😰😰😰 2 ')
    if not user:
        return Response(status_code=404, content="user not found")
    
    print('😰😰😰 3 ')
    
    if notification_token:
        if is_farmer(user_type):
            await update_farmer_by_id(current_user_id, {"notification_token": notification_token['notification_token']})
        elif is_user(user_type):
            await update_user_by_id(current_user_id, {"notification_token": notification_token['notification_token']})
        elif is_admin(user_type) or is_super_admin(user_type):
            await update_admin_by_id(current_user_id, {"notification_token": notification_token['notification_token']})
            user["is_verified"] = True
        
        user["notification_token"] = notification_token["notification_token"]

    user['created_at'] = user['created_at'].isoformat()
    user['updated_at'] = user['updated_at'].isoformat()
    
    access_token = Authorize.create_refresh_token(
            subject=str(current_user_id),
            user_claims={
                "user_type": user["user_type"],
                "is_verified": user["is_verified"],
                "is_active": user["is_active"],
            }
        )   

    return Response(
        status_code=200,
        content=json.dumps({"message": "user refreshed successfully", "data": user}), 
        headers={
            "Authorization": f"Bearer {access_token}"
            },
    )



router.include_router(users_auth_router, prefix='/users')
router.include_router(farmers_auth_router, prefix='/farmers')
router.include_router(admins_auth_router, prefix='/admins')