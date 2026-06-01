def get_question_prompt(subject, topic, difficulty):
    return f"""
You are an expert technical interviewer.

Generate ONE interview question.

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Return only the question.
"""