from utils.prepare_vectordb import PrepareVectorDB
from typing import List, Tuple
from utils.load_config import LoadConfig
from utils.summarizer import Summarizer

APPCFG = LoadConfig()


class UploadFile:
    """
    Utility class for managing file uploads and processing.

    This class provides helpful methods to:
    - Check if directories exist
    - Process uploaded files
    - Prepare files for building a Vector Database (VectorDB)
    """

    @staticmethod
    def process_uploaded_files(files_dir: List, chatbot: List, rag_with_dropdown:str) -> Tuple:
        """
        Processes uploaded files to prepare them for building a Vector Database (VectorDB).

        Args:
            files_dir (List): List of file paths for the uploaded files.
            chatbot: The chatbot instance used for showing messages or updates.

        Returns:
            Tuple: Returns an empty string and the updated chatbot instance.
        """

        if rag_with_dropdown == "Upload doc: Process for RAG":
            prepare_vectordb_instance = PrepareVectorDB(data_directory=files_dir,
                                                        persist_directory=APPCFG.custom_persist_directory,
                                                        embedding_model_engine=APPCFG.embedding_model_engine,
                                                        chunk_size=APPCFG.chunk_size,
                                                        chunk_overlap=APPCFG.chunk_overlap)
            
            prepare_vectordb_instance.perpare_and_save_vectordb()
            chatbot.append((" ", "Upload files are ready. Please ask your question"))

        elif rag_with_dropdown == "Upload doc: Give Full Summary":
            final_summary = Summarizer.summarize_the_pdf(file_dir=files_dir[0],
                                                         max_final_token=APPCFG.max_final_token, 
                                                         token_threshold=APPCFG.token_threshold,
                                                         gpt_model=APPCFG.llm_engine,
                                                         temperature=APPCFG.temperature,
                                                         summarizer_llm_system_role=APPCFG.summarizer_llm_system_role,
                                                         final_summarizer_llm_system_role=APPCFG.final_summarizer_llm_system_role,
                                                         character_overlap=APPCFG.character_overlap)
            chatbot.append(
                (" ", final_summary)
            )
        
        else:
            chatbot.append(
                (" ", "If you would like to upload a PDF, please select your desired action in 'RAG with' dropdown.")
            )

        return "", chatbot