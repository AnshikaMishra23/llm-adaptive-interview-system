from evaluation.adaptive_metrics import (
    adaptive_learning_metrics
)

report = adaptive_learning_metrics(
    "anshika"
)

print()

for key, value in report.items():

    print(f"{key}: {value}")