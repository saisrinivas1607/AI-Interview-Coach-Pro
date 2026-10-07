import re


class JDService:

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
    def analyze_jd(cls, jd_text):

        detected_skills = []

        for skill in cls.SKILL_DATABASE:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, jd_text, re.IGNORECASE):
                detected_skills.append(skill)

        return {
            "required_skills": detected_skills
        }