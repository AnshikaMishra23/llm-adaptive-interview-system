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

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()
def save_assessment(

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
            subject,
            topic,
            question_type,
            score,
            max_score,
            percentage,
            recommended_difficulty,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
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

def get_assessments():

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
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows