import streamlit as st

from services.resume_service import ResumeService
from services.jd_service import JDService
from services.ats_service import ATSService

st.title("🎯 ATS Match")

jd_text = st.text_area(
    "Paste Job Description",
    value=st.session_state.get("jd_text", ""),
    height=300
)

if st.button("Analyze JD"):
    st.session_state["jd_text"] = jd_text

    jd_result = JDService.analyze_jd(
        jd_text
    )

    # Save JD skills for Mock Interview
    st.session_state["jd_skills"] = jd_result["required_skills"]
    st.session_state["jd_text"] = jd_text

    st.subheader("Detected JD Skills")

    st.json(jd_result)

    resume_skills = st.session_state.get(
        "resume_skills",
        []
    )

    ats_result = ATSService.calculate_match(
        resume_skills,
        jd_result["required_skills"]
    )

    st.subheader("ATS Result")

    st.json(ats_result)
if "jd_result" in st.session_state:

    st.subheader("Detected JD Skills")

    st.json(
        st.session_state["jd_result"]
    )

if "ats_result" in st.session_state:

    st.subheader("ATS Result")

    st.json(
        st.session_state["ats_result"]
    )