class ATSService:

    @classmethod
    def calculate_match(
        cls,
        resume_skills,
        jd_skills
    ):

        matched = []
        missing = []

        for skill in jd_skills:

            if skill in resume_skills:
                matched.append(skill)

            else:
                missing.append(skill)

        score = 0

        if len(jd_skills) > 0:

            score = round(
                len(matched)
                /
                len(jd_skills)
                * 100,
                2
            )

        return {
            "ats_score": score,
            "matched_skills": matched,
            "missing_skills": missing
        }