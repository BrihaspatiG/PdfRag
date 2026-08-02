import os
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
PDF_FOLDER = "uploaded_pdfs"


def load_pdf(selected_pdf):
    return requests.post(
        f"{API_URL}/load_pdf",
        json={
            "pdf": selected_pdf
        }
    )


def ask_question(question, chat_history):
    return requests.post(
        f"{API_URL}/ask",
        json={
            "question": question,
            "chat_history": chat_history
        }
    )


st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------------- Session State ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

# ---------------- Title ---------------- #

st.title("📚 Intelligent PDF QA Assistant")

st.caption(
    "Ask questions about your PDFs using Retrieval-Augmented Generation (RAG)"
)

# ---------------- Sidebar ---------------- #

with st.sidebar:
    st.title("📄 PDF Manager")
    os.makedirs(PDF_FOLDER, exist_ok=True)
    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )
    if uploaded_file is not None:
        save_path = os.path.join(
            PDF_FOLDER,
            uploaded_file.name
        )
        if os.path.exists(save_path):
            st.warning("This PDF already exists.")
        else:
            with open(save_path, "wb") as file:
                file.write(uploaded_file.getbuffer())
            st.success(
                f"{uploaded_file.name} uploaded successfully!"
            )

    pdf_files = [
        file
        for file in os.listdir(PDF_FOLDER)
        if file.endswith(".pdf")
    ]

    if pdf_files:

        selected_pdf = st.selectbox(
            "Select PDF",
            pdf_files
        )

        if st.button(
            "📥 Load PDF",
            use_container_width=True
        ):

            with st.spinner("Loading PDF..."):
                response = load_pdf(selected_pdf)
            if response.status_code == 200:
                data = response.json()
                st.session_state.current_pdf = selected_pdf
                st.success(data["message"])
                st.info(
                    f"""
📄 Chunks: {data['chunks']}

🧠 Embedding Dimension: {data['embedding_dimension']}
"""
                )

            else:
                st.error(
                    response.json()["detail"]
                )

    else:

        st.warning(
            "No PDFs available. Upload one first."
        )

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.chat_history = []
        st.success("Chat cleared!")
        st.rerun()
    st.divider()
    st.markdown("### ℹ️ About")
    st.write(
        """
**PDF RAG Assistant**

Built using:

- FastAPI
- Streamlit
- FAISS
- Sentence Transformers
- Groq LLM
"""
    )

# ---------------- Main Area ---------------- #

if st.session_state.current_pdf:

    st.success(
        f"📄 Current PDF: {st.session_state.current_pdf}"
    )

else:

    st.info(
        """
### 👋 Welcome!

1. Upload or select a PDF from the sidebar.
2. Click **Load PDF**.
3. Start asking questions.

The assistant will answer only from the selected document.
"""
    )

# ---------------- Chat History ---------------- #

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            st.caption("📄 Sources")

            for source in message["sources"]:

                with st.expander(
                    f"Page {source['page']} (Chunk {source['chunk_id']})"
                ):

                    st.write(source["text"])

            with st.expander("📊 Retrieval Details"):

                st.write("Embedding Model: all-MiniLM-L6-v2")
                st.write("Vector Database: FAISS")
                st.write(
                    f"Retrieved Chunks: {len(message['sources'])}"
                )

# ---------------- Chat Input ---------------- #

question = st.chat_input(
    "Ask anything about the selected PDF..."
)

if question:

    if not st.session_state.current_pdf:

        st.error(
            "Please load a PDF first."
        )

    else:

        with st.spinner("Thinking..."):

            response = ask_question(
            question,
            st.session_state.chat_history[-6:]
            )

        if response.status_code == 200:

            data = response.json()

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data["sources"]
                }
            )

            st.rerun()

        else:

            st.error(
                response.json()["detail"]
            )