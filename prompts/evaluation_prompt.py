def get_evaluation_prompt(question, answer):
    return f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Return your response in exactly this format:

SCORE: <number>

STRENGTHS:
...

WEAKNESSES:
...

MISSING_CONCEPTS:
...

IMPROVED_ANSWER:
...
"""