import faiss
import numpy as np


class FAISSManager:

    def __init__(self, dimension=384):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embedded_chunks):
        embeddings = []
        for chunk in embedded_chunks:
            embeddings.append(chunk["embedding"])
        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )
        self.index.add(embeddings)

    def search(self, query_embedding, k=3):
        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        ).reshape(1, -1)
        distances, indices = self.index.search(
            query_embedding, k
        )
        return distances, indices
    
    def reset(self):
        self.index.reset()