from services.pdf_reader import (
    extract_text_from_pdf
)

from rag.chunker import (
    chunk_text
)

from rag.embedder import (
    create_embeddings,
    model
)

from rag.retriever import (
    build_index,
    retrieve_chunks
)

pdf_path = r"Introduction_to_DBMS.pdf"

text = extract_text_from_pdf(
    pdf_path
)

chunks = chunk_text(text)

embeddings = create_embeddings(
    chunks
)

index = build_index(
    embeddings
)

query = "What is file system limitation?"

query_embedding = model.encode(
    query,
    convert_to_numpy=True
)

results = retrieve_chunks(
    query_embedding,
    chunks,
    index
)

for i, chunk in enumerate(results):

    print(
        f"\n===== RESULT {i+1} =====\n"
    )

    print(chunk[:500])