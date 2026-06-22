from services.evaluator import evaluate_answer
from utils.helper import extract_score


def evaluate_assessment(
    questions,
    user_answers
):

    total_score = 0
    max_score = 0

    results = []

    for question in questions:

        qid = question["question_id"]

        qtype = question["question_type"]

        marks = question["marks"]

        max_score += marks

        user_answer = user_answers.get(qid)

        # =====================
        # MCQ
        # =====================

        if qtype == "MCQ":

            correct_answer = question["correct_answer"]

            is_correct = (
                user_answer == correct_answer
            )

            if is_correct:
                total_score += marks

            results.append(
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "correct": is_correct,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer
                }
            )

        # =====================
        # MSQ
        # =====================

        elif qtype == "MSQ":

            correct_answer = question["correct_answer"]

            is_correct = (
                set(user_answer)
                ==
                set(correct_answer)
            )

            if is_correct:
                total_score += marks

            results.append(
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "correct": is_correct,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer
                }
            )

        # =====================
        # DESCRIPTIVE
        # =====================

        elif qtype == "Descriptive":

            evaluation = evaluate_answer(
                question["question"],
                user_answer
            ) 

            score = extract_score(
                evaluation
            )

            descriptive_marks = round(
                (score / 10) * marks
            )

            total_score += descriptive_marks

            results.append(
                {
                    "question_id": qid,
                    "question_type": qtype,
                    "correct": None,
                    "user_answer": user_answer,
                    "correct_answer": "LLM Evaluated",
                    "evaluation": evaluation,
                    "score": descriptive_marks,
                    "max_marks": marks
                }
            )

    return {
        "score": total_score,
        "max_score": max_score,
        "results": results
    }