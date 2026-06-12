from database.sqlite_manager import save_assessment

save_assessment(
    "DBMS",
    "Normalization",
    "MCQ",
    4,
    5,
    80.0,
    "Hard"
)

print("Saved successfully")