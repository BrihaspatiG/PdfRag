import os
from dotenv import load_dotenv
from groq import Groq

class LLMService:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file."
            )

        self.client = Groq(
            api_key=api_key
        )

    def generate_response(
        self,
        context,
        question,
        chat_history=None
    ):
        conversation = ""

        if chat_history:
            for message in chat_history:
                role = message["role"].capitalize()
                conversation += (
                f"{role}: {message['content']}\n"
                )

        prompt = f"""
            You are a helpful AI assistant that answers questions ONLY from the provided PDF.

            Rules:

            1. Use ONLY the provided context.

            2. Use the previous conversation only to understand follow-up questions like "it", "that", or "those".

            3. Never invent information.

            4. If the answer is not found in the context, reply exactly:

            "I couldn't find that information in the document."

            Previous Conversation:
            {conversation}

            Context:
            {context}

            Current Question:
            {question}
            """
            
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )
        return response.choices[0].message.content