import gradio as gr
import time 
import openai
import os
from langchain_chroma import Chroma
from typing import List, Tuple
import re
import ast
import html
from utils.load_config import LoadConfig

APPCFG = LoadConfig()

class ChatBot:
    """
    Class for a chatbot that can retrieve documents and generate responses.

    Features:
        - Answers user questions
        - Handles feedback (like/dislike)
        - Cleans up references from retrieved documents

    """
    @staticmethod
    def respond(chatbot: List, message: str, data_type:str = "Preprocessed doc", temperature:float = 0.0) -> Tuple:
        """
        Generates a response to the user's question using document retrieval and a language model.

        Args:
            chatbot (List): The conversation history of the chatbot.
            message (str): The user's question.
            data_type (str): Type of document source ("Preprocessed doc" or "Upload doc: Process for RAG").
            temperature (float): Controls how creative the language model's response is (higher means more creative).

        Returns:
            Tuple: An empty string, the updated chat history, and any references from the retrieved documents.
        """
        if data_type == "Preprocessed doc":
            # directories
            if os.path.exists(APPCFG.persist_directory):
                vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                                  embedding_function=APPCFG.embedding_model)
            
            else:
                chatbot.append(
                    (message, f"VectorDB does not exist. Please first execute the 'upload_data_manually.py' module."))
                return "", chatbot, None
            
        elif data_type == "Upload doc: Process for RAG":
            if os.path.exists(APPCFG.custom_persist_directory):
                vectordb = Chroma(persist_directory=APPCFG.persist_directory,
                                  embedding_function=APPCFG.embedding_model)
            else:
                chatbot.append(
                    (message, f"No file was uploaded. Please first upload your files using the 'upload' button.")
                )
                return "", chatbot, None
            

        docs = vectordb.similarity_search(message, k = APPCFG.k)
        print(docs)
        question = "# User new question:\n" + message
        retrieved_content = ChatBot.clean_references(docs)

        # Memory: Previous two Q&A Pairs
        chat_history = f"Chat history:\n {str(chatbot[-APPCFG.number_of_q_a_pairs:])}\n\n"
        prompt = f"{chat_history}{retrieved_content}{question}"

        print("========================")
        print(prompt)
        response = openai.chat.completions.create(
            model=APPCFG.llm_engine,
            messages=[
                {"role": "system", "content": APPCFG.llm_system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,) 
        
        chatbot.append((message, response.choices[0].message.content))
        time.sleep(2)

        return "", chatbot, retrieved_content
    
    @staticmethod
    def clean_references(documents: List) -> str:
        """
        Cleans and formats references from retrieved documents.

        Args:
            documents (List): List of retrieved document results.

        Returns:
            str: A cleaned and nicely formatted string of references.
        """

        server_url = "http://localhost:8000"
        documents = [str(x)+"\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        for doc in documents:
            print(f"Raw doc:\n{doc}\n")  # Debug, remove later
            match = re.match(r"page_content=(.*?)(?:\s+)metadata=(\{.*\})", doc, re.DOTALL)
    
            if not match:
                print(f"[WARN] Regex did not match for document:\n{doc}\n")
                continue  # or handle as needed
            
            content, metadata = match.groups()
            metadata_dict = ast.literal_eval(metadata)

            # Decode newlines and other escape sequences
            content = bytes(content, "utf-8").decode("unicode_escape")

            # Replace escaped newlines with actual newlines
            content = re.sub(r'\\n', '\n', content)
            # Remove special tokens
            content = re.sub(r'\s*<EOS>\s*<pad>\s*', ' ', content)
            # Remove any remaining multiple spaces
            content = re.sub(r'\s+', ' ', content).strip()

            # Decode HTML entities
            content = html.unescape(content)

            # Replace incorrect unicode characters with correct ones
            content = content.encode('latin1').decode('utf-8', 'ignore')

            # Remove or replace special characters and mathematical symbols
            # This step may need to be customized based on the specific symbols in your documents
            content = re.sub(r'â', '-', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Ã', '×', content)
            content = re.sub(r'ï¬', 'fi', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Â·', '·', content)
            content = re.sub(r'ï¬', 'fl', content)

            pdf_url = f"{server_url}/{os.path.basename(metadata_dict['source'])}"

            # Append cleaned content to the markdown string with two newlines between documents
            markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n" + \
                f"Source: {os.path.basename(metadata_dict['source'])}" + " | " +\
                f"Page number: {str(metadata_dict['page'])}" + " | " +\
                f"[View PDF]({pdf_url})" "\n\n"
            counter += 1

        return markdown_documents