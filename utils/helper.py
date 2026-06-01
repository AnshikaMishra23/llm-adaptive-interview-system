import re

def extract_score(evaluation_text):

    match = re.search(r"SCORE:\s*(\d+)", evaluation_text)

    if match:
        return int(match.group(1))

    return 0