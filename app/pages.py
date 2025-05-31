from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import APIRouter

templates = Jinja2Templates(directory="templates")

pages_router = APIRouter()

@pages_router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@pages_router.get("/login",response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@pages_router.get("/register",response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
@pages_router.get("/index",response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
      
@pages_router.get("/audit",response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("audit.html", {"request": request})