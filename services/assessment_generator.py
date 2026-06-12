import json

from services.llm_service import ask_llm


def generate_assessment(
    subject,
    topic,
    difficulty,
    question_type,
    num_questions
):

    if question_type == "MCQ":

        prompt = f"""
Generate {num_questions} MCQ questions.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

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
Generate {num_questions} MSQ questions.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

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

    else:

        mcq_count = max(1, num_questions // 2)

        msq_count = num_questions - mcq_count

        prompt = f"""
Generate a mixed assessment.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Create:

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
1. MCQ must have exactly one correct answer.
2. MSQ must have at least two correct answers.
3. Mix both question types.
4. Return JSON only.
"""

    response = ask_llm(prompt)

    return json.loads(response)