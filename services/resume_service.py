from pathlib import Path
from pypdf import PdfReader
import re


class ResumeService:

    UPLOAD_DIR = Path("data/resumes")
    SKILL_DATABASE = [
        "Python",
        "SQL",
        "Java",
        "C",
        "C++",
        "HTML",
        "CSS",
        "JavaScript",
        "TensorFlow",
        "Keras",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Deep Learning",
        "Power BI",
        "Tableau",
        "Git",
        "GitHub",
        "MySQL",
        "DBMS"
    ]


    @classmethod
    def save_resume(cls, uploaded_file):

        file_path = cls.UPLOAD_DIR / uploaded_file.name

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        return file_path

    @classmethod
    def extract_text(cls, pdf_path):

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text
    @classmethod
    
    def parse_resume(cls, text):

        skills = []

        for skill in cls.SKILL_DATABASE:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text, re.IGNORECASE):
                skills.append(skill)
                

        email_match = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )

        phone_match = re.search(
            r'(\+91[- ]?)?[6-9]\d{9}',
            text
        )

        lines = text.split("\n")

        name = ""

        for line in lines:

            cleaned = line.strip()

            if len(cleaned) > 5:

                name = cleaned
                break
        

        return {
            
            "name": name,
            "email": email_match.group() if email_match else "",
            "phone": phone_match.group() if phone_match else "",
            "skills": skills,
            "projects": [],
            "certifications": []
}
        