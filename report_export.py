from fpdf import FPDF

def generate_report(products, companies, image_path, report_path="output/report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Complaint Summary Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Top 10 Products", ln=True)
    for product, count in products.items():
        pdf.cell(200, 10, txt=f"{product}: {count}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Top 10 Companies", ln=True)
    for company, count in companies.items():
        pdf.cell(200, 10, txt=f"{company}: {count}", ln=True)

    pdf.image(image_path, x=10, y=pdf.get_y()+10, w=190)
    pdf.output(report_path)
