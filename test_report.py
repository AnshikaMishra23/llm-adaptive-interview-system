from services.assessment_generator import (
    generate_assessment
)

from evaluation.report import (
    generate_report
)

questions = generate_assessment(
    "DBMS",
    "Normalization",
    "Medium",
    "Mixed",
    10
)

report = generate_report(
    questions
)

print()

for key, value in report.items():

    print(
        f"{key}: {value}"
    )