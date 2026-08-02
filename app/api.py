from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.rag_service import RAGService

app = FastAPI()
rag = RAGService()


class PDFRequest(BaseModel):
    pdf: str


class QuestionRequest(BaseModel):
    question: str
    chat_history: list = []

@app.get("/")
def home():
    return {
        "message": "Welcome to PDFRAG API"
    }


@app.post("/load_pdf")
def load_pdf(request: PDFRequest):

    try:
        return rag.load_pdf(request.pdf)

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/ask")
def ask(request: QuestionRequest):

    try:
        return rag.ask(
        request.question,
        request.chat_history
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )