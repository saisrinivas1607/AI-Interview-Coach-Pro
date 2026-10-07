import streamlit as st
from services.resume_service import ResumeService

st.title("📄 Resume Analysis")

st.write("Upload your resume to begin analysis.")
if "resume_skills" in st.session_state:
    st.success("Resume already loaded")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    saved_path = ResumeService.save_resume(
        uploaded_file
    )

    extracted_text = ResumeService.extract_text(
        saved_path
    )
    st.session_state["resume_text"] = extracted_text
    result = ResumeService.parse_resume(
        extracted_text
    )

    # Save skills for other pages
    
    st.session_state["resume_skills"] = result["skills"]
    st.session_state["resume_name"] = result["name"]
    st.session_state["resume_email"] = result["email"]
    st.session_state["resume_projects"] = result.get("projects", [])
    st.session_state["resume_certifications"] = result.get("certifications", [])

    st.success(
        "Resume uploaded and parsed successfully!"
    )

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        extracted_text,
        height=400
    )

    st.subheader("Detected Resume Information")

    st.json(result)