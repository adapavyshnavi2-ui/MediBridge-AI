import streamlit as st
from wire_client import get_medical_context, get_job_result
from report_generator import create_pdf



def generate_doctor_brief(symptoms, duration, medications):
    return f"""
Patient reports: {symptoms}

Duration: {duration}

Current Medications: {medications if medications else "None reported"}

Key Clinical Assessment:
• Review symptom progression
• Evaluate severity trends
• Assess medication response
• Recommend further diagnostic evaluation if needed
"""



st.set_page_config(
    page_title="MediBridge-AI",
    page_icon="🏥",
    layout="wide"
)


st.markdown("""
<div style="
    padding: 26px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    margin-bottom: 20px;
">
    <h1 style="margin:0;"> MediBridge Hospital OS</h1>
    <p style="opacity:0.7;">AI-Powered Electronic Health Record & Clinical Decision Support System</p>
</div>
""", unsafe_allow_html=True)


st.markdown("## 🧾 Patient EHR Intake System")

col1, col2 = st.columns([2, 2])

with col1:
    symptoms = st.text_area("🩺 Chief Complaints", placeholder="Headache, dizziness, fatigue...", height=120)

with col2:
    medications = st.text_area(" Current Medications", placeholder="Paracetamol, Vitamin D...", height=120)

duration = st.selectbox(
    " Symptom Duration",
    ["1 Day", "2–3 Days", "1 Week", "2 Weeks", "1 Month+"]
)

st.divider()


if st.button(" Run Clinical Assessment", use_container_width=True):

    if not symptoms:
        st.warning("Please enter patient symptoms")
        st.stop()

    
    doctor_brief = generate_doctor_brief(symptoms, duration, medications)

    severity_score = min(100, len(symptoms.split()) * 12)

    if severity_score >= 70:
        risk_level = "HIGH RISK"
        color = "#ef4444"
        alert = "🚨 Immediate clinical attention recommended"
    elif severity_score >= 40:
        risk_level = "MODERATE RISK"
        color = "#f59e0b"
        alert = "⚠️ Monitor closely and consider evaluation"
    else:
        risk_level = "LOW RISK"
        color = "#22c55e"
        alert = "🟢 Stable condition"

    
    st.markdown("##  Clinical Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Symptoms Load", len(symptoms.split()))
    c2.metric("Duration", duration)
    c3.metric("Risk Level", risk_level)
    c4.metric("Status", "Processed")

   
    st.markdown("##  Triage Assessment")

    st.markdown(f"""
    <div style="
        padding:16px;
        border-radius:14px;
        background:{color}20;
        border:1px solid {color};
        color:{color};
        font-weight:600;
    ">
    {alert}
    </div>
    """, unsafe_allow_html=True)

   
    st.markdown("## Symptom Progression Model")

    import plotly.graph_objects as go

    timeline = [
        severity_score * 0.4,
        severity_score * 0.6,
        severity_score * 0.8,
        severity_score
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=timeline,
        mode="lines+markers",
        line=dict(width=3)
    ))

    fig.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Time Progression",
        yaxis_title="Symptom Severity Index"
    )

    st.plotly_chart(fig, use_container_width=True)

    
    st.markdown("##  AI Clinical Decision Support")

    st.markdown(f"""
    <div style="
        padding:18px;
        border-radius:16px;
        background:#f8fafc;
        border:1px solid #e2e8f0;
        line-height:1.6;
    ">
    {doctor_brief}
    </div>
    """, unsafe_allow_html=True)

    
    pdf_file = create_pdf(symptoms, duration, medications, doctor_brief)

    with open(pdf_file, "rb") as file:
        st.download_button(
            "📄 Generate Patient Report (PDF)",
            file,
            file_name="Hospital_OS_Report.pdf"
        )

    
    with st.spinner("🔬 Running clinical literature scan..."):
        try:
            job = get_medical_context(symptoms)
            result = get_job_result(job["poll_url"])

            st.markdown("## 🔬 Evidence-Based Medicine Feed")

            articles = result["data"]["data"]["articles"]

            for article in articles:
                with st.expander("📄 " + article["title"]):
                    st.write("Journal:", article.get("journal", "N/A"))
                    st.write("Published:", article.get("pub_date", "N/A"))
                    st.write("PMID:", article.get("pmid", "N/A"))

        except Exception as e:
            st.warning(f"Clinical database unavailable: {e}")


st.divider()

st.caption("MediBridge Hospital OS • Clinical Decision Support System.Anakin API")

st.info(
    "⚠️ This system assists clinical decision-making and does not replace professional diagnosis."
)
