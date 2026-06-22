from database.sqlite_manager import get_topic_performance

rows = get_topic_performance()

for row in rows:
    print(row)