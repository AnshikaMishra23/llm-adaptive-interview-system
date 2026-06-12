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

        correct_answer = question["correct_answer"]

        marks = question["marks"]

        max_score += marks

        user_answer = user_answers.get(qid)

        if qtype == "MCQ":

            is_correct = (
                user_answer == correct_answer
            )

        elif qtype == "MSQ":

            is_correct = (
                set(user_answer)
                ==
                set(correct_answer)
            )

        else:

            is_correct = False

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

    return {
        "score": total_score,
        "max_score": max_score,
        "results": results
    }