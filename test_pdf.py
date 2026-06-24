from services.pdf_reader import extract_text_from_pdf

pdf_path = r"Introduction_to_DBMS.pdf"

text = extract_text_from_pdf(
    pdf_path
)

print(text[:2000])