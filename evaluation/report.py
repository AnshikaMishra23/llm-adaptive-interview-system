from evaluation.metrics import (
    get_metrics
)

from evaluation.question_metrics import (
    diversity_score,
    duplicate_questions,
    average_question_length
)

from evaluation.assessment_metrics import (
    assessment_statistics
)


def generate_report(
    questions
):

    report = {}

    # -------------------------
    # System Performance
    # -------------------------

    report.update(
        get_metrics()
    )

    # -------------------------
    # Question Quality
    # -------------------------

    report["Diversity Score"] = diversity_score(
        questions
    )

    report["Duplicate Questions"] = duplicate_questions(
        questions
    )

    report["Average Question Length"] = (
        average_question_length(
            questions
        )
    )

    # -------------------------
    # Assessment Statistics
    # -------------------------

    report.update(
        assessment_statistics(
            questions
        )
    )

    return report