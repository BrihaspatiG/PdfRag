from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_document(self, chunks):
        for chunk in chunks:
            text = chunk["text"]
            embedding = self.model.encode(text)
            chunk["embedding"] = embedding.tolist()
        return chunks

    def embed_query(self, query):
        embedding = self.model.encode(query)
        return embedding.tolist()