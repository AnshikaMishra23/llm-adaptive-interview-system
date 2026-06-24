import json

from services.llm_service import ask_llm


def generate_questions_from_pdf(
    pdf_text,
    question_type,
    num_questions
):

    prompt = f"""
Based on the following notes:

{pdf_text[:5000]}

Generate {num_questions} {question_type} questions.

Return ONLY valid JSON in this format:

[
    {{
        "question_id": 1,
        "question_type": "MCQ",
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": "Option B",
        "marks": 1
    }}
]

Do not return explanations.
Do not return markdown.
Return JSON only.
"""

    response = ask_llm(prompt)

    print("PDF RESPONSE:")
    print(response)

    data = json.loads(response)

    if isinstance(data, dict) and "questions" in data:

        questions = []

        for i, q in enumerate(data["questions"], start=1):

            questions.append(
                {
                    "question_id": i,
                    "question_type": "MCQ",
                    "question": q["question"],
                    "options": q["options"],
                    "correct_answer": q["answer"],
                    "marks": 1
                }
            )

        return questions

    return data