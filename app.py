import streamlit as st
import pandas as pd

from services.llm_service import ask_llm
from prompts.question_prompt import get_question_prompt
from services.evaluator import evaluate_answer
from utils.helper import extract_score
from services.learning_path import get_learning_path
from services.adaptive_engine import get_next_difficulty

from services.assessment_generator import generate_assessment
from services.assessment_evaluator import evaluate_assessment
from database.sqlite_manager import (
    save_assessment,
    get_assessments,
    get_topic_performance
)
from database.auth_manager import (
    register_user,
    login_user
)
from services.pdf_reader import (
    extract_text_from_pdf
)

from services.pdf_assessment_generator import (
    generate_questions_from_pdf
)
from evaluation.report import generate_report
from evaluation.adaptive_metrics import (
    adaptive_learning_metrics
)

st.set_page_config(
    page_title="LLM Adaptive Interview System",
    page_icon="🎯"
)
st.title("🎯 LLM Adaptive Interview System")

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if not st.session_state.logged_in:

    auth_mode = st.radio(
        "Authentication",
        ["Login", "Register"]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if auth_mode == "Login":

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

    else:

        if st.button("Register"):

            success = register_user(
                username,
                password
            )

            if success:

                st.success(
                    "Registration Successful"
                )

            else:

                st.error(
                    "Username already exists"
                )

else:

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        if "username" in st.session_state:
            del st.session_state.username

        st.rerun()

    mode = st.radio(
        "Select Mode",
        [
            "Interview Mode",
            "Assessment Mode",
            "History",
            "Evaluation Dashboard"
        ]
    )
# ==================================================
# INTERVIEW MODE
# ==================================================

if st.session_state.logged_in and mode == "Interview Mode":

    subject = st.selectbox(
        "Subject",
        ["DBMS", "Operating Systems", "Computer Networks", "Machine Learning"]
    )

    topic = st.text_input("Topic")

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if "question" not in st.session_state:
        st.session_state.question = ""

    if st.button("Generate Question"):

        prompt = get_question_prompt(
            subject,
            topic,
            difficulty
        )

        st.session_state.question = ask_llm(prompt)

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

                st.info(
                    f"Recommended Next Difficulty: {next_difficulty}"
                )

                st.write(evaluation)

# ==================================================
# ASSESSMENT MODE
# ==================================================

if st.session_state.logged_in and mode == "Assessment Mode":

    st.header("Assessment Mode")

    subject = st.selectbox(
        "Subject",
        ["DBMS", "Operating Systems", "Computer Networks", "Machine Learning"],
        key="assessment_subject"
    )

    topic = st.text_input(
        "Topic",
        key="assessment_topic"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        key="assessment_difficulty"
    )

    question_type = st.selectbox(
        "Question Type",
        ["MCQ" , "MSQ" ,"Mixed","Descriptive"],
        key="assessment_question_type"
    )
    assessment_source = st.radio(
        "Assessment Source",
        [
            "Topic Based",
            "PDF Based"
        ]
    )

    uploaded_pdf = None

    if assessment_source == "PDF Based":

        uploaded_pdf = st.file_uploader(
            "Upload PDF Notes",
            type=["pdf"]
        )
    num_questions = st.number_input(
        "Number of Questions",
        min_value=1,
        max_value=20,
        value=5
    )

    if "assessment_questions" not in st.session_state:
        st.session_state.assessment_questions = []

    if st.button(
        "🚀 Generate Assessment",
        use_container_width=True
    ):

        st.session_state.saved_result = False

        with st.spinner("Generating assessment... Please wait ⏳"):

            if assessment_source == "Topic Based":

                questions = generate_assessment(
                    subject,
                    topic,
                    difficulty,
                    question_type,
                    num_questions
                )

            else:

                if uploaded_pdf is None:

                    st.warning(
                        "Please upload a PDF."
                    )

                    st.stop()

                pdf_text = extract_text_from_pdf(
                    uploaded_pdf
                )

                questions = generate_questions_from_pdf(
                    pdf_text,
                    question_type,
                    num_questions
                )

            st.session_state.assessment_questions = questions

            st.session_state.evaluation_report = generate_report(
                questions
            )

        st.success(
            " Assessment generated successfully!"
        )

    if st.session_state.assessment_questions:

        st.subheader("Generated Assessment")

        user_answers = {}

        for question in st.session_state.assessment_questions:

            st.markdown(
                f"### Q{question['question_id']}. {question['question']}"
            )

            if question["question_type"] == "MCQ":

                options = ["Select an option"] + question["options"]

                answer = st.radio(
                    "Select Answer",
                    options,
                    key=f"q_{question['question_id']}"
                )

                if answer != "Select an option":

                    user_answers[
                        question["question_id"]
                    ] = answer

            elif question["question_type"] == "MSQ":

                answer = st.multiselect(
                    "Select One or More Answers",
                    question["options"],
                    key=f"q_{question['question_id']}"
                )

                if len(answer) > 0:

                    user_answers[
                        question["question_id"]
                    ] = answer
            elif question["question_type"] == "Descriptive":

                answer = st.text_area(
                    "Your Answer",
                    key=f"q_{question['question_id']}",
                    height=150
                )

                if answer.strip():

                    user_answers[
                        question["question_id"]
                    ] = answer

        if st.button("Submit Assessment"):

            if len(user_answers) != len(
                st.session_state.assessment_questions
            ):

                st.warning(
                    "Please answer all questions before submitting."
                )

            else:
                with st.spinner(
                    "Evaluating answers... Please wait."
                ):

                    result = evaluate_assessment(
                        st.session_state.assessment_questions,
                        user_answers
                    )

                st.subheader("Assessment Result")

                st.success(
                    f"Score: {result['score']} / {result['max_score']}"
                )

                percentage = (
                    result["score"]
                    / result["max_score"]
                ) * 100

                st.info(
                    f"Percentage: {percentage:.2f}%"
                )
                score_on_10 = round(
                    (result["score"] / result["max_score"]) * 10
                )

                next_difficulty = get_next_difficulty(
                    score_on_10
                )

                st.info(
                    f"Recommended Next Difficulty: {next_difficulty}"
                )
                if "saved_result" not in st.session_state:
                    st.session_state.saved_result = False

                if not st.session_state.saved_result:

                    save_assessment(
                        st.session_state.username,
                        subject,
                        topic,
                        question_type,
                        result["score"],
                        result["max_score"],
                        percentage,
                        next_difficulty
                    )

                    st.session_state.saved_result = True

                for item in result["results"]:

                    if item["question_type"] == "Descriptive":

                        st.subheader(
                            f"Q{item['question_id']} Evaluation"
                        )

                        st.info(
                            f"Score: {item['score']} / {item['max_marks']}"
                        )

                        st.write(
                            item["evaluation"]
                        )

                    else:

                        if item["correct"]:

                            st.success(
                                f"Q{item['question_id']} Correct"
                            )

                        else:

                            st.error(
                                f"Q{item['question_id']} Incorrect"
                            )

                            user_answer = item["user_answer"]
                            correct_answer = item["correct_answer"]

                            if isinstance(user_answer, list):
                                user_answer = ", ".join(user_answer)

                            if isinstance(correct_answer, list):
                                correct_answer = ", ".join(correct_answer)

                            st.write(
                                f"Your Answer: {user_answer}"
                            )

                            st.write(
                                f"Correct Answer: {correct_answer}"
                            )
        
# ==================================================
# HISTORY MODE
# ==================================================

if st.session_state.logged_in and mode == "History":

    st.header("Assessment History")
    
    rows = get_assessments(
        st.session_state.username
    )
    if len(rows) > 0:

        chart_data = []

        for row in reversed(rows):

            chart_data.append(
                {
                    "Timestamp": row[7],
                    "Percentage": row[5]
                }
            )

        df = pd.DataFrame(chart_data)


        st.subheader("⚠ Weak Topic Detection")

        topics = get_topic_performance(
            st.session_state.username
        )

        if len(topics) > 0:

            weak_topics = topics[:3]

            for topic, score in weak_topics:

                st.write(
                    f"📌 {topic} : {score:.2f}%"
                )
        if len(topics) > 0:

            weakest_topic = topics[0][0]

            path = get_learning_path(
                weakest_topic
            )

            st.subheader(
                "📚 Recommended Learning Path"
            )

            for step_no, step in enumerate(
                path,
                start=1
            ):

                st.write(
                    f"{step_no}. {step}"
                )
        if len(rows) == 0:

            st.info("No assessments found.")

        else:

            history_data = []
            ...
        

    if len(rows) == 0:

        st.info("No assessments found.")

    else:

        history_data = []

        for row in rows:

            history_data.append(
                {
                    "Subject": row[0],
                    "Topic": row[1],
                    "Type": row[2],
                    "Score": f"{row[3]}/{row[4]}",
                    "Percentage": f"{row[5]:.2f}%",
                    "Recommended Difficulty": row[6],
                    "Timestamp": row[7]
                }
            )

        st.dataframe(
            history_data,
            use_container_width=True
        )

# ==================================================
# EVALUATION DASHBOARD
# ==================================================

if (
    st.session_state.logged_in
    and mode == "Evaluation Dashboard"
):

    st.header("📊 Evaluation Dashboard")

    adaptive = adaptive_learning_metrics(
        st.session_state.username
    )

    st.header("📈 Adaptive Learning")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Assessments",
            adaptive["Total Assessments"]
        )

    with col2:

        st.metric(
            "Average Score",
            f"{adaptive['Average Score']:.2f}%"
        )

    with col3:

        st.metric(
            "Highest Score",
            f"{adaptive['Highest Score']:.2f}%"
        )

    with col4:

        st.metric(
            "Current Difficulty",
            adaptive["Current Difficulty"]
        )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Lowest Score",
            f"{adaptive['Lowest Score']:.2f}%"
        )

    with col2:

        st.metric(
            "Performance Trend",
            adaptive["Performance Trend"]
        )

    with col3:

        st.metric(
            "Most Practiced Subject",
            adaptive["Most Practiced Subject"]
        )

    with col4:

        st.metric(
            "Weakest Topic",
            adaptive["Weakest Topic"]
        )
    st.divider()

    # ==================================================
    # PERFORMANCE TREND
    # ==================================================

    st.header("📈 Performance Trend")

    rows = get_assessments(
        st.session_state.username
    )

    if len(rows) > 0:

        chart_data = []

        for row in reversed(rows):

            chart_data.append(
                {
                    "Timestamp": row[7],
                    "Percentage": row[5]
                }
            )

        df = pd.DataFrame(chart_data)

        st.line_chart(
            df.set_index("Timestamp")
        )

    else:

        st.info(
            "No assessment history available."
        )

    st.divider()

    # ==================================================
    # QUESTION QUALITY
    # ==================================================
    st.caption(
        "Metrics for the latest assessment generated in this session."
    )
    st.header("🧠 Question Quality")

    if "evaluation_report" in st.session_state:

        report = st.session_state.evaluation_report

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Diversity Score",
                round(
                    report["Diversity Score"],
                    2
                )
            )

        with col2:

            st.metric(
                "Duplicate Questions",
                report["Duplicate Questions"]
            )

        with col3:

            st.metric(
                "Average Question Length",
                round(
                    report["Average Question Length"],
                    2
                )
            )

    else:

        st.info(
            "Generate an assessment to view question quality metrics."
        )

    st.divider()

    # ==================================================
    # ASSESSMENT STATISTICS
    # ==================================================
    st.caption(
        "Statistics for the latest assessment generated in this session."
    )
    st.header("📄 Assessment Statistics")

    if "evaluation_report" in st.session_state:

        report = st.session_state.evaluation_report

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Questions",
                report["Total Questions"]
            )

        with col2:

            st.metric(
                "MCQ Questions",
                report["MCQ Questions"]
            )

        with col3:

            st.metric(
                "MSQ Questions",
                report["MSQ Questions"]
            )

        with col4:

            st.metric(
                "Descriptive",
                report["Descriptive Questions"]
            )

        st.metric(
            "Total Marks",
            report["Total Marks"]
        )

    else:

        st.info(
            "Generate an assessment to view assessment statistics."
        )
        st.divider()

    # ==================================================
    # RAG PERFORMANCE
    # ==================================================

    st.subheader("⚡ RAG Performance")

    if "evaluation_report" in st.session_state:

        report = st.session_state.evaluation_report

        rag_metrics = [
            "PDF Extraction Time",
            "Chunking Time",
            "Embedding Time",
            "FAISS Index Time",
            "Retrieval Time",
            "LLM Generation Time",
            "Retrieved Chunks"
        ]

        rag_data = []

        for metric in rag_metrics:

            if metric in report:

                rag_data.append(
                    {
                        "Metric": metric,
                        "Value": report[metric]
                    }
                )

        if len(rag_data) > 0:

            col1, col2 = st.columns(2)

            for i, item in enumerate(rag_data):

                if i % 2 == 0:
                    with col1:
                        st.metric(item["Metric"], item["Value"])
                else:
                    with col2:
                        st.metric(item["Metric"], item["Value"])

        else:

            st.info(
                "Generate a PDF-based assessment to view RAG metrics."
            )

    else:

        st.info(
            "Generate a PDF-based assessment to view RAG metrics."
        )
    