from services.pdf_reader import (
    extract_text_from_pdf
)

from rag.chunker import (
    chunk_text
)

from rag.embedder import (
    create_embeddings
)

pdf_path = r"Introduction_to_DBMS.pdf"

text = extract_text_from_pdf(
    pdf_path
)

chunks = chunk_text(text)

embeddings = create_embeddings(
    chunks
)

print(
    "Chunks:",
    len(chunks)
)

print(
    "Embedding Shape:",
    embeddings.shape
)