import streamlit as st
from wire_client import get_medical_context, get_job_result
from report_generator import create_pdf


# =========================
# AI FUNCTION
# =========================
def generate_doctor_brief(symptoms, duration, medications):
    return f"""
Patient reports: {symptoms}

Duration: {duration}

Current Medications: {medications if medications else "None reported"}

Key Discussion Focus:
• Review symptom progression
• Evaluate symptom severity
• Assess medication effectiveness
• Consider additional diagnostic tests if necessary
"""


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="MediBridge AI",
    page_icon="🏥",
    layout="wide"
)

# =========================
# HERO UI (UNCHANGED)
# =========================
st.markdown("""
<div class="hero">
    <h1>🏥 MediBridge AI</h1>
    <p>AI-Powered Doctor Visit Preparation Assistant</p>
    <p>Powered by Anakin Wire + PubMed</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# INPUT UI
# =========================
col1, col2 = st.columns(2)

with col1:
    symptoms = st.text_area("🩺 Symptoms", placeholder="Headache, dizziness, fatigue...")

with col2:
    medications = st.text_area("💊 Current Medications", placeholder="Paracetamol, Vitamin D...")

duration = st.selectbox(
    "⏳ Duration",
    ["1 Day", "2-3 Days", "1 Week", "2 Weeks", "1 Month+"]
)

# =========================
# BUTTON LOGIC (FIXED FLOW)
# =========================
if st.button("🚀 Generate Medical Report", use_container_width=True):

    if not symptoms:
        st.warning("Please enter symptoms.")
        st.stop()

    # STEP 1: AI BRIEF (MOVED UP → FIXED CRASH)
    doctor_brief = generate_doctor_brief(symptoms, duration, medications)

    # STEP 2: SHOW UI IMMEDIATELY
    st.markdown("## 🤖 AI Doctor Brief")
    st.text_area("Doctor Brief", doctor_brief, height=180)

    # STEP 3: METRICS
    st.markdown("## 📋 Patient Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Symptoms Entered", len(symptoms.split()))

    with c2:
        st.metric("Duration", duration)

    with c3:
        st.metric("Status", "Ready")

    # STEP 4: PDF GENERATION (NOW SAFE)
    pdf_file = create_pdf(symptoms, duration, medications, doctor_brief)

    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="MediBridge_Report.pdf",
            mime="application/pdf"
        )

    # STEP 5: LOADING + PUBMED (INSIDE BUTTON FLOW)
    with st.spinner("🔬 Searching medical literature using Anakin Wire..."):
        try:
            job = get_medical_context(symptoms)
            result = get_job_result(job["poll_url"])

            st.success("Medical literature retrieved successfully!")

            st.markdown("## 🔬 Medical Literature")

            articles = result["data"]["data"]["articles"]

            st.success(f"Found {len(articles)} relevant PubMed articles")

            for article in articles:
                with st.expander(article["title"]):
                    st.write("**Journal:**", article.get("journal", "N/A"))
                    st.write("**Published:**", article.get("pub_date", "N/A"))
                    st.write("**PMID:**", article.get("pmid", "N/A"))

        except Exception as e:
            st.warning(f"No articles found or error occurred: {e}")

    # STEP 6: FOOTER
    st.divider()

    st.caption("Powered by Anakin Wire • PubMed • Streamlit")

    st.info(
        "Disclaimer: This tool does not diagnose medical conditions. "
        "It helps organize information before consulting healthcare professionals."
    )
