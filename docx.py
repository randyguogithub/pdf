from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from docx import Document  # Import python-docx to read .docx files


def generate_pdf_from_docx(docx_path, pdf_path):
    # Load the .docx file
    document = Document(docx_path)

    # Create a PDF object
    pdf = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Set font for the PDF
    pdf.setFont("SourceHanSans-VF", 12)

    # Initialize vertical position
    y_position = height - 50

    # Iterate through paragraphs in the .docx file
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:  # Skip empty lines
            pdf.drawString(50, y_position, text)
            y_position -= 20  # Move to the next line
            if y_position < 50:  # Check if the page is full
                pdf.showPage()  # Add a new page
                pdf.setFont("SourceHanSans-VF", 12)
                y_position = height - 50

    # Save the PDF
    pdf.save()


# Example usage
docx_file = "static/energy.docx"
pdf_file = "static/energy_report_from_docx.pdf"
generate_pdf_from_docx(docx_file, pdf_file)