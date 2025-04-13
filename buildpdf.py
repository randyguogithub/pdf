from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
pdfmetrics.registerFont(TTFont('Black-CN', 'fonts/NotoSerifCJKsc-VF.ttf'))
# 自定义样式配置

def load_styles_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        style_data = json.load(file)

    styles = getSampleStyleSheet()

    for style_name, style_attrs in style_data.items():
        # Convert color names to ReportLab color objects
        if "textColor" in style_attrs:
            style_attrs["textColor"] = getattr(colors, style_attrs["textColor"], colors.black)

        # Add the style to the stylesheet
        styles.add(ParagraphStyle(name=style_name, **style_attrs))

    return styles
def page1(template_data, styles):
    elements = []
    # -----------------  page  1 -----------------
    # 主标题
    elements.append(Spacer(1, 4*cm))
    elements.append(Paragraph(template_data["document_title"], styles["MainTitle"]))
    elements.append(Spacer(1, 3*cm))
    elements.append(Paragraph(template_data["document_subtitle"], styles["SubTitle"]))
    elements.append(Spacer(1, 3*cm))

    # section1
    for para in template_data["section1"]:
        elements.append(Paragraph(para, styles["section1"]))
        elements.append(Spacer(1, 0.2*cm))
    # section2
    elements.append(Spacer(1, 3*cm))
    for para in template_data["section2"]:
        elements.append(Paragraph(para, styles["section2"]))
        elements.append(Spacer(1, 0.3*cm))
    elements.append(PageBreak())
     # page break
    elements.append(Spacer(1, 3*cm))
    elements.append(PageBreak())
    return elements
def numofdoc(linestring,fontSize=12):
    if fontSize == 14:
       dots="."*(68-len(linestring))
    else:
        dots="."*(95-len(linestring))
    return dots

def page2(template_data, styles):
    elements = []
    elements.append(Paragraph(template_data["agendaheader"], styles["agendaheader"]))
    for agenda in template_data["agendas"]:
        elements.append(Paragraph(agenda["agenda"].format(numofdoc(agenda["agenda"],14)), styles["agenda"]))
        for para in agenda["agendasub"]:
            elements.append(Paragraph(para.format(numofdoc(para)), styles["agendasub"]))
        elements.append(Spacer(1, 0.1*cm))
    # elements.append(Paragraph(template_data["agenda2"].format(numofdoc(template_data["agenda2"],14)), styles["agenda1"]))
    # for para in template_data["agenda2sub"]:
    #     elements.append(Paragraph(para.format(numofdoc(para)), styles["agenda2sub"]))
    # elements.append(Spacer(1, 0.1*cm))
    return elements

def build_dynamic_pdf(template_data, styles, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=A4,topMargin=2*cm,bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm)
    elements = []
    # elements.extend(page1(template_data, styles))
    elements.extend(page2(template_data, styles))

    doc.build(elements)
    


styles = getSampleStyleSheet()

styles = load_styles_from_json("data/styles.json") 

# 数据输入示例
with open('data/templatedata.json', 'r', encoding='utf-8') as file:
    template_data = json.load(file)
    build_dynamic_pdf(template_data, styles, "static/dynamic_pdf.pdf")


# def add_table(template_data):
#     # 修改后的header_data
#     header_data = [
#         [
#             Image(template_data["company_logo"], width=3*cm, height=1.5*cm),
#             Paragraph(
#                 f"<b>公司名称:</b> {template_data['company_name']}<br/>"
#                 f"<b>地  址:</b> {template_data['company_address']}",
#                 styles["ChineseHeader"]  # 使用自定义中文样式
#             )
#         ]
#     ]
#     header_table = Table(header_data, colWidths=[4*cm, 12*cm])
#     header_table.setStyle(TableStyle([
#         ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
#         ('BOX', (0,0), (-1,-1), 1, colors.grey),
#         ('FONTNAME', (0,0), (-1,0), 'Black-CN')
#     ]))
#     # elements.append(header_table)
#     # 客户信息表格
#     client_table = Table([
#         ["客户名称", template_data["client_name"]],
#         ["合同编号", template_data["contract_id"]]
#     ], colWidths=[4*cm, 12*cm], hAlign='LEFT')
#     client_table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
#         ('FONTNAME', (0,0), (-1,0), 'Black-CN')
#     ]))
#     elements.append(client_table)
#     elements.append(Spacer(1, 1*cm))

#     # 动态数据表（从JSON数据生成）
#     main_table = Table(template_data["dynamic_table_data"])
#     main_table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')),
#         ('TEXTCOLOR', (0,0), (-1,0), colors.white),
#         ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#         ('FONTNAME', (0,0), (-1,0), 'Black-CN'),
#         ('GRID', (0,0), (-1,-1), 1, colors.black)
#     ]))
#     elements.append(main_table)
#     elements.append(Spacer(1, 1*cm))

#     return header_table
#     # ----------------- 页脚构建 -----------------
# def add_footer(canvas, doc):
#     canvas.saveState()
#     canvas.setFont('Black-CN', 9)
#     canvas.drawString(2*cm, 1*cm, 
#                         f"{template_data['footer_text']} | 页码: {doc.page}")
#     canvas.restoreState()
