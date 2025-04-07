from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generate_energy_report():
    # 创建PDF对象
    pdf = canvas.Canvas("energy_report.pdf", pagesize=A4)
    width, height = A4

    # 标题样式
    pdf.setFont("SourceHanSans-VF", 18)
    pdf.drawCentredString(width/2, height-80, "广东阿尔派电力科技股份有限公司")

    pdf.setFont("SourceHanSans-VF", 14)
    pdf.drawCentredString(width/2, height-120, "初始能源评审报告")
    # pdf.drawString(0, height-100, "")  # Add a blank line

    # 元数据
    pdf.setFont("SourceHanSans-VF", 12)
    pdf.drawCentredString(width/2, height-140, f"编制：能源管理团队")
    # pdf.drawString(0, height-100, "")  # Add a blank line
    pdf.drawCentredString(width/2, height-160, f"审核：陈海")
    # pdf.drawString(0, height-100, "")  # Add a blank line
    pdf.drawCentredString(width/2, height-180, f"批准：兰升")
    # pdf.drawString(0, height-100, "")  # Add a blank line
    pdf.drawCentredString(width/2, height-200, f"编制日期：2024年01月01日")
    pdf.drawString(0, height-100, "")  # Add a blank line
    pdf.drawCentredString(width/2, height-220, f"修订日期：2024年11月21日")
    pdf.drawString(0, height-100, "")  # Add a blank line
    # 目录（示例）
    # positions = [100, 600, 100, 580, 100, 560, 100, 540]
    # items = ["能源评审目的", "评审范围", "能源管理现状", "法律法规合规性"]
    # for i, item in enumerate(items):
        # pdf.drawString(positions[0], positions[1]-i*20, item)
        # pdf.drawString(positions[2], positions[3]-i*20, f"{i+1}.00")

    # 能源消耗表格
    # data = [
    #     ["能源类型", "消耗量", "折标系数", "综合能耗占比"],
    #     ["电力", "675,064 kWh", "0.1229 kgce/kWh", "52.86%"],
    #     ["柴油", "8,503 kg", "1.4714 kgce/kg", "6.66%"],
    #     ["液化气", "1,812.5 kg", "1.7143 kgce/kg", "1.98%"]
    # ]
    # table = Table(data, colWidths=[5*cm, 6*cm, 6*cm, 6*cm])
    # table.setStyle(TableStyle([
    #     ('BACKGROUND', (0,0), (-1,0), colors.grey),
    #     ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    #     ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    #     ('FONTNAME', (0,0), (-1,0), 'SourceHanSans-VF'),
    #     ('BOTTOMPADDING', (0,0), (-1,0), 12),
    #     ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    #     ('GRID', (0,0), (-1,-1), 1, colors.black),
    # ]))
    # table.wrapOn(pdf, width, height)
    # table.drawOn(pdf, 50, 400)

    # 插入能流图（需准备图片）
    # pdf.drawImage("energy_flowchart.png", 50, 200, width=500, height=150)

    pdf.save()

# Register fonts from the main fonts folder
pdfmetrics.registerFont(TTFont('SourceHanSans-VF', 'fonts/SourceHanSans-VF.ttf'))
pdfmetrics.registerFont(TTFont('SourceHanSansHC-VF', 'fonts/SourceHanSansHC-VF.ttf'))
pdfmetrics.registerFont(TTFont('SourceHanSansK-VF', 'fonts/SourceHanSansK-VF.ttf'))
pdfmetrics.registerFont(TTFont('SourceHanSansSC-VF', 'fonts/SourceHanSansSC-VF.ttf'))
pdfmetrics.registerFont(TTFont('SourceHanSansTC-VF', 'fonts/SourceHanSansTC-VF.ttf'))

# 执行生成
generate_energy_report()