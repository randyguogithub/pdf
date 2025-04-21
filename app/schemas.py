import uuid
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

class CompanyCreate(BaseModel):
    name: Optional[str] = "name" 
    address: Optional[str] = "address"

class InfoCreate(BaseModel):
    info: Optional[str] = "公司主要概况" 
    scope: Optional[str] = "能源评审的范围" 
    purpose: Optional[str] = "能源评审的目的" 
    org: Optional[str] = "能源管理体系组织架构" 
    principles: Optional[str] = "能源方针" 
    product: Optional[str] = "公司主要产品" 
    period : Optional[str] ="能源评审的统计期"
    team: Optional[str] ="成立评审领导小组"
    responsiblity : Optional[str] ="领导小组职责"
    rules: Optional[str] ="评审的主要方法"
    law : Optional[str] ="能源评审的依据"
    created_by : Optional[str] ="user"

class Base(DeclarativeBase):
    pass

class Company_info(Base): #公司概况
    __tablename__ = "company_info"
    id =Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True))
    scope = Column(String, default="能源评审的范围")
    org = Column(String, default="能源管理体系组织架构")
    period = Column(String, default="能源评审的统计期")
    team = Column(String, default="成立评审领导小组")
    responsiblity = Column(String, default="领导小组职责")
    rules = Column(String, default="评审的主要方法")
    law = Column(String, default="能源评审的依据")
    principles = Column(String, default="能源方针")
    product = Column(String, default="公司主要产品")
    purpose = Column(String, default="能源评审的目的")
    info = Column(String, default="公司主要概况")
    updated_by = Column(String, default="user")
    created_at = Column(DateTime, server_default=func.now())
    
class Company(Base):
    __tablename__ = "company"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    address = Column(String)
    created_by = Column(String, default="admin")
    auditor = Column(String, default="admin")
    status = Column(String, default="draft")
    created_at = Column(DateTime, server_default=func.now())
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    role = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    lastlogin = Column(DateTime, server_default=func.now())
    pass
    