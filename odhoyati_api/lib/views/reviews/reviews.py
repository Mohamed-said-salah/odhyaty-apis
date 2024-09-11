
from fastapi.routing import APIRouter

from fastapi import  Response, Depends, File, UploadFile, Form, Body

import shutil

import os

from fastapi_jwt_auth import AuthJWT

from typing import Optional, Union

import json

from secrets import token_hex

from core.schemas.reviews_schema import ReviewSchema, UpdateReviewModel

from controllers.crud.reviews import (
    create_review,
    get_reviews_by_farmer_id,
    get_reviews_by_user_id,
    get_reviews_by_item_id,
    get_review_by_order_id,
    get_review_by_id,
    update_review,
    get_all_reviews,
    query_reviews_by_filter,
    delete_review,
)

from controllers.crud.users import (
    get_user_by_id,
    
)

from controllers.crud.farmers import (
    get_farmer_by_id,
    update_farmer_by_id
)

from controllers.crud.items import (
    get_item_by_id,
)

from controllers.crud.orders import (
    get_order_by_id,
)

# from   ..auth.helpers.check_user_type import is_farmer, is_admin, is_super_admin

router = APIRouter()


@router.post("/add")
async def add_review(review: ReviewSchema = Body(...), Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        return Response(status_code=401, content=json.dumps({"message": "user not authorized", "error": str(e)}))
    
    user_id = Authorize.get_jwt_subject()
    
    user = await get_user_by_id(user_id)
    user_part = {
        "name": user["name"],
    }
    farmer = await get_farmer_by_id(review.farmer_id)
    farmer_part = {
        "name": farmer["name"],
    }
    item = await get_item_by_id(review.item_id)
    item_part = {
        "image": item["image"],
        "title": item["title"],
        "category": item["category"]
    }
    
    order =  await get_order_by_id(review.order_id)
    
    if not order:
        return Response(status_code=400, content="review not found")

    review.user_id = user_id
    review.part_of_farmer = farmer_part
    review.part_of_user =   user_part
    review.part_of_item =   item_part


    review_dict = await create_review(review.dict())
        
    if not review_dict:
        return Response(status_code=400, content="review not added")
    

    new_rate = ((farmer["rating"] + review.rate) / 2) if farmer["rating"]  else  review.rate
    await update_farmer_by_id(review.farmer_id, {"rating": new_rate})
    
    review_dict["created_at"] = review.created_at.isoformat()
    review_dict["updated_at"] = review.updated_at.isoformat()

    return {"message": "review added successfully", "data": review_dict}


# edit review
# todo: edit review


# delete review
# todo: delete the review 