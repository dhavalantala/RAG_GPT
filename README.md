# 🧠 RAG GPT — Retrieval-Augmented Generation with GPT

**RAG GPT** is a modular system for document ingestion, vector search, summarization, and conversational interaction powered by GPT models. It combines a Vector Database with GPT-based summarization and chat functionality to provide document understanding and interactive querying.

## 📦 Project Structure

The project is divided into **four main components**, designed to work together or independently:

### **1️⃣ Data Preparation & Ingestion Pipeline**

- Processes and cleans your documents (PDF, text, etc.)

- Converts documents into vector representations using embeddings

- Stores vectors in a vector database for fast, semantic search


### **2️⃣ Real-Time Chatbot Document Upload**

- Upload new documents dynamically during a chatbot session

- Automatically processes and indexes uploaded documents into the vector database

- Enables immediate querying of new content without restarting the system

### **3️⃣ Chatbot with Vector Search Integration**

- Accepts user questions during chat sessions

- Translates questions into embeddings for vector search

- Retrieves relevant content chunks from the vector database

- Combines model instructions, chat history, and retrieved context to generate a response

### **4️⃣ Document Summarization Pipeline**

- Splits documents (e.g., PDFs) into pages

- Each page is summarized individually using GPT

- Final summaries are compiled and passed to a second GPT model

- The second model produces a comprehensive "summary of summaries" for improved understanding


## Project Flow
![](https://github.com/dhavalantala/RAG_GPT/blob/740e74c81c1b88d22b440aba0a6c99fccb372a2f/images/RAGGPT_schema.png)


## **⚠️ Known Limitations**

**1. Second GPT Model Context Length**

- Each page of a document produces a summary.

- Large documents (e.g., 2,000 pages) lead to thousands of summaries, exceeding GPT's context window.

- Potential workaround: Recursive summarization — summarize batches of summaries until the content fits within the model's input limits.

**2. API Call Rate Limits**

- Large documents generate a high number of API calls (one per page during summarization).

- Be aware of API rate limits or quota restrictions from your LLM provider.

- For extensive documents, batching, throttling, or upgraded API access may be required.

**Note**: The system is optimized for documents up to ~50 pages, such as academic papers or short reports. It can be expanded for larger use cases, but additional engineering is needed to address the limitations above.