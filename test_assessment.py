from services.assessment_generator import generate_assessment

questions = generate_assessment(
    "DBMS",
    "Normalization",
    "Easy",
    "Descriptive",
    2
)

print(questions)