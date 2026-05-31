import streamlit as st
from wire_client import get_medical_context, get_job_result
from report_generator import create_pdf


# =========================
# AI FUNCTION (UNCHANGED)
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
# 🍎 APPLE HEALTH HEADER (UPGRADED)
# =========================
st.markdown("""
<div style="
    padding: 26px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    margin-bottom: 18px;
">
    <h1 style="margin:0; font-size:34px;">MediBridge AI</h1>
    <p style="opacity:0.7; margin-top:6px;">
        Apple Health Style Clinical Intelligence System
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT SECTION (CLEAN APPLE CARDS)
# =========================
st.markdown("### Patient Intake")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        padding:16px;
        border-radius:18px;
        background:#f8fafc;
        border:1px solid #e2e8f0;
    ">
    """, unsafe_allow_html=True)

    symptoms = st.text_area("🩺 Symptoms", placeholder="Headache, dizziness, fatigue...")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        padding:16px;
        border-radius:18px;
        background:#f8fafc;
        border:1px solid #e2e8f0;
    ">
    """, unsafe_allow_html=True)

    medications = st.text_area("💊 Current Medications", placeholder="Paracetamol, Vitamin D...")

    st.markdown("</div>", unsafe_allow_html=True)

duration = st.selectbox(
    "⏳ Duration",
    ["1 Day", "2-3 Days", "1 Week", "2 Weeks", "1 Month+"]
)

st.divider()

# =========================
# BUTTON (UNCHANGED FUNCTIONALITY)
# =========================
if st.button("🚀 Generate Medical Report", use_container_width=True):

    if not symptoms:
        st.warning("Please enter symptoms.")
        st.stop()

    # =========================
    # AI BRIEF
    # =========================
    doctor_brief = generate_doctor_brief(symptoms, duration, medications)

    st.markdown("### AI Clinical Summary")

    st.markdown(f"""
    <div style="
        padding:18px;
        border-radius:18px;
        background:rgba(248,250,252,0.95);
        border:1px solid #e2e8f0;
        line-height:1.6;
    ">
    {doctor_brief}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # METRICS DASHBOARD (APPLE STYLE)
    # =========================
    st.markdown("### Patient Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Symptoms Count", len(symptoms.split()))

    with c2:
        st.metric("Duration", duration)

    with c3:
        st.metric("Status", "Ready")

    # =========================
    # PDF (UNCHANGED)
    # =========================
    pdf_file = create_pdf(symptoms, duration, medications, doctor_brief)

    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download Medical Report",
            data=file,
            file_name="MediBridge_Report.pdf",
            mime="application/pdf"
        )

    # =========================
    # PUBMED SECTION (CLEAN APPLE STYLE)
    # =========================
    with st.spinner("🔬 Fetching medical literature..."):
        try:
            job = get_medical_context(symptoms)
            result = get_job_result(job["poll_url"])

            st.markdown("### Clinical Evidence Feed")

            articles = result["data"]["data"]["articles"]

            st.success(f"{len(articles)} relevant studies found")

            for article in articles:
                with st.expander("📄 " + article["title"]):
                    st.write("Journal:", article.get("journal", "N/A"))
                    st.write("Published:", article.get("pub_date", "N/A"))
                    st.write("PMID:", article.get("pmid", "N/A"))

        except Exception as e:
            st.warning(f"Medical literature unavailable: {e}")

# =========================
# FOOTER (UNCHANGED)
# =========================
st.divider()

st.caption("Powered by Anakin Wire • PubMed • Streamlit")

st.info(
    "Disclaimer: This tool does not diagnose medical conditions. "
    "It helps organize information before consulting healthcare professionals."
)
