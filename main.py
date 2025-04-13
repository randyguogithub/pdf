from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from sqlclient import DBclint
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import uuid  # Import the uuid module
import os
from fastapi.responses import RedirectResponse

app = FastAPI()
db=DBclint()
# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

pdfmetrics.registerFont(TTFont('SourceHanSans-VF', 'fonts/SourceHanSans-VF.ttf'))
def verify_user_logged_in(request: Request):
    user_logged_in = request.cookies.get("user_logged_in")
    if not user_logged_in and "register" not in str(request.url):
        return False
    return True
@app.get("/audit", response_class=HTMLResponse)
async def show_page(request: Request):
    # Usage in the $SELECTION_PLACEHOLDER$
    if not verify_user_logged_in(request):
        return RedirectResponse(url="/login")
    
    url = str(request.url)
    return templates.TemplateResponse(
        "audit.html",
        {
            "mdoc": url.split("#")[-1] if "#" in url else "docs",
            "request": request,
            "username": request.cookies.get("username")
        }
    )

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    sql = "SELECT * FROM users WHERE username = ? AND password = ?"
    params = (username, password)
    user = db.run_sql(sql, params)
    if len(user) > 0:
        usr=user[0]
        print(usr)
        response = RedirectResponse(url="/company", status_code=303)
        response.set_cookie(key="user_logged_in",value="true")
        response.set_cookie(key="userid", value=usr[0])
        response.set_cookie(key="username",value=username)
        return response
    else:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid username or password"}
        )

@app.get("/register", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user_id = str(uuid.uuid4())  # Generate a UUID
    sql = "INSERT INTO users (id,username, email, password) VALUES (?, ?, ?, ?)"
    params = (user_id, username, email, password)
    cursor = db.run_sql(sql, params)
    return templates.TemplateResponse("index.html", {"request": request, "message": "User registered successfully! Please log in."})


@app.post("/company", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    address: str = Form(...)
):
    if not verify_user_logged_in(request):
        return RedirectResponse(url="/login")

    company_id = str(uuid.uuid4())  # Generate a UUID
    created_by = request.cookies.get("userid")
    sql = "INSERT INTO companies (id,name,  address,created_by) VALUES (?,?, ?,?)"
    params = (company_id,name, address,created_by)
    company = db.run_sql(sql, params)
    return templates.TemplateResponse("company.html", {"request": request, "message": "Company added successfully!"})

@app.get("/admin", response_class=HTMLResponse)
async def list_companies(request: Request):
    if not verify_user_logged_in(request):
        return RedirectResponse(url="/login")
    sql = "SELECT * FROM users"
    users = db.run_sql(sql)
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})

@app.get("/company", response_class=HTMLResponse)
async def list_companies(request: Request):
    if not verify_user_logged_in(request):
        return RedirectResponse(url="/login")
    sql = "SELECT * FROM companies where created_by = ? "
    params = (request.cookies.get("userid"),)
    companies = db.run_sql(sql, params)
    return templates.TemplateResponse("company.html", {"request": request, "companies": companies})

# @app.get("/company/{company_id}", response_class=HTMLResponse)
# async def company_detail(request: Request, company_id: int):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
#     company = cursor.fetchone()
#     conn.close()
#     if company is None:
#         return templates.TemplateResponse("company.html", {"request": request, "message": "Company not found!"})
#     return templates.TemplateResponse("detail.html", {"request": request, "company": company})

# def generate_energy_report(filename="energy_report.pdf", company=[]):
#     # 创建PDF对象
#     pdf = canvas.Canvas("static/{}".format(filename), pagesize=A4)
#     width, height = A4

#     # 标题样式
#     pdf.setFont("SourceHanSans-VF", 18)
#     pdf.drawCentredString(width/2, height-80, company[1])

#     pdf.setFont("SourceHanSans-VF", 14)
#     pdf.drawCentredString(width/2, height-120, "初始能源评审报告")
#     # 元数据
#     pdf.setFont("SourceHanSans-VF", 12)
#     pdf.drawCentredString(width/2, height-140, f"编制：能源管理团队")
#     pdf.drawCentredString(width/2, height-160, f"审核：陈海")
#     pdf.drawCentredString(width/2, height-180, f"批准：兰升")
#     pdf.drawCentredString(width/2, height-200, f"编制日期：2024年01月01日")
#     pdf.drawCentredString(width/2, height-220, f"修订日期：2024年11月21日")
#     pdf.drawString(80, height-320, company[2])
#     pdf.drawString(80, height-340, company[3])
#     pdf.save()


# @app.get("/download/{company_id}")
# async def download_pdf(company_id: int):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
#     company = cursor.fetchone()
#     conn.close()
#     if company is None:
#         return {"error": "Company not found"}
#     # 执行生成
#     pdf_file = f"static/company_{company_id}.pdf"
#     filename = f"company_{company_id}.pdf"
#     generate_energy_report(filename=filename , company=company)

#     # Serve the PDF file
#     return FileResponse(pdf_file, media_type="application/pdf", filename=f"company_{company_id}.pdf")