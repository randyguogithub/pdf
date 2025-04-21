from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select
from fastapi_users.password import PasswordHelper
from app.schemas import Base, User
import uuid


DATABASE_URL = "sqlite+aiosqlite:///./data/aiso.db"

# class CompanyCreate(BaseModel):
#     name: Optional[str] = "name" 
#     address: Optional[str] = "address"

# class InfoCreate(BaseModel):
#     id: str
#     info: str | None = None
#     scope: str | None = None
#     status: str | None = None
#     purpose: str | None = None
#     general: str | None = None
#     org: str | None = None
#     principles: str | None = None
#     product: str | None = None

# class Base(DeclarativeBase):
#     pass

# class Company_info(Base): #公司概况
#     __tablename__ = "company_info"
#     id =Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     company_id = Column(UUID(as_uuid=True))
#     scope = Column(String, default="能源评审的范围")
#     org = Column(String, default="能源管理体系组织架构")
#     period = Column(String, default="能源评审的统计期")
#     team= Column(String, default="能源评审的统计期")
#     responsiblity = Column(String, default="领导小组职责")
#     rules = Column(String, default="评审的主要方法")
#     law = Column(String, default="能源评审的依据")
#     principles = Column(String, default="能源方针")
#     product = Column(String, default="公司主要产品")
#     purpose = Column(String, default="能源评审的目的")
#     info = Column(String, default="公司主要概况")
#     updated_by = Column(String, default="user")
#     created_at = Column(DateTime, server_default=func.now())
    
# class Company(Base):
#     __tablename__ = "company"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String)
#     address = Column(String)
#     created_by = Column(String, default="admin")
#     auditor = Column(String, default="admin")
#     status = Column(String, default="draft")
#     created_at = Column(DateTime, server_default=func.now())
#     pass

# class User(SQLAlchemyBaseUserTableUUID, Base):
#     __tablename__ = "user"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String)
#     email = Column(String, unique=True, nullable=False)
#     role = Column(String)
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)
#     is_verified = Column(Boolean, default=False)
#     lastlogin = Column(DateTime, server_default=func.now())
#     pass

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