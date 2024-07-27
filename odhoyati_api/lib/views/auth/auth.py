from fastapi.routing import APIRouter

from users_auth import router as auth_router
from farmers_auth import router as farmers_router

router = APIRouter()


router.include_router(auth_router, prefix='/users')
router.include_router(farmers_router, prefix='/farmers')