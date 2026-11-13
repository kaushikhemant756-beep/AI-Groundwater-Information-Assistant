import hashlib
from modules.build_database import build_from_pdf
from modules.groundwater_qa import answer_from_pdf
import streamlit as st
from pypdf import PdfReader
from io import BytesIO

st.set_page_config(
    page_title="AI Groundwater Assistant",
    page_icon="💧",
    layout="wide"
)

st.title("💧 AI Groundwater Information Assistant")

st.write(
    "Upload groundwater reports and explore "
    "their information."
)

st.sidebar.title("Project Details")
st.sidebar.success("Project ID: P16")
st.sidebar.info("Group ID: OJ16")

st.divider()

st.header("📄 Upload Groundwater Report")

uploaded_file = st.file_uploader(
    "Select your groundwater PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        pdf_bytes = uploaded_file.getvalue()

        file_hash = hashlib.sha256(pdf_bytes).hexdigest()

        if st.session_state.get("processed_pdf_hash") != file_hash:

            with st.spinner("Building AI database from uploaded PDF..."):
                total_chunks = build_from_pdf(pdf_bytes)

            st.session_state["processed_pdf_hash"] = file_hash
            st.session_state["messages"] = []

            st.success(
                f"AI database updated successfully! "
                f"Total chunks: {total_chunks}"
            )
        pdf = PdfReader(
            BytesIO(uploaded_file.getvalue())
        )

        total_pages = len(pdf.pages)

        st.success("PDF uploaded successfully!")

        st.metric("Total PDF Pages", total_pages)

        pages_to_read = min(5, total_pages)

        st.info(
            f"Reading first {pages_to_read} pages "
            f"out of {total_pages} pages."
        )

        extracted_text = []

        progress = st.progress(0)

        for i in range(pages_to_read):

            try:
                page = pdf.pages[i]
                text = page.extract_text() or ""

                if text.strip():
                    extracted_text.append(
                        f"PAGE {i + 1}\n{text[:3000]}"
                    )
                else:
                    extracted_text.append(
                        f"PAGE {i + 1}: No readable text."
                    )

            except Exception:
                extracted_text.append(
                    f"PAGE {i + 1}: Could not extract text."
                )

            progress.progress(
                (i + 1) / pages_to_read
            )

        full_text = "\n\n".join(extracted_text)

        st.subheader("Extracted Information")

        st.text_area(
            "PDF Text Preview",
            full_text[:12000],
            height=350
        )

        st.download_button(
            "Download Extracted Text",
            data=full_text,
            file_name="groundwater_information.txt",
            mime="text/plain"
        )

        st.success("PDF processing completed!")

    except Exception as error:
        st.error(f"PDF Error: {error}")

else:
    st.info("Please upload a groundwater PDF report.")

st.divider()

st.caption(
    "P16 | AI Groundwater Information Assistant"
)

# ==============================
# AI CHATBOT SECTION
# ==============================

st.divider()

st.header("💧 Ask Groundwater AI")

st.write(
    "Ask any question related to groundwater. "
    "AI will answer using your groundwater database."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User question

question = st.chat_input(
    "Ask your groundwater question..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Qwen AI is thinking..."):

            answer = answer_from_pdf(question)

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })



