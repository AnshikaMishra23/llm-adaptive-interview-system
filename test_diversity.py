from services.assessment_generator import (
    generate_assessment
)

from evaluation.question_metrics import (
    diversity_score,
    duplicate_questions
)

questions = generate_assessment(
    "DBMS",
    "Normalization",
    "Medium",
    "MCQ",
    5
)

print()

for q in questions:

    print(q["question"])

print()

print(
    "Diversity Score:",
    diversity_score(
        questions
    )
)

print(
    "Duplicate Questions:",
    duplicate_questions(
        questions
    )
)