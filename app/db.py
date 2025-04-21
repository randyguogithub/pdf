from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select
from fastapi_users.password import PasswordHelper
from app.schemas import Base, User
import uuid
from fastapi_users.db import SQLAlchemyUserDatabase

DATABASE_URL = "sqlite+aiosqlite:///./data/aiso.db"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
     # Add default admin use
    async with async_session_maker() as session:
            query = await session.execute(select(User).where(User.email == "admin@aiso.com"))
            admin_user = query.scalars().first()
            # print("Admin user result:", admin_user)
            if not admin_user:
                password_helper = PasswordHelper()
                hashed_password = password_helper.hash("admin")
                admin_user = User(
                    email="admin@aiso.com",
                    name = 'admin',
                    hashed_password=hashed_password,
                    is_active=True,
                    is_superuser=True,
                    is_verified=True,
                    role="admin"
                )
                session.add(admin_user)
                await session.commit()
                print("Default admin user created: admin@aiso.com")
            else:
                print("Admin user already exists.")
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)