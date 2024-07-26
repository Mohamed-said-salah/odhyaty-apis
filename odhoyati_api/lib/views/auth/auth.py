from fastapi.routing import APIRouter


router = APIRouter()

# todo: register
@router.post("/register")
async def register():
    return {"message": "welcome to register"}

# todo: login
@router.post("/login")
async def login():
    return {"message": "welcome to login"}

# todo: logout
@router.delete("/logout")
async def logout():
    return {"message": "welcome to logout"}

