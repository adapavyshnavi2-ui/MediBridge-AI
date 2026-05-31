from fpdf import FPDF
from datetime import datetime


def safe_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")


def create_pdf(symptoms, duration, medications, doctor_brief):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("MediBridge AI - Clinical Summary"), ln=True)

    pdf.set_font("Arial", size=10)
    pdf.cell(
        0,
        8,
        safe_text(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
        ln=True
    )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, safe_text("Patient Information"), ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, safe_text(f"Symptoms: {symptoms}"))
    pdf.multi_cell(0, 8, safe_text(f"Duration: {duration}"))
    pdf.multi_cell(0, 8, safe_text(f"Medications: {medications}"))

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, safe_text("AI Clinical Brief"), ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, safe_text(doctor_brief))

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, safe_text("Disclaimer"), ln=True)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(
        0,
        6,
        safe_text(
            "This AI-generated report is for informational purposes only. "
            "It is not a medical diagnosis."
        )
    )

    filename = "medibridge_report.pdf"
    pdf.output(filename)

    return filename
