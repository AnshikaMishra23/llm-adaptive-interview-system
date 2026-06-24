import faiss
import numpy as np


def build_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(
            embeddings,
            dtype=np.float32
        )
    )

    return index


def retrieve_chunks(
    query_embedding,
    chunks,
    index,
    k=5
):

    distances, indices = index.search(
        np.array(
            [query_embedding],
            dtype=np.float32
        ),
        k
    )

    retrieved = []

    for idx in indices[0]:

        retrieved.append(
            chunks[idx]
        )

    return retrieved