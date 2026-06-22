def get_learning_path(topic):

    paths = {

        "normalisation": [
            "Revise Normalization Fundamentals",
            "Practice 1NF",
            "Practice 2NF",
            "Practice 3NF",
            "Attempt Medium Questions"
        ],

        "normalization": [
            "Revise Normalization Fundamentals",
            "Practice 1NF",
            "Practice 2NF",
            "Practice 3NF",
            "Attempt Medium Questions"
        ],

        "transactions": [
            "Revise ACID Properties",
            "Study Transaction States",
            "Practice Schedules",
            "Learn Concurrency Control",
            "Practice Previous Questions"
        ],

        "joins": [
            "Revise SQL Basics",
            "Practice Inner Join",
            "Practice Outer Join",
            "Practice Self Join",
            "Solve Join-based Queries"
        ]
    }

    return paths.get(
        topic.lower(),
        [
            "Revise Fundamentals",
            "Practice Easy Questions",
            "Practice Medium Questions",
            "Attempt Mock Test"
        ]
    )