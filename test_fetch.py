import sqlite3

conn = sqlite3.connect(
    "assessment_history.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM assessments"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()