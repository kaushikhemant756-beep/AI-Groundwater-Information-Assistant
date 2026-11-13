
from pypdf import PdfReader
from io import BytesIO


def extract_pdf_text(pdf_file):

    pdf = PdfReader(BytesIO(pdf_file))

    documents = []

    for page_number, page in enumerate(pdf.pages, start=1):

        try:
            text = page.extract_text() or ""

            if text.strip():
                documents.append({
                    "page": page_number,
                    "text": text
                })

        except Exception as error:
            print(f"Page {page_number} error: {error}")

    return documents


def create_chunks(documents, chunk_size=1000, overlap=150):

    chunks = []

    for document in documents:

        text = document["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "page": document["page"],
                    "text": chunk_text
                })

            start += chunk_size - overlap

    return chunks
