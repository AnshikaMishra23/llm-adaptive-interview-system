from services.assessment_evaluator import evaluate_mcq_assessment

questions = [
    {
        "question_id": 1,
        "correct_answer": "B",
        "marks": 1
    },
    {
        "question_id": 2,
        "correct_answer": "A",
        "marks": 1
    }
]

user_answers = {
    1: "B",
    2: "C"
}

result = evaluate_mcq_assessment(
    questions,
    user_answers
)

print(result)