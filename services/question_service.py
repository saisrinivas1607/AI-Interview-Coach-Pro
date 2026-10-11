
import os
import re

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
        hr_count,
        extra_skills="",
        include_hr=False
    ):

        model = genai.GenerativeModel("gemini-3.5-flash-lite")

        # Normalize optional inputs
        resume_text = resume_text or ""
        jd_text = jd_text or ""
        extra_skills = extra_skills or ""

        has_resume = bool(resume_text.strip())
        has_jd = bool(jd_text.strip())
        has_extra_skills = bool(extra_skills.strip())

        skills_only_mode = (
            not has_resume
            and not has_jd
            and has_extra_skills
        )

        if not has_resume and not has_jd and not has_extra_skills:
            return (
                "Please upload a resume, provide a job description, "
                "or enter additional skills."
            )

        # Build input sections
        resume_section = (
            f"Candidate Resume:\n{resume_text}"
            if has_resume
            else "No resume provided."
        )

        jd_section = (
            f"Job Description:\n{jd_text}"
            if has_jd
            else "No job description provided."
        )

        extra_skills_section = (
            f"""
Additional skills requested by the user:
{extra_skills}

Include these as practice topics even if they are absent
from the resume and job description.
"""
            if has_extra_skills
            else "No additional skills provided."
        )

        # Identify skills dynamically before calculating question count
        try:
            skill_prompt = f"""
Identify distinct technical skills relevant to interview questions
from the following resume, job description, and additional skills.

RESUME:
{resume_text if has_resume else "Not provided."}

JOB DESCRIPTION:
{jd_text if has_jd else "Not provided."}

ADDITIONAL SKILLS:
{extra_skills if has_extra_skills else "None."}

Rules:
- Include relevant programming languages, frameworks, libraries,
  databases, platforms, tools, and technical concepts.
- Include skills explicitly required by the job description.
- Include manually entered skills.
- Do not invent skills or treat unrelated words as technical skills.
- Remove duplicates and equivalent names.
- Return only a numbered list of distinct skills, one skill per line.
- Do not include explanations or introductory text.
"""

            skill_response = model.generate_content(skill_prompt)
            skill_text = skill_response.text or ""

            detected_skills = []
            for line in skill_text.splitlines():
                line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()
                if line and line.lower() not in {
                    "none", "no skills", "no relevant skills"
                }:
                    if line.lower() not in {
                        skill.lower() for skill in detected_skills
                    }:
                        detected_skills.append(line)

        except Exception as e:
            return (
                "Could not identify skills for question generation. "
                "Please try again.\n\n"
                f"Details: {str(e)}"
            )

        # Calculate technical question minimums
        if has_resume:
            # 20 questions for each distinct detected skill
            technical_count = max(
                int(technical_count),
                20 * len(detected_skills)
            )

        elif skills_only_mode:
            # At least 50 questions for manually entered skills only
            technical_count = max(int(technical_count), 50)

        elif has_jd:
            # JD-only mode: at least 15 questions per detected skill
            technical_count = max(
                int(technical_count),
                15 * len(detected_skills)
            )

        else:
            technical_count = max(int(technical_count), 15)

        # Optional HR questions
        generate_hr = bool(include_hr)

        if generate_hr:
            hr_count = max(int(hr_count), 15)
        else:
            hr_count = 0

        # Project questions require an actual resume
        generate_projects = has_resume and int(project_count) > 0

        if not generate_projects:
            project_count = 0

        # HR instructions
        hr_instructions = (
            f"""
Generate exactly {hr_count} HR questions.
Keep them in a separate HR QUESTIONS section.
Cover communication, teamwork, adaptability, strengths,
career goals, and handling challenges.
"""
            if generate_hr
            else """
Do not generate HR questions or include an HR section.
"""
        )

        # Project instructions
        project_instructions = (
            f"""
Generate exactly {project_count} project questions.
Use only projects actually mentioned in the resume.
Mention the actual project name in each question.
Cover implementation, tools, contributions, challenges,
debugging, and possible improvements.
Do not invent projects or implementations.
"""
            if generate_projects
            else """
Do not generate project questions.
"""
        )

        # Interview mode
        if skills_only_mode:
            mode_instructions = """
MODE: SKILLS-ONLY PRACTICE

Generate technical questions using the manually entered skills.
Do not assume the candidate has professional experience.
Do not generate project questions.
"""
        else:
            mode_instructions = """
MODE: RESUME / JOB PREPARATION

Use the available resume, job description, and additional skills.
Prioritize job requirements when a JD is available.
Do not claim the candidate has experience with skills appearing
only in the JD or Additional Skills input.
"""

        # Main question-generation prompt
        prompt = f"""
You are an experienced technical interviewer preparing questions
for freshers and candidates with 0-2 years of experience.

{resume_section}

{jd_section}

{extra_skills_section}

{mode_instructions}

IDENTIFIED TECHNICAL SKILLS:
{chr(10).join("- " + skill for skill in detected_skills)
    if detected_skills else "- Use the relevant topics in the provided inputs."}

QUESTION COUNTS:
- Total technical questions required: {technical_count}
- Project questions: {project_count if generate_projects else 0}
- HR questions: {hr_count if generate_hr else 0}

MANDATORY PER-SKILL REQUIREMENT:

{"- Generate AT LEAST 20 technical questions for EACH identified skill." if has_resume else ""}
{"- Generate AT LEAST 15 technical questions for EACH identified skill." if has_jd and not has_resume else ""}
{"- Generate AT LEAST 50 technical questions in total." if skills_only_mode else ""}
- Cover every identified skill.
- Keep questions under the correct skill heading.
- Do not count project or HR questions as technical questions.
- Do not count one question under multiple skills.
- The total technical question target is {technical_count}.
- Do not stop after generating questions for only the first few skills.

DIFFICULTY STRUCTURE:

Organize questions into these sections:

# EASY QUESTIONS
# MEDIUM QUESTIONS
# HARD QUESTIONS

Target approximately:
- Easy: 50%
- Medium: 35%
- Hard: 15%

TOPIC-WISE ORGANIZATION:

- Create a separate heading for every identified technical skill.
- Include all identified skills, not just the most important ones.
- Distribute each skill's questions across Easy, Medium, and Hard.
- Keep topics dynamic; do not restrict them to a predefined list.
- Avoid duplicate and nearly identical questions.

EASY:
Fundamentals, definitions, syntax, basic coding, and common use cases.

MEDIUM:
Practical coding, implementation, debugging, and design decisions.

HARD:
Challenging problem-solving, optimization, performance, and trade-offs.
Keep difficulty appropriate for fresher interviews.

SKILL SOURCE RULES:
- Resume skills are skills listed by the candidate.
- JD-only skills are requirements, not verified experience.
- Additional skills are practice topics, not verified experience.
- Do not invent candidate skills or project experience.

PROJECT RULES:
{project_instructions}

HR RULES:
{hr_instructions}

OUTPUT FORMAT:


OUTPUT FORMAT:

Organize the entire response BY SKILL, not by difficulty.

For each detected technical skill, use this exact structure:

# [SKILL NAME]

## Easy Questions
1. Question
2. Question

## Medium Questions
1. Question
2. Question

## Hard Questions
1. Question
2. Question

Then move to the next skill and repeat the same structure.

Rules:
- Every skill must have its own Easy, Medium, and Hard sections.
- Keep questions under the correct skill.
- Preserve the required total number of questions for each skill.
- Do not combine all Easy, Medium, or Hard questions into global sections.
- Keep project questions in a separate Project Questions section.
- Include HR questions in a separate HR Questions section only
  when the user enables the HR checkbox.
- Do not provide answers.


[Include Project Questions only when applicable.]
[Include HR Questions only when enabled.]

FINAL CHECKS:
- Cover every identified technical skill.
- When a resume is provided, generate at least 20 technical questions
  per identified skill.
- When only a JD is provided, generate at least 15 per identified skill.
- In skills-only mode, generate at least 50 technical questions total.
- Include at least 15 HR questions when HR is enabled.
- Never generate project questions without a resume.
- Do not include HR questions when disabled.
- Do not provide answers.
"""

        try:
            response = model.generate_content(prompt)

            if response.text:
                return response.text

            return "No questions were generated. Please try again."

        except Exception as e:
            return f"Error generating questions:\n\n{str(e)}"
