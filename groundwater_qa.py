
from modules.vector_database import GroundwaterDatabase
from modules.local_ai import ask_local_ai


def answer_from_pdf(question):
    try:
        db = GroundwaterDatabase()
        db.load_database()

        results = db.search(question, top_k=3)

        if not results:
            return "Sorry, no relevant information found in the PDF."

        context = ""
        source_pages = []

        for item in results:
            page = item["page"]
            context += f"\nPage {page}:\n{item['text']}\n"

            if page not in source_pages:
                source_pages.append(page)

        answer = ask_local_ai(question, context)

        sources = ", ".join(str(page) for page in source_pages)

        final_answer = (
            f"{answer}\n\n"
            f"**Source pages in groundwater report:** {sources}"
        )

        return final_answer

    except Exception as e:
        return f"Error: {e}"

