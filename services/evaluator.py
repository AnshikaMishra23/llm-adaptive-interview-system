from services.llm_service import ask_llm
from prompts.evaluation_prompt import get_evaluation_prompt


def evaluate_answer(question, answer):

    prompt = get_evaluation_prompt(
        question,
        answer
    )

    evaluation = ask_llm(prompt)

    return evaluation