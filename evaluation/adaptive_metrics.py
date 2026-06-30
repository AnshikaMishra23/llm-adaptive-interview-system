from database.sqlite_manager import (
    get_assessments
)


def adaptive_learning_metrics(username):

    history = get_assessments(username)

    if len(history) == 0:

        return {
            "Total Assessments": 0,
            "Average Score": 0,
            "Highest Score": 0,
            "Lowest Score": 0,
            "Performance Trend": "N/A",
            "Most Practiced Subject": "N/A",
            "Weakest Topic": "N/A",
            "Current Difficulty": "N/A"
        }

    percentages = []

    subject_count = {}

    topic_scores = {}

    latest_difficulty = history[0][6]

    for row in history:

        subject = row[0]

        topic = row[1].strip()

        if topic == "":
            topic = "General"

        percentage = row[5]

        percentages.append(percentage)

        subject_count[subject] = (
            subject_count.get(subject, 0) + 1
        )

        topic_scores.setdefault(
            topic,
            []
        ).append(percentage)

    average = round(
        sum(percentages) / len(percentages),
        2
    )

    highest = max(percentages)

    lowest = min(percentages)

    most_practiced = max(
        subject_count,
        key=subject_count.get
    )

    weakest_topic = min(
        topic_scores,
        key=lambda t: (
            sum(topic_scores[t]) /
            len(topic_scores[t])
        )
    )

    # --------------------------
    # Performance Trend
    # --------------------------

    if len(percentages) >= 4:

        recent = percentages[:3]

        previous = percentages[-3:]

        recent_avg = (
            sum(recent) /
            len(recent)
        )

        previous_avg = (
            sum(previous) /
            len(previous)
        )

        if recent_avg > previous_avg + 5:

            trend = "Improving"

        elif recent_avg < previous_avg - 5:

            trend = "Declining"

        else:

            trend = "Stable"

    else:

        trend = "N/A"

    return {

        "Total Assessments": len(history),

        "Average Score": average,

        "Highest Score": highest,

        "Lowest Score": lowest,

        "Performance Trend": trend,

        "Most Practiced Subject": most_practiced,

        "Weakest Topic": weakest_topic,

        "Current Difficulty": latest_difficulty
    }