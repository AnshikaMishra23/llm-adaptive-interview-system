from database.sqlite_manager import get_assessments

rows = get_assessments()

for row in rows:
    print(row)