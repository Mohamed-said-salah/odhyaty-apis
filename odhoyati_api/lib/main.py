from fastapi import FastAPI
from uvicorn import run

# Replace relative imports with absolute imports
from views.appointments.appointments import router as appointments_router
from views.auth.auth import router as auth_router
from views.items.items import router as items_router
from views.users.users import router as users_router



# App instance
app = FastAPI()

# Including routes
app.include_router(appointments_router, prefix='/appointments')
app.include_router(auth_router, prefix='/auth')
app.include_router(items_router, prefix='/items')
app.include_router(users_router, prefix='/users')


# Starting app
if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000)


