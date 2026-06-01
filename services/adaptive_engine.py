def get_next_difficulty(score):

    if score >= 8:
        return "Hard"

    elif score >= 5:
        return "Medium"

    else:
        return "Easy"