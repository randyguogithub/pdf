from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import sqlite3
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import os

app = FastAPI()

# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize SQLite database
DB_NAME = "data/data.db"

def init_db_fonts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    pdfmetrics.registerFont(TTFont('SourceHanSans-VF', 'fonts/SourceHanSans-VF.ttf'))

init_db_fonts()

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    address: str = Form(...)
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (name, description, address) VALUES (?, ?, ?)", (name, description, address))
    conn.commit()
    conn.close()
    return templates.TemplateResponse("form.html", {"request": request, "message": "Company added successfully!"})

@app.get("/companies", response_class=HTMLResponse)
async def list_companies(request: Request):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("companies.html", {"request": request, "companies": companies})

@app.get("/company/{company_id}", response_class=HTMLResponse)
async def company_detail(request: Request, company_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
    company = cursor.fetchone()
    conn.close()
    if company is None:
        return templates.TemplateResponse("companies.html", {"request": request, "message": "Company not found!"})
    return templates.TemplateResponse("detail.html", {"request": request, "company": company})

def generate_energy_report(filename="energy_report.pdf", company=[]):
    # 创建PDF对象
    pdf = canvas.Canvas("static/{}".format(filename), pagesize=A4)
    width, height = A4

    # 标题样式
    pdf.setFont("SourceHanSans-VF", 18)
    pdf.drawCentredString(width/2, height-80, company[1])

    pdf.setFont("SourceHanSans-VF", 14)
    pdf.drawCentredString(width/2, height-120, "初始能源评审报告")
    # 元数据
    pdf.setFont("SourceHanSans-VF", 12)
    pdf.drawCentredString(width/2, height-140, f"编制：能源管理团队")
    pdf.drawCentredString(width/2, height-160, f"审核：陈海")
    pdf.drawCentredString(width/2, height-180, f"批准：兰升")
    pdf.drawCentredString(width/2, height-200, f"编制日期：2024年01月01日")
    pdf.drawCentredString(width/2, height-220, f"修订日期：2024年11月21日")
    pdf.drawString(80, height-320, company[2])
    pdf.drawString(80, height-340, company[3])
    pdf.save()


@app.get("/download/{company_id}")
async def download_pdf(company_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
    company = cursor.fetchone()
    conn.close()
    if company is None:
        return {"error": "Company not found"}
    # 执行生成
    pdf_file = f"static/company_{company_id}.pdf"
    filename = f"company_{company_id}.pdf"
    generate_energy_report(filename=filename , company=company)

    # Serve the PDF file
    return FileResponse(pdf_file, media_type="application/pdf", filename=f"company_{company_id}.pdf")