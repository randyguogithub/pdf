from fastapi import APIRouter, Depends, Request,HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from app.schemas import User, Company, CompanyCreate, InfoCreate, Company_info
from app.db import get_async_session
from app.users import current_active_user,decode_jwt_token
import uuid


templates = Jinja2Templates(directory="templates")
company_router = APIRouter()

@company_router.get("/", response_class=HTMLResponse)
async def list_mycompanies(
    request: Request, 
    session: AsyncSession = Depends(get_async_session),
    token: str = Query(..., alias="token")
    ):
    user=decode_jwt_token(token)
    result = await session.execute(select(Company).where(Company.created_by == user.get('sub')))
    companies = result.scalars().all()
    if len(companies) ==0:
        return templates.TemplateResponse("new_company.html", {"request": request})
        #  return templates.TemplateResponse("new_company.html", {"request": request, "token": token})
    else:
        # return templates.TemplateResponse("my_company.html", {"request": request, "companies": companies, "token": token})
        return templates.TemplateResponse("my_company.html", {"request": request, "companies": companies})

@company_router.get("/update", response_class=HTMLResponse)
async def update_company(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    company_id: str = Query(..., alias="companyid")):
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")
    result = await session.execute(select(Company).where(Company.company_id == company_uuid))
    company = result.scalars().first()
    if result is None:
        companys= {"message": "Company not found"}

    company_dict = {
        "id": company.id,
        "name": company.name,
        "address": company.address
    }     
    return templates.TemplateResponse("update_company.html", {"request": request,"company": company_dict})

@company_router.get("/info",response_class=HTMLResponse)
async def add_info_form(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    company_id: str = Query(..., alias="companyid")
    ):
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")
    result = await session.execute(select(Company_info).where(Company_info.company_id == company_uuid))
    info = result.scalars().first()

    if info is None:
        return templates.TemplateResponse("add_info.html", {"request": request,"companyid": company_uuid})

    company_dict = {
        "id": info.id,
        "product": info.product,
        "scope": info.scope
    }     
    return templates.TemplateResponse("update_info.html", {"request": request,"company": company_dict})


