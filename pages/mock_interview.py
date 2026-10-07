import streamlit as st
from services.question_service import QuestionService

st.title("🎤 AI Mock Interview")

resume_text = st.session_state.get(
    "resume_text",
    ""
)

jd_text = st.session_state.get(
    "jd_text",
    ""

)

resume_skills = st.session_state.get(
    "resume_skills",
    []
)

jd_skills = st.session_state.get(
    "jd_skills",
    []
)

st.subheader("Resume Skills")
st.write(", ".join(resume_skills))

st.subheader("JD Skills")
st.write(", ".join(jd_skills))

technical_count = st.number_input(
    "Technical Questions",
    min_value=1,
    max_value=100,
    value=5
)

project_count = st.number_input(
    "Project Questions",
    min_value=1,
    max_value=20,
    value=3
)

hr_count = st.number_input(
    "HR Questions",
    min_value=1,
    max_value=30,
    value=2
)

if not resume_skills:
    st.warning(
        "Please upload a resume first."
    )
    st.stop()

if not jd_skills:
    st.info(
        "No Job Description found. Questions will be generated based only on the resume."
    )

# Initialize interview history
if "interview_history" not in st.session_state:
    st.session_state["interview_history"] = []

# Generate questions
if st.button("Generate Questions"):

    with st.spinner(
        "Generating interview questions..."
    ):

       questions = QuestionService.generate_questions(
            resume_text,
            jd_text,
            technical_count,
            project_count,
            hr_count
    )
    

    st.session_state["generated_questions"] = questions

    st.session_state["interview_history"].append(
            questions
        )

# Show latest generated questions
if "generated_questions" in st.session_state:

    st.subheader(
        "Generated Interview Questions"
    )

    st.markdown(
        st.session_state["generated_questions"]
    )

# Download button
if "generated_questions" in st.session_state:

    st.download_button(
        label="📥 Download Questions",
        data=st.session_state["generated_questions"],
        file_name="mock_interview.txt",
        mime="text/plain"
    )

# Interview History
st.subheader("📜 Interview History")

history = st.session_state.get(
    "interview_history",
    []
)

for i, interview in enumerate(history):

    with st.expander(
        f"Interview {i+1}"
    ):
        st.markdown(interview)

# Debug
st.write("Resume Skills in Session:")
st.write(
    st.session_state.get("resume_skills")
)

st.write("JD Skills in Session:")
st.write(
    st.session_state.get("jd_skills")
)