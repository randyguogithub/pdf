from fastapi import APIRouter, Depends, Request,HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from app.db import get_async_session
from app.db import User, Company, CompanyCreate, CompanyInfo
from app.users import current_active_user,decode_jwt_token
import uuid
from fastapi import Query, HTTPException

templates = Jinja2Templates(directory="templates")
company_router = APIRouter()
# SECRET_KEY = "your_secret_key"  # Replace with your actual secret key
# ALGORITHM = "HS256"  # Replace with your actual algorithm

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
    else:
        return templates.TemplateResponse("my_company.html", {"request": request, "companies": companies, "user": username})

@company_router.get("/edit/{company_id}", response_class=HTMLResponse)
async def get_company(company_id: str,  # Add company_id as a parameter
    request: Request,
    session: AsyncSession = Depends(get_async_session)):
    # print("company_id:", company_id)
    try:
        # Convert company_id to a UUID object
        company_uuid = uuid.UUID(company_id)
    except ValueError:
        # Raise an error if the company_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid company ID format")

    result = await session.execute(select(Company).where(Company.id == company_uuid))
    company = result.scalars().first()
    if result is None:
        companys= {"message": "Company not found"}
    # print("company:", company)    
    # return company
    company_dict = {
        "id": str(company.id),
        "name": company.name,
        "address": company.address,
        "info": company.info,
    }    
    return templates.TemplateResponse("edit_company.html", {"request": request,"company": company_dict})

# @company_router.get("/detail/{company_id}",response_class=HTMLResponse)
# async def get_company(company_id: str,  # Add company_id as a parameter
#     request: Request,
#     session: AsyncSession = Depends(get_async_session)):
#     # print("company_id:", company_id)
#     try:
#         # Convert company_id to a UUID object
#         company_uuid = uuid.UUID(company_id)
#     except ValueError:
#         # Raise an error if the company_id is not a valid UUID
#         raise HTTPException(status_code=400, detail="Invalid company ID format")

#     result = await session.execute(select(Company).where(Company.id == company_uuid))
#     company = result.scalars().first()
#     if result is None:
#         companys= {"message": "Company not found"}
#     # print("company:", company)    
#     # return company
#     company_dict = {
#         "id": str(company.id),
#         "name": company.name,
#         "address": company.address,
#         "info": company.info,
#     }    
#     return templates.TemplateResponse("detail_company.html", {"request": request,"company": company_dict})

# @company_router.get("/new",response_class=HTMLResponse)
# async def add_company_form(request: Request):
#     return templates.TemplateResponse("add_company.html", {"request": request})

@company_router.get("/info",response_class=HTMLResponse)
async def add_info_form(request: Request):
    return templates.TemplateResponse("add_info.html", {"request": request})


