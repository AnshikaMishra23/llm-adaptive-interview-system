from services.pdf_reader import extract_text_from_pdf
from rag.rag_pipeline import get_relevant_context
from evaluation.metrics import get_metrics, clear_metrics

clear_metrics()

pdf_path = r"D:\llm_adaptive_interview_system\Introduction_to_DBMS.pdf"

text = extract_text_from_pdf(pdf_path)

context = get_relevant_context(
    text,
    "MCQ questions"
)

print("Retrieved Context:\n")
print(context[:500])

print("\nMetrics:\n")
print(get_metrics())