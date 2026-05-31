from fpdf import FPDF

def create_pdf(symptoms, duration, medications, doctor_brief):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, "MediBridge AI Report", ln=True)

    pdf.ln(5)

    pdf.multi_cell(0, 10, f"Symptoms: {symptoms}")
    pdf.multi_cell(0, 10, f"Duration: {duration}")
    pdf.multi_cell(0, 10, f"Medications: {medications}")

    pdf.ln(5)

    pdf.multi_cell(
        0,
        10,
        "This report is intended to help patients prepare for doctor consultations."
    )
    pdf.ln(5)

pdf.multi_cell(
    0,
    10,
    "AI Doctor Brief"
)

pdf.multi_cell(
    0,
    10,
    doctor_brief
)

    pdf.output("medical_report.pdf")

    return "medical_report.pdf"
