
from modules.pdf_processor import (
    extract_pdf_text,
    create_chunks
)

from modules.vector_database import GroundwaterDatabase


def build_from_pdf(pdf_bytes):

    print("Reading PDF...")

    documents = extract_pdf_text(pdf_bytes)

    print("Extracting text completed!")

    print("Creating text chunks...")

    chunks = create_chunks(documents)

    print("Total chunks:", len(chunks))

    print("Building FAISS database...")

    database = GroundwaterDatabase()

    database.create_database(chunks)

    database.save_database()

    print("Database saved successfully!")

    return len(chunks)


if __name__ == "__main__":

    pdf_path = "data/groundwater_report.pdf"

    with open(pdf_path, "rb") as file:

        pdf_bytes = file.read()

    total = build_from_pdf(pdf_bytes)

    print("Total chunks saved:", total)
