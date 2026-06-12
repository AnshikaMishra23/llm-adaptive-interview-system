from services.assessment_generator import generate_assessment

questions = generate_assessment(
    "DBMS",
    "Normalization",
    "Easy",
    "Mixed",
    6
)

print(questions)