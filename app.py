def generate_doctor_brief(symptoms, duration, medications):
    brief = f"""
Patient reports: {symptoms}

Duration: {duration}

Current Medications: {medications if medications else "None reported"}

Key Discussion Focus:
• Review symptom progression
• Evaluate symptom severity
• Assess medication effectiveness
• Consider additional diagnostic tests if necessary
"""

    return brief
import streamlit as st
from wire_client import get_medical_context
from wire_client import get_job_result
from report_generator import create_pdf

st.set_page_config(
page_title="MediBridge AI",
page_icon="🏥",
layout="wide"
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    background: linear-gradient(90deg, #2563eb, #0ea5e9);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 1rem;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 0;
}

.hero p {
    font-size: 1.1rem;
    opacity: 0.9;
}

.stButton > button {
    width: 100%;
    height: 3rem;
    border-radius: 10px;
    font-weight: bold;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1> MediBridge AI</h1>
    <p>AI-Powered Doctor Visit Preparation Assistant</p>
    <p>Powered by Anakin Wire + PubMed</p>
</div>
""", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)

with col1:
    symptoms = st.text_area(
        "🩺 Symptoms",
        placeholder="Headache, dizziness, fatigue..."
    )

with col2:
    medications = st.text_area(
        "💊 Current Medications",
        placeholder="Paracetamol, Vitamin D..."
    )

duration = st.selectbox(
    "⏳ Duration",
    [
        "1 Day",
        "2-3 Days",
        "1 Week",
        "2 Weeks",
        "1 Month+"
    ]
)
if st.button("🚀 Generate Medical Report", use_container_width=True):
    
    if not symptoms:
        st.warning("Please enter symptoms.")
        st.stop()
pdf_file = create_pdf(
    symptoms,
    duration,
    medications,
    doctor_brief
)

with open(pdf_file, "rb") as file:
    st.download_button(
        label="📄 Download PDF Report",
        data=file,
        file_name="MediBridge_Report.pdf",
        mime="application/pdf"
    )

with st.spinner("Searching medical literature using Anakin Wire..."):

    try:
        job = get_medical_context(symptoms)
        result = get_job_result(job["poll_url"])

        st.success("✅ Medical literature retrieved successfully!")

        st.markdown("## 📋 Doctor Visit Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Symptoms Entered", len(symptoms.split()))

        with c2:
            st.metric("Duration", duration)

        with c3:
            st.metric("Status", "Ready")
        doctor_brief = generate_doctor_brief(
    symptoms,
    duration,
    medications
)
        st.markdown("## 🤖 AI Doctor Brief")

        st.text_area(
        "Doctor Brief",
        doctor_brief,
        height=180
)

        st.markdown("### 📄 Patient Summary")

        st.markdown(f"""
        **Symptoms:** {symptoms}

        **Duration:** {duration}

        **Current Medications:** {medications if medications else "Not Provided"}

        """)
        st.markdown("### 🗣 Suggested Discussion Points")

        st.markdown("""


* Describe when symptoms started
* Explain symptom severity
* Mention symptom frequency
* Discuss medication usage
* Mention recent lifestyle changes
  """)

        st.markdown("### ❓ Questions To Ask Your Doctor")

        st.markdown("""
  

1. What could be causing these symptoms?
2. Are any tests recommended?
3. Are there warning signs requiring urgent care?
4. What treatment options are available?
5. What lifestyle changes may help?
   """)

   
        st.markdown("## 🔬 Medical Literature")

        try:
            articles = result["data"]["data"]["articles"]

            st.success(f"Found {len(articles)} relevant PubMed articles")

            for article in articles:

                with st.expander(article["title"]):

                    st.write(
                        "**Journal:**",
                        article.get("journal", "N/A")
                    )

                    st.write(
                        "**Published:**",
                        article.get("pub_date", "N/A")
                    )

                    st.write(
                        "**PMID:**",
                        article.get("pmid", "N/A")
                    )

        except:
            st.warning("No articles found.")

        st.divider()

        st.caption(
            "Powered by Anakin Wire • PubMed • Streamlit"
        )

        st.info(
            "Disclaimer: This tool does not diagnose medical conditions. "
            "It helps patients organize information before consulting healthcare professionals."
        )

    except Exception as e:
        st.error(f"Error: {e}")
   
