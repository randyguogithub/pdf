from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from app.db import get_async_session
from app.db import User

templates = Jinja2Templates(directory="templates")
admin_router = APIRouter()

@admin_router.get("/users", tags=["users"])
async def list_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    # print(result.scalars().all())
    return result.scalars().all()

@admin_router.get("/admin/user", tags=["admin"])
async def admin_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    # Fetch all users from the database
    result = await session.execute(select(User))
    users = result.scalars().all()
    print("users:", users)
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})