import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
from nltk.tokenize import sent_tokenize

class TextChunker:

    def __init__(self, sentences_per_chunk=3, overlap=1):
        if overlap >= sentences_per_chunk:
            raise ValueError(
                "overlap must be smaller than sentences_per_chunk"
            )
        self.sentences_per_chunk = sentences_per_chunk
        self.overlap = overlap

    def split_sentences(self, text):
        return sent_tokenize(text)
    
    def chunk_text(self, page_data, chunk_id):
        filename = page_data["filename"]
        page = page_data["page"]
        text = page_data["text"]
        sentences = self.split_sentences(text)
        chunks = []
        step_size = self.sentences_per_chunk - self.overlap
        start = 0

        while start < len(sentences):
            end = start + self.sentences_per_chunk
            chunk = sentences[start:end]
            if len(chunk) < self.sentences_per_chunk and chunks:
                chunks[-1]["text"] += " " + " ".join(chunk)
                break
            
            chunk = " ".join(chunk)
            chunk_data = {
                "filename": filename,
                "page": page,
                "chunk_id": chunk_id,
                "text": chunk
            }
            chunks.append(chunk_data)
            chunk_id += 1
            start += step_size
        return chunks, chunk_id
    
    def chunk_document(self, pages):
        all_chunks = []
        chunk_id = 1
        for page in pages:
            page_chunks, chunk_id = self.chunk_text(
                page,
                chunk_id
            )
            all_chunks.extend(page_chunks)
        return all_chunks