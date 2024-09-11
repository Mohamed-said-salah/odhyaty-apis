from fastapi import APIRouter

from .users import router as users_router
from .admin import router as admin_router
from .farmers import router as farmers_router
from .orders import router as orders_router

router = APIRouter()


router.include_router(router=admin_router, prefix="/admins")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=farmers_router, prefix="/farmers")
router.include_router(router=orders_router, prefix="/orders")