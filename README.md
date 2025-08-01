# 🧠 RAG GPT — Retrieval-Augmented Generation with GPT

**RAG GPT** is a modular system for document ingestion, vector search, summarization, and conversational interaction powered by GPT models. It combines a Vector Database with GPT-based summarization and chat functionality to provide document understanding and interactive querying.

RAG-GPT supports both **PDF** and **DOCX** document formats, offering flexible, real-time document interaction with an intuitive user interface.

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

## **💡 Key Features**

- ✅ Chatbot supports three interaction modes:

    - **Offline Document**s: Pre-ingested and vectorized documents ready for querying

    - **Real-Time Uploads**: Upload documents during chat for instant processing

    - **Summarization Requests**: Generate comprehensive summaries on demand

- ✅ Simple interface with **Gradio** for document upload, chat interaction, and result visualization

- ✅ Persistent chat memory for enhanced, context-aware conversations

- ✅ View retrieved content chunks alongside GPT responses for transparency

- ✅ Configurable GPT settings, such as temperature control, for response tuning

## **🖥️ User Interface Preview**

Here is a screenshot of the RAG-GPT chatbot interface:

![RAG-GPT Chatbot Screenshot](images/GUI.png)

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

## **🚀 Running the Project**

To get the project up and running, follow these simple steps to configure your environment and run the application.

### **🔧 Environment Setup**

Follow these steps to set up your environment and run the application:

### 🔧 Installation

1. Navigate to the project root:
    ```
    cd RAG-GPT
    ```

2. Install all required dependencies using the provided `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```

### ⚙️ Configuration

1. Create a `.env` file in the project root directory.

2. Add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

### ▶️ Running the Application
1. Start the backend service: 
    ```
    python src/serve.py
    ```

2. In a new terminal, run the Gradio chatbot interface:
    ```
    python src/raggpt_app.py
    ```

- After launching, you should see an output like:
server{
    Running on local URL:  http://127.0.0.1:7860
}

### 💬 Start Chatting

- Open your browser and go to `http://127.0.0.1:7860`.

- Upload documents, ask questions, or request summaries through the chatbot interface.



## 🆘 Troubleshooting

For port management and common setup issues, refer to [TROUBLESHOOTING.md](./TROUBLESHOOTING.md).
