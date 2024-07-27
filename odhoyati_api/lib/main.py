from fastapi import FastAPI
from uvicorn import run


from fastapi_jwt_auth import AuthJWT
from security.token_settings import Settings
from core.redis.redis_conn import redis_conn


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    entry = redis_conn.get(jti)
    return entry and entry == "true"


# Replace relative imports with absolute imports
from odhoyati_api.lib.views.auth.auth import router as auth_router
from views.admin.admin import router as admin_router
from views.appointments.appointments import router as appointments_router
from views.items.items import router as items_router
from views.users.users import router as users_router



# App instance
app = FastAPI()

# Including routes
app.include_router(auth_router, prefix='/auth')
app.include_router(admin_router, prefix='/admin')
app.include_router(appointments_router, prefix='/appointments')
app.include_router(items_router, prefix='/items')
app.include_router(users_router, prefix='/users')


# Starting app
if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)


