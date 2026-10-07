from services.question_service import QuestionService

print("Starting Gemini test...")

result = QuestionService.generate_questions(
    "Python SQL Machine Learning",
    "Python SQL Git Power BI"
)

print("Response received:")
print(result)