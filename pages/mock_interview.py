
import streamlit as st
from services.question_service import QuestionService

st.title("🎤 Sai's Interview Prep")

# Get data from session state
resume_text = st.session_state.get("resume_text", "") or ""
jd_text = st.session_state.get("jd_text", "") or ""

resume_skills = st.session_state.get("resume_skills", []) or []
jd_skills = st.session_state.get("jd_skills", []) or []

# Additional skills
st.subheader("Additional Skills")

extra_skills = st.text_input(
    "Enter skills you want to practise",
    placeholder="e.g. Java, C, Spring Boot, Docker",
    help=(
        "Enter comma-separated skills. You can practise these "
        "even if they are not in your resume or job description."
    )
)

# Show existing skills when available
with st.expander("Resume and Job Description Skills", expanded=False):
    st.write("**Resume Skills:**")
    st.write(", ".join(resume_skills) or "No resume skills available.")

    st.write("**JD Skills:**")
    st.write(", ".join(jd_skills) or "No job description skills available.")

# Question counts
st.subheader("Question Settings")

technical_count = st.number_input(
    "Number of Technical Questions",
    min_value=50,
    max_value=200,
    value=50,
    step=5
)

# Project questions are available only when a resume is present
if resume_text.strip():
    project_count = st.number_input(
        "Number of Project Questions",
        min_value=15,
        max_value=50,
        value=20,
        step=5
    )
else:
    project_count = 0
    st.caption(
        "Project questions are available after you upload a resume."
    )

# HR questions are optional
include_hr = st.checkbox(
    "Include HR Interview Questions",
    value=False,
    help="Enable this option if you also want HR interview questions."
)

if include_hr:
    hr_count = st.number_input(
        "Number of HR Questions",
        min_value=15,
        max_value=50,
        value=15,
        step=5
    )
else:
    hr_count = 0

# Require at least one input source
if not resume_text.strip() and not jd_text.strip() and not extra_skills.strip():
    st.info(
        "Upload a resume, provide a job description, "
        "or enter additional skills to generate questions."
    )

# Initialize interview history
if "interview_history" not in st.session_state:
    st.session_state["interview_history"] = []

# Generate questions
if st.button("Generate Questions", type="primary"):

    if not resume_text.strip() and not jd_text.strip() and not extra_skills.strip():
        st.warning(
            "Please provide a resume, job description, or additional skills."
        )

    else:
        with st.spinner("Generating interview questions..."):

            questions = QuestionService.generate_questions(
                resume_text=resume_text,
                jd_text=jd_text,
                technical_count=int(technical_count),
                project_count=int(project_count),
                hr_count=int(hr_count),
                extra_skills=extra_skills,
                include_hr=include_hr
            )

        st.session_state["generated_questions"] = questions

        st.session_state["interview_history"].append(questions)

# Display latest questions
if "generated_questions" in st.session_state:
    st.subheader("Generated Interview Questions")

    st.markdown(st.session_state["generated_questions"])

    st.download_button(
        label="📥 Download Questions",
        data=st.session_state["generated_questions"],
        file_name="mock_interview.txt",
        mime="text/plain"
    )

# Interview history
st.subheader("📜 Interview History")

history = st.session_state.get("interview_history", [])

if history:
    for i, interview in enumerate(reversed(history)):
        with st.expander(f"Interview {len(history) - i}"):
            st.markdown(interview)
else:
    st.caption("Your generated interviews will appear here.")
