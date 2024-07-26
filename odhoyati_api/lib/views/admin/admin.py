
from fastapi.routing import APIRouter


router = APIRouter()


# todo: add
@router.post("/add")
async def add():
    return {"message": "welcome to add"}

# todo: remove
@router.delete("/remove")
async def remove():
    return {"message": "welcome to remove"}

# todo: login
@router.post("/login")
async def login():
    return {"message": "welcome to login"}

# todo: logout
@router.delete("/logout")
async def logout():
    return {"message": "welcome to logout"}


# todo: get admins
@router.get("/admins")
async def get_admins():
    return {"message": "welcome to get admins"}