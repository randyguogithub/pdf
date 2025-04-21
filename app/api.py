from fastapi import APIRouter, Depends, Request,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_async_session
from app.schemas import User, Company, CompanyCreate, InfoCreate
from app.users import current_active_user
import uuid

api_router = APIRouter()
@api_router.get("/mycompany", tags=["company"])
async def get_my_companies(request: Request,session: AsyncSession = Depends(get_async_session),user: User = Depends(current_active_user)):
    result = await session.execute(select(Company).where(Company.created_by==user.email))
    return result.scalars().all()
@api_router.get("/company", tags=["company"])
async def list_companies(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Company))
    return result.scalars().all()

@api_router.get("/user", tags=["users"])
async def list_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@api_router.post("/company", tags=["company"])
async def add_company_api(
    company_data: CompanyCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    company = Company(
        name=company_data.name,
        address=company_data.address,
        created_by=str(user.id),
    )
    session.add(company)
    await session.commit()
    return {"company": company}

@api_router.put("/company", tags=["company"])
async def update_company(
    company_data: CompanyCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
    company_id: str = Query(..., alias="companyid")
):
    # print("Received company_id:", company_id)
    try:
        company_uuid = uuid.UUID(company_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")

    # Fetch the company from the database
    result = await session.execute(select(Company).where(Company.id == company_uuid))
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update the fields if provided
    if company_data.name:
        company.name = company_data.name
    if company_data.address:
        company.address = company_data.address
    await session.commit()
    return {"message": "Company updated successfully", "company": company}

@api_router.delete("/company", tags=["company"])
async def delete_company_api(
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

@api_router.post("/company/info", tags=["company"])
async def add_company_api(
    info_data: CompanyCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    company = Company_info(
        name=company_data.name,
        address=company_data.address,
        created_by=str(user.id),
    )
    session.add(company)
    await session.commit()
    return {"company": company}    