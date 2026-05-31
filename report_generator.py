from fpdf import FPDF
from datetime import datetime


def create_pdf(symptoms, duration, medications, doctor_brief):
    pdf = FPDF()
    pdf.add_page()

    # ===== HEADER =====
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "MediBridge AI - Clinical Summary", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(5)

    # ===== PATIENT DETAILS =====
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Patient Information", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, f"Symptoms: {symptoms}")
    pdf.multi_cell(0, 8, f"Duration: {duration}")
    pdf.multi_cell(0, 8, f"Medications: {medications}")

    pdf.ln(5)

    # ===== AI BRIEF =====
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Clinical Brief", ln=True)

    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, doctor_brief)

    pdf.ln(5)

    # ===== DISCLAIMER =====
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Medical Disclaimer", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(
        0,
        6,
        "This report is AI-generated to assist clinical consultation only. "
        "It does not constitute a medical diagnosis and should not replace a qualified doctor."
    )

    # ===== OUTPUT =====
    filename = "medibridge_clinical_report.pdf"
    pdf.output(filename)

    return filename
