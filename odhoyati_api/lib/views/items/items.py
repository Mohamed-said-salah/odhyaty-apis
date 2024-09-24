from fastapi.routing import APIRouter

from fastapi import  Response, Depends, File, UploadFile, Form

import shutil

import os

from fastapi_jwt_auth import AuthJWT

from typing import Optional, Union

import json

from secrets import token_hex

from core.schemas.items_schema import ItemSchema, UpdateItemModel

from controllers.crud.items import (
    add_item,
    get_item_by_id,
    get_items,
    query_items_by_filter,
    update_item_by_id,
    delete_item_by_id,
    delete_item_by_farmer_id,
)

from   ..auth.helpers.check_user_type import is_farmer, is_admin, is_super_admin

router = APIRouter()

# Todo: create item
@router.post("/add")
async def create_item( item_string: str = Form(...) , image: UploadFile = File(None) , Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="user not authorized")

    if not is_farmer(Authorize.get_raw_jwt().get("user_type")):
        return Response(status_code=400, content="user type does not has privileges to take this action.")

    farmer_id = Authorize.get_jwt_subject()
    
    # Parse the JSON item
    item_data = json.loads(item_string)
    item = ItemSchema(**item_data)
    item.farmer_id = farmer_id
    
    if image:
        image_unique_id = f"{farmer_id}/{token_hex(5)}.jpg"
        image_path = f"/mnt/d/api_images/{image_unique_id}" # todo: edit this while on production 
        
        # this makes sure that the directory is made before saving to it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        item.image = image_unique_id
    
    item_dict = await add_item(item.dict())
    
    item_dict["created_at"] = item.created_at.isoformat()
    item_dict["updated_at"] = item.updated_at.isoformat()
    
    return Response(status_code=201, content=json.dumps({"message": "item created successfully", "data": item_dict}))


# Todo: get items
@router.get("/")
async def get_all_items(page: Optional[int] = None, limit: Optional[int] = None, Authorize: AuthJWT = Depends()):
    is_active = True

    try:
        Authorize.jwt_refresh_token_required()
        
        user_type = Authorize.get_raw_jwt().get("user_type")
        if is_farmer(user_type) or is_admin(user_type) or is_super_admin(user_type):
            is_active = False
        
    except:
        pass

    items = await get_items(is_active=is_active, page=page, limit=limit)
    return {"message": "items fetched successfully", "data": items}

# Todo: filter items
@router.get("/filter")
async def get_items_by_filter(
    from_weight: Optional[int] = None,
    to_weight: Optional[int] = None,
    from_price_per_kilo: Optional[int] = None,
    to_price_per_kilo: Optional[int] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    from_age: Optional[int] = None,
    to_age: Optional[int] = None,
    is_slaughtering: Optional[bool] = None,
    is_delivering: Optional[bool] = None,
    page: Optional[int] = None,
    limit: Optional[int] = None,
):
    query_filter = {}
    
    if from_weight:
        query_filter["weight"] = {"$gte": from_weight}
    if to_weight:
        query_filter["weight"] = {"$lte": to_weight}
    if from_price_per_kilo:
        query_filter["pricePerKilo"] = {"$gte": from_price_per_kilo}
    if to_price_per_kilo:
        query_filter["pricePerKilo"] = {"$lte": to_price_per_kilo}
    if category:
        query_filter["category"] = category
    if gender:
        query_filter["gender"] = gender
    if from_age:
        query_filter["age"] = {"$gte": from_age}
    if to_age:
        query_filter["age"] = {"$lte": to_age}
    if is_slaughtering:
        query_filter["is_slaughtering"] = is_slaughtering
    if is_delivering:
        query_filter["is_delivering"] = is_delivering
    
    query_filter["is_active"] = True

    items = await query_items_by_filter(filter_=query_filter, page=page, limit=limit) # get items by filter
    
    return {"message": "items fetched successfully", "data": items}
    



# Todo: edit item
@router.put("/update/{id}")
async def update_item_by_id_req(id: str, item: UpdateItemModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="farmer not authorized")
    
    farmer_id = Authorize.get_jwt_subject()
    
    item_in_db = await get_item_by_id(id)
    
    if item_in_db.get("farmer_id") != farmer_id:
        return Response(status_code=403, content="you are not the owner of this item")
    
    item_dict = item.dict(exclude_unset=True)
    updated_item = await update_item_by_id(id, item_dict)
    
    return Response(status_code=200, content={"message": "item updated successfully", "data": updated_item})

# Todo: Update Item Image
@router.put("/update/image/{item_id}")
async def update_item_image_by_id(item_id: str, image: UploadFile = File(...), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="farmer not authorized")
    
    farmer_id = Authorize.get_jwt_subject()
    
    item_in_db = await get_item_by_id(item_id)
    
    if item_in_db.get("farmer_id") != farmer_id:
        return Response(status_code=403, content="you are not the owner of this item")
    
    image_unique_id = f"{farmer_id}/{token_hex(5)}.jpg"
    image_path = f"/mnt/d/api_images/{image_unique_id}" # todo: edit this while on production
    
    try:
        # this makes sure that the directory is made before saving to it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except:
        return Response(status_code=500, content="failed to update item image")
    
    if await update_item_by_id(item_id, {"image": image_unique_id}):
    
        try:
            os.remove(f"/mnt/d/api_images/{item_in_db.get('image')}")
        except:
            pass
    
        return Response(status_code=200, content={"message": "item image updated successfully", "data": {"image": image_unique_id}})
    
    return Response(status_code=500, content="failed to update item image")

# Todo: delete item
@router.delete("/delete/{id}")
async def delete_item_by_id(id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except:
        return Response(status_code=401, content="farmer not authorized")
    
    farmer_id = Authorize.get_jwt_subject()
    
    item_in_db = await get_item_by_id(id)
    
    if item_in_db.get("farmer_id") != farmer_id:
        return Response(status_code=403, content="you are not the owner of this item")
    
    deleted_item = await delete_item_by_id(id)
    
    return Response(status_code=200, content={"message": "item deleted successfully", "data": deleted_item})