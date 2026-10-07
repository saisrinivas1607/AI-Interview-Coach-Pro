import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class QuestionService:

    @classmethod
    def generate_questions(
        cls,
        resume_text,
        jd_text,
        technical_count,
        project_count,
        hr_count
    ):

        model = genai.GenerativeModel("gemini-3.5-flash-lite")
        

        if jd_text:

            prompt = f"""
You are an experienced technical interviewer.

Candidate Resume:
{resume_text}

Job Description:
{jd_text}

Generate:

{technical_count} Technical Questions

{project_count} Project Questions

{hr_count} HR Questions

Rules:
- Analyze the complete resume carefully.
- Analyze the complete job description carefully.
- Give higher weight to job description requirements.
- Ask project-specific questions if projects are present.
- Ask internship-specific questions if internships are present.
- Ask questions about technologies actually used in projects.
- Ask implementation, challenge, optimization, and improvement questions.
- Technical questions should range from beginner to advanced.
- HR questions should assess communication, teamwork, adaptability, and career goals.
- Do not provide answers.
- Format clearly using section headings.
- First identify all projects mentioned in the resume.
- Generate ALL project questions from those identified projects only.
- Mention project names explicitly in the questions.
- Ask about implementation, challenges faced, tools used, optimization, and future improvements.
- Do not generate generic project questions.
Question Difficulty Distribution:

- 50% of questions should be fresher-friendly and easy to moderate.
- 40% of questions should be moderate and implementation-focused.
- 10% of questions can be advanced and challenging.

Guidelines:

Easy Questions:
- Focus on project explanation.
- Ask about technologies used and why they were chosen.
- Cover basic Python, SQL, OOP, DBMS, OS, and Data Structures concepts.
- Ask about challenges faced during development.

Moderate Questions:
- Ask implementation details.
- Ask design decisions and trade-offs.
- Cover API integration, debugging, and database usage.
- Explore project architecture at a high level.

Advanced Questions:
- Ask about scalability, optimization, security, and performance.
- Limit advanced questions to a small percentage.

For project-based questions:
- Prioritize understanding the project, implementation, challenges faced, and technology choices.
- Avoid generating too many architect-level or research-level questions.
- Questions should be suitable for candidates with 0–2 years of experience.

Ensure the overall difficulty is appropriate for campus placements and fresher interviews.
"""

        else:

            prompt = f"""
You are an experienced technical interviewer.

Candidate Resume:
{resume_text}

Generate:

{technical_count} Technical Questions

{project_count} Project Questions

{hr_count} HR Questions

Rules:
- Analyze the complete resume carefully.
- Ask project-specific questions if projects are present.
- Ask internship-specific questions if internships are present.
- Ask questions about technologies actually used in projects.
- Focus heavily on the candidate's projects and experience.
- Technical questions should range from beginner to advanced.
- HR questions should assess communication, teamwork, adaptability, and career goals.
- Do not provide answers.
- Format clearly using section headings.
"""

        try:
            response = model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"Error generating questions:\n\n{str(e)}"