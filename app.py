import streamlit as st

from services.llm_service import ask_llm
from prompts.question_prompt import get_question_prompt
from services.evaluator import evaluate_answer
from utils.helper import extract_score
from services.adaptive_engine import get_next_difficulty

st.set_page_config(
    page_title="LLM Adaptive Interview System",
    page_icon="🎯"
)

st.title("🎯 LLM Adaptive Interview System")

subject = st.selectbox(
    "Subject",
    ["DBMS", "Operating Systems", "Computer Networks", "Machine Learning"]
)

topic = st.text_input("Topic")

difficulty = st.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

# Initialize session state
if "question" not in st.session_state:
    st.session_state.question = ""

if st.button("Generate Question"):

    prompt = get_question_prompt(
        subject,
        topic,
        difficulty
    )

    st.session_state.question = ask_llm(prompt)

# Show question if available
if st.session_state.question:

    st.subheader("Generated Question")
    st.write(st.session_state.question)

    answer = st.text_area(
        "Your Answer",
        height=200
    )

    if st.button("Evaluate Answer"):

        if answer.strip() == "":
            st.warning("Please enter an answer.")

        else:

            evaluation = evaluate_answer(
                st.session_state.question,
                answer
            )

            score = extract_score(evaluation)

            next_difficulty = get_next_difficulty(score)

            st.subheader("Evaluation")

            st.success(f"Score: {score}/10")

            st.info(f"Recommended Next Difficulty: {next_difficulty}")

            st.write(evaluation)