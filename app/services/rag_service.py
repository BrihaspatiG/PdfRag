import os
from app.services.pdf_parser import PDFParser
from app.services.text_chunker import TextChunker
from app.services.embedding_generator import EmbeddingGenerator
from app.services.faiss_manager import FAISSManager
from app.services.llm_service import LLMService
from app.services.json_handler import JSONHandler
from app.services.intent_classifier import IntentClassifier

class RAGService:

    def __init__(self):

        self.chunker = TextChunker()
        self.embedding_generator = EmbeddingGenerator()
        self.faiss_manager = FAISSManager()
        self.llm_service = LLMService()
        self.json_handler = JSONHandler()
        self.intent_classifier = IntentClassifier()

        self.embedded_chunks = []
        self.pdf_loaded = False
        self.current_pdf = None
        self.last_retrieved_chunks = []

    def load_pdf(self, pdf_name):

        pdf_path = os.path.join(
            "uploaded_pdfs",
            pdf_name
        )

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"PDF '{pdf_name}' not found."
            )

        # Clear previous FAISS index
        self.faiss_manager.reset()
        filename_without_extension = os.path.splitext(pdf_name)[0]
        output_path = (
            f"extracted_text/{filename_without_extension}.json"
        )

        chunk_output_path = (
            f"chunked_text/{filename_without_extension}_chunks.json"
        )

        embedding_output_path = (
            f"embedded_chunks/{filename_without_extension}_embedded.json"
        )

        parser = PDFParser(pdf_path)

        if os.path.exists(embedding_output_path):
            print("\nEmbedded file found. Loading from cache...\n")
            self.embedded_chunks = self.json_handler.load(
                embedding_output_path
            )
        else:
            print("\nNo cached embeddings found. Processing PDF...\n")
            parser.open_pdf()
            pages = parser.extract_text()
            parser.close_pdf()
            chunks = self.chunker.chunk_document(
                pages
            )
            self.embedded_chunks = (
                self.embedding_generator.embed_document(
                    chunks
                )
            )

            self.json_handler.save(
                pages,
                output_path
            )

            self.json_handler.save(
                chunks,
                chunk_output_path
            )

            self.json_handler.save(
                self.embedded_chunks,
                embedding_output_path
            )

        self.faiss_manager.add_embeddings(
            self.embedded_chunks
        )

        self.pdf_loaded = True
        self.current_pdf = pdf_name

        return {
            "message": f"{pdf_name} loaded successfully.",
            "chunks": len(self.embedded_chunks),
            "embedding_dimension": len(
                self.embedded_chunks[0]["embedding"]
            )
        }

    def ask(self, question, chat_history=None):

        intent = self.intent_classifier.classify(
            question
            )
        if intent == "greeting":

            return {
                "answer":
                    "Hello! 👋 How can I help you with your PDF today?",
                "sources": []
            }

        if intent == "thanks":

            return {
                "answer":
                    "You're welcome! 😊",
                "sources": []
            }

        if intent == "farewell":

            return {
                "answer":
                    "Goodbye! 👋 Have a great day!",
                "sources": []
            }

        if intent == "help":

            return {
                "answer":
                    (
                        "I can answer questions related to the "
                        "currently loaded PDF. "
                        "Simply ask me anything about its content."
                    ),
                "sources": []
            }
        if not self.pdf_loaded:
            raise ValueError(
                "No PDF has been loaded."
            )
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )
        query_embedding = self.embedding_generator.embed_query(
            question
        )
        distances, indices = self.faiss_manager.search(
            query_embedding,
            k=3
        )
        context_parts = []
        retrieved_chunks = []

        for idx in indices[0]:
            chunk = self.embedded_chunks[idx]
            retrieved_chunks.append(chunk)
            context_parts.append(
                chunk["text"]
            )

        self.last_retrieved_chunks = retrieved_chunks
        context = "\n\n".join(context_parts)
        answer = self.llm_service.generate_response(
            context,
            question,
            chat_history
        )
        return {
            "answer": answer,
            "sources": [
                {
                    "page": chunk["page"],
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"]
                }
                for chunk in retrieved_chunks
            ]
        }