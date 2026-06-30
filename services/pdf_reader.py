from pypdf import PdfReader
from evaluation.metrics import (
    Timer,
    add_metric
)


def extract_text_from_pdf(pdf_file):

    timer = Timer()

    timer.start()

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    extraction_time = timer.stop()

    add_metric(
        "PDF Extraction Time",
        extraction_time
    )

    return text