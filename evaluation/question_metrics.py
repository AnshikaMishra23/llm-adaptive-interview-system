from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def diversity_score(questions):

    texts = []

    for q in questions:

        texts.append(
            q["question"]
        )

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    similarity = cosine_similarity(
        embeddings
    )

    n = len(similarity)

    total = 0
    count = 0

    for i in range(n):

        for j in range(i + 1, n):

            total += similarity[i][j]
            count += 1

    if count == 0:

        return 100

    avg_similarity = total / count

    diversity = (
        1 - avg_similarity
    ) * 100

    return round(diversity, 2)
def duplicate_questions(questions):

    texts = []

    for q in questions:

        texts.append(
            q["question"]
        )

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    similarity = cosine_similarity(
        embeddings
    )

    duplicates = 0

    n = len(similarity)

    for i in range(n):

        for j in range(i + 1, n):

            if similarity[i][j] >= 0.90:

                duplicates += 1

    return duplicates
def average_question_length(questions):

    total = 0

    for q in questions:

        total += len(
            q["question"].split()
        )

    return round(
        total / len(questions),
        2
    )