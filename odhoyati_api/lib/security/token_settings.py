from pydantic import BaseModel
from datetime import timedelta
from .keys import AUTH_JWT_SECRET_KEY

class Settings(BaseModel):
    authjwt_secret_key: str = AUTH_JWT_SECRET_KEY
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=60)
    fresh_expires: int = timedelta(minutes=10)
