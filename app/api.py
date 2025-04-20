from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_async_session
from app.db import User, Company, CompanyCreate, CompanyInfo
from app.users import current_active_user
import uuid

api_router = APIRouter()

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
        created_by=user.email,
    )
    session.add(company)
    await session.commit()
    return {"company": company}

@api_router.put("/company", tags=["company"])
async def update_company(
    company_data: CompanyInfo,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        # Convert company_id to a UUID object
        company_uuid = uuid.UUID(company_data.id)
    except ValueError:
        # Raise an error if the company_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid company ID format")

    # Fetch the company from the database
    result = await session.execute(select(Company).where(Company.id == company_uuid))
    company = result.scalars().first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Update the fields if provided
    if company_data.scope:
        company.scope = company_data.scope
    if company_data.purpose:
        company.purpose = company_data.purpose
    if company_data.info:
        company.info = company_data.info
    if company_data.general:
        company.general = company_data.general
    if company_data.org:
        company.org = company_data.org
    if company_data.principles:
        company.principles = company_data.principles
    if company_data.product:
        company.product = company_data.product
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