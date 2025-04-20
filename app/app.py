from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from app.api import api_router
from app.pages import pages_router
from app.company import company_router
from app.db import User, create_db_and_tables
from app.admin import admin_router
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from fastapi.staticfiles import StaticFiles
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
# Include routes from pages.py
# Get the current directory of the app.py file
BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory="{}/static".format(BASE_DIR)), name="static")
app.include_router(pages_router)
app.include_router(api_router,prefix="/api/v1")
app.include_router(admin_router,prefix="/admin")
app.include_router(company_router,prefix="/company")
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/v1", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/v1",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/v1",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/v1",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/v1",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}