# 📚 PDFRAG

> AI-powered PDF Question Answering System built using Retrieval-Augmented Generation (RAG), FastAPI, Streamlit, FAISS, Sentence Transformers, and Groq LLM.
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

## 📖 Overview

PDFRAG is an AI-powered document question answering system based on the Retrieval-Augmented Generation (RAG) architecture.

Instead of answering from general knowledge, PDFRAG retrieves the most relevant information from the uploaded PDF using semantic search and generates context-aware responses using a Large Language Model (LLM).

The application consists of a FastAPI backend that performs document processing, embedding generation, vector search, and response generation, along with a Streamlit frontend that provides an intuitive chat interface for interacting with PDF documents.

## ✨ Features

- 📄 Upload PDF documents
- 📚 Automatic text extraction using PyMuPDF
- 🧹 Text cleaning and preprocessing
- ✂️ Sentence-based chunking with overlap
- 🧠 Semantic embeddings using Sentence Transformers
- 🔍 Fast similarity search using FAISS
- 🤖 AI-powered answers using Groq Llama 3.3
- 💬 Conversation memory for follow-up questions
- 😊 Intent classification (Greetings, Help, Thanks, Farewell)
- 📖 Source chunk visualization
- 💾 Cached embeddings for faster PDF loading
- ⚡ FastAPI backend
- 🎨 Streamlit frontend