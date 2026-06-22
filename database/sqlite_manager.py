import sqlite3
from datetime import datetime

def create_connection():

    conn = sqlite3.connect(
        "assessment_history.db",
        check_same_thread=False
    )

    return conn


def create_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        subject TEXT,

        topic TEXT,

        question_type TEXT,

        score INTEGER,

        max_score INTEGER,

        percentage REAL,

        recommended_difficulty TEXT,
        username TEXT,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()
def save_assessment(

    username,
    subject,
    topic,
    question_type,
    score,
    max_score,
    percentage,
    recommended_difficulty
):

    conn = create_connection()

    cursor = conn.cursor()

    
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO assessments (
            username,
            subject,
            topic,
            question_type,
            score,
            max_score,
            percentage,
            recommended_difficulty,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            subject,
            topic,
            question_type,
            score,
            max_score,
            percentage,
            recommended_difficulty,
            timestamp
        )
    )

    conn.commit()

    conn.close()

def get_assessments(username):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            subject,
            topic,
            question_type,
            score,
            max_score,
            percentage,
            recommended_difficulty,
            timestamp
        FROM assessments
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_analytics(username):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),
            AVG(percentage),
            MAX(percentage)
        FROM assessments
        WHERE username = ?
        """,
        (username,)
    )

    summary = cursor.fetchone()

    cursor.execute(
        """
        SELECT subject,
            COUNT(*)
        FROM assessments
        WHERE username = ?
        GROUP BY subject
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """,
        (username,)
    )

    subject_row = cursor.fetchone()

    cursor.execute(
        """
        SELECT recommended_difficulty
        FROM assessments
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (username,)
    )

    difficulty_row = cursor.fetchone()

    conn.close()

    return {
        "total_assessments": summary[0],
        "average_percentage": summary[1] if summary[1] else 0,
        "highest_percentage": summary[2] if summary[2] else 0,
        "most_practiced_subject":
            subject_row[0] if subject_row else "N/A",
        "latest_difficulty":
            difficulty_row[0] if difficulty_row else "N/A"
    }
def get_topic_performance(username):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            topic,
            AVG(percentage)
        FROM assessments
        WHERE username = ?
        GROUP BY topic
        ORDER BY AVG(percentage)
        """,
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows