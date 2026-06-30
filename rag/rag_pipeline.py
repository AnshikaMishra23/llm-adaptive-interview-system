from rag.chunker import chunk_text
from rag.embedder import create_embeddings, model
from rag.retriever import (
    build_index,
    retrieve_chunks
)

from evaluation.metrics import (
    Timer,
    add_metric
)


def get_relevant_context(
    pdf_text,
    query,
    k=5
):

    # --------------------------
    # Chunking
    # --------------------------

    timer = Timer()

    timer.start()

    chunks = chunk_text(
        pdf_text
    )

    chunk_time = timer.stop()

    add_metric(
        "Chunking Time",
        chunk_time
    )

    # --------------------------
    # Embeddings
    # --------------------------

    timer.start()

    embeddings = create_embeddings(
        chunks
    )

    embedding_time = timer.stop()

    add_metric(
        "Embedding Time",
        embedding_time
    )

    # --------------------------
    # FAISS Index
    # --------------------------

    timer.start()

    index = build_index(
        embeddings
    )

    index_time = timer.stop()

    add_metric(
        "FAISS Index Time",
        index_time
    )

    # --------------------------
    # Query Embedding
    # --------------------------

    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    # --------------------------
    # Retrieval
    # --------------------------

    timer.start()

    retrieved_chunks = retrieve_chunks(
        query_embedding,
        chunks,
        index,
        k
    )

    retrieval_time = timer.stop()

    add_metric(
        "Retrieval Time",
        retrieval_time
    )

    add_metric(
        "Retrieved Chunks",
        len(retrieved_chunks)
    )
    return "\n\n".join(
        retrieved_chunks
    )