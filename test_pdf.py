from services.pdf_reader import extract_text_from_pdf
from evaluation.metrics import get_metrics

pdf_path = r"D:\llm_adaptive_interview_system\Introduction_to_DBMS.pdf"

text = extract_text_from_pdf(pdf_path)

print(text[:500])

print("\nMetrics:")
print(get_metrics())