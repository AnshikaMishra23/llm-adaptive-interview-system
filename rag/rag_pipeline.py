from rag.chunker import chunk_text
from rag.embedder import create_embeddings, model
from rag.retriever import (
    build_index,
    retrieve_chunks
)


def get_relevant_context(
    pdf_text,
    query,
    k=5
):

    chunks = chunk_text(
        pdf_text
    )

    embeddings = create_embeddings(
        chunks
    )

    index = build_index(
        embeddings
    )

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    retrieved_chunks = retrieve_chunks(
        query_embedding,
        chunks,
        index,
        k
    )

    return "\n\n".join(
        retrieved_chunks
    )