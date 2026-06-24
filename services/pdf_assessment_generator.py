import json

from services.llm_service import ask_llm


def generate_questions_from_pdf(
    pdf_text,
    question_type,
    num_questions
):

    if question_type == "MCQ":

        prompt = f"""
Based on the following notes:

{pdf_text[:5000]}

Generate {num_questions} MCQ questions.

Return ONLY valid JSON.

Format:

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

Rules:
1. Exactly one correct answer.
2. Return JSON only.
"""

    elif question_type == "MSQ":

        prompt = f"""
Based on the following notes:

{pdf_text[:5000]}

Generate {num_questions} MSQ questions.

Return ONLY valid JSON.

Format:

[
    {{
        "question_id": 1,
        "question_type": "MSQ",
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": [
            "Option A",
            "Option C"
        ],
        "marks": 1
    }}
]

Rules:
1. At least two correct answers.
2. Return JSON only.
"""

    elif question_type == "Descriptive":

        prompt = f"""
Based on the following notes:

{pdf_text[:5000]}

Generate {num_questions} descriptive questions.

Return ONLY valid JSON.

Format:

[
    {{
        "question_id": 1,
        "question_type": "Descriptive",
        "question": "Question text",
        "marks": 10
    }}
]

Rules:
1. Generate descriptive/theory questions.
2. Return JSON only.
"""

    else:

        mcq_count = max(1, num_questions // 2)

        msq_count = num_questions - mcq_count

        prompt = f"""
Based on the following notes:

{pdf_text[:5000]}

Generate:

{mcq_count} MCQ questions
{msq_count} MSQ questions

Return ONLY valid JSON.

Format:

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
    }},
    {{
        "question_id": 2,
        "question_type": "MSQ",
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": [
            "Option A",
            "Option C"
        ],
        "marks": 1
    }}
]

Rules:
1. MCQ must have one correct answer.
2. MSQ must have multiple correct answers.
3. Return JSON only.
"""

    response = ask_llm(prompt)

    print("PDF RESPONSE:")
    print(response)

    return json.loads(response)