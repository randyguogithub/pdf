from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from app.db import get_async_session
from app.db import User, Company, CompanyCreate
from app.users import current_active_user
import uuid

templates = Jinja2Templates(directory="templates")
company_router = APIRouter()

@company_router.get("/company", tags=["company"])
async def list_companies(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Company))
    return result.scalars().all()

@company_router.get("/company/detail/{company_id}", tags=["company"])
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
    return templates.TemplateResponse("detail_company.html", {"request": request,"company": company_dict})
@company_router.get("/company/add",response_class=HTMLResponse)
async def add_company_form(request: Request):
    return templates.TemplateResponse("add_company.html", {"request": request})

@company_router.post("/company", tags=["company"])
async def add_company_api(
    company_data: CompanyCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    company = Company(
        name=company_data.name,
        address=company_data.address,
        created_by=user.email,
    )
    session.add(company)
    await session.commit()
    return {"company": company}
@company_router.get("/admin/company", tags=["admin"])
async def admin_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    # Fetch all users from the database
    result = await session.execute(select(Company))
    companies = result.scalars().all()
    # print("users:", users)
    return templates.TemplateResponse("admin_company.html", {"request": request, "companies": companies})