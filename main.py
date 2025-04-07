from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import pdfkit
import os

app = FastAPI()

# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize SQLite database
DB_NAME = "data.db"

def init_db():
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

init_db()

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

@app.get("/download/{company_id}")
async def download_pdf(company_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM companies WHERE id = ?", (company_id,))
    company = cursor.fetchone()
    conn.close()

    if not company:
        return {"error": "Company not found"}

    # Generate PDF content
    pdf_content = f"""
    <h1>Company Information</h1>
    <p><strong>Name:</strong> {company[1]}</p>
    <p><strong>Description:</strong> {company[2]}</p>
    <p><strong>Address:</strong> {company[3]}</p>
    """

    # Save PDF to a file
    pdf_file = f"static/company_{company_id}.pdf"
    options = {'page-size': 'A4', 'margin-top': '0mm'}
    pdfkit.from_string(pdf_content,pdf_file , options=options)

    # Serve the PDF file
    return FileResponse(pdf_file, media_type="application/pdf", filename=f"company_{company_id}.pdf")