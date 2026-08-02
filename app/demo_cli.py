from app.services.rag_service import RAGService
import os

pdf_folder = "uploaded_pdfs"

pdf_files = [
    file for file in os.listdir(pdf_folder)
    if file.endswith(".pdf")
]

if not pdf_files:
    print("No PDF files found in the uploaded_pdfs folder.")
    exit()

print("\nAvailable PDFs:\n")

for i, file in enumerate(pdf_files, start=1):
    print(f"{i}. {file}")

while True:
    try:
        choice = int(input("\nSelect a PDF by number: "))
        if 1 <= choice <= len(pdf_files):
            break
        print("Please enter a valid number.")
    except ValueError:
        print("Please enter a numeric value.")

rag = RAGService()

rag.load_pdf(
    pdf_files[choice - 1]
)

while True:
    query = input("\nAsk a question: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    if not query.strip():
        print("Please enter a question.")
        continue

    answer = rag.ask(query)

    print("\nAnswer:\n")
    print(answer)