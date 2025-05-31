from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from app.db import get_async_session
from app.schemas import User

templates = Jinja2Templates(directory="templates")
admin_router = APIRouter()

@admin_router.get("/users", response_class=HTMLResponse)
async def admin_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    # Fetch all users from the database
    result = await session.execute(select(User))
    users = result.scalars().all()
    print("users:", users)
    return templates.TemplateResponse("admin_user.html", {"request": request, "users": users})

@admin_router.get("/companies", response_class=HTMLResponse)
async def admin_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    # Fetch all users from the database
    result = await session.execute(select(Company))
    companies = result.scalars().all()
    # print("users:", users)
    return templates.TemplateResponse("admin_company.html", {"request": request, "companies": companies})    