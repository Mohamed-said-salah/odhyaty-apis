from fastapi.routing import APIRouter

from .users_auth import router as users_auth_router
from .farmers_auth import router as farmers_auth_router

router = APIRouter()


router.include_router(users_auth_router, prefix='/users')
router.include_router(farmers_auth_router, prefix='/farmers')