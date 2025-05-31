from fastapi import APIRouter, Depends, Request,HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from app.schemas import User, Company, CompanyCreate, InfoCreate, Company_info
from app.db import get_async_session
from app.users import current_active_user,decode_jwt_token
import uuid
import markdown
from markdown.extensions.toc import TocExtension
import re

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
    else:
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
    result = await session.execute(select(Company).where(Company.id == company_uuid))
    company = result.scalars().first()
    if result is None:
        companys= {"message": "Company not found"}
    print(company)
    company_info = {
        "id": company.id,
        "name": company.name,
        "address": company.address
    }     
    return templates.TemplateResponse("update_company.html", {"request": request,"company": company_info})

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




def generate_toc(html_content: str) -> str:
    """从HTML内容生成目录"""
    toc_pattern = re.compile(r'<h([1-6]) id="(.*?)">(.*?)</h\1>', re.DOTALL)
    toc_items = []
    
    for match in toc_pattern.finditer(html_content):
        level, anchor, title = match.groups()
        toc_items.append({
            "level": int(level),
            "anchor": anchor,
            "title": title.strip()
        })
    
    # 生成嵌套的目录HTML
    toc_html = '<div class="toc">\n<ul>\n'
    current_level = 0
    
    for item in toc_items:
        if item['level'] > current_level:
            toc_html += '<ul>\n' * (item['level'] - current_level)
        elif item['level'] < current_level:
            toc_html += '</li>\n</ul>\n' * (current_level - item['level'])
        else:
            toc_html += '</li>\n'
        
        toc_html += f'<li><a href="#{item["anchor"]}">{item["title"]}</a>'
        current_level = item['level']
    
    toc_html += '</li>\n</ul>\n</div>'
    return toc_html

@company_router.get("/detail", response_class=HTMLResponse)
async def detail_company(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    company_id: str = Query(..., alias="companyid")
):
    # 从数据库获取Markdown内容
    try:
        company_uuid = uuid.UUID(company_id)
        result = await session.execute(select(Company_info).where(Company_info.company_id == company_uuid))
        print("company_uuid:", company_uuid)
        print("result:", result)
        article = result.scalars().first()
        if not article:
            return HTMLResponse(content="<h1>Article not found</h1>", status_code=404)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")
    md_content = "### markdown content\n 转换Markdown为HTML并生成目录锚点 \n ## 转换Markdown为HTML并生成目录锚点 \n ### No content available"
    # 转换Markdown为HTML并生成目录锚点
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'fenced_code',
            'tables',
            'codehilite',
            TocExtension(toc_depth="2-6", title="Table of Contents")
        ]
    )
    
    # 生成目录结构
    toc_html = generate_toc(html_content)
    
    # 渲染模板
    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "title": "title of the article",
            "toc": toc_html,
            "content": html_content
        }
    )
        # return templates.TemplateResponse("update_info.html", {"request": request,"company": company_dict})

# @company_router.get("/detail", response_class=HTMLResponse)
# async def detail_company(
#     request: Request,
#     session: AsyncSession = Depends(get_async_session),
#     company_id: str = Query(..., alias="companyid")
# ):
#     try:
#         company_uuid = uuid.UUID(company_id)
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid company ID format")
#     result = await session.execute(select(Company_info).where(Company_info.company_id == company_uuid))
#     info = result.scalars().first()

#     if info is None:
#         raise HTTPException(status_code=404, detail="Company info not found")

#     company_detail = {
#         "id": info.id,
#         "product": info.product,
#         "scope": info.scope,
#         "purpose": getattr(info, "purpose", ""),
#         "period": getattr(info, "period", "")
#     }
#     return templates.TemplateResponse("detail_company.html", {"request": request, "company": company_detail})
