from collections import Counter


def assessment_statistics(questions):

    stats = {}

    stats["Total Questions"] = len(questions)

    type_counter = Counter()

    total_marks = 0

    for question in questions:

        type_counter[
            question["question_type"]
        ] += 1

        total_marks += question["marks"]

    stats["MCQ Questions"] = type_counter["MCQ"]

    stats["MSQ Questions"] = type_counter["MSQ"]

    stats["Descriptive Questions"] = type_counter[
        "Descriptive"
    ]

    stats["Total Marks"] = total_marks

    return stats