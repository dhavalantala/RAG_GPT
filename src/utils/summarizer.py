from langchain_community.document_loaders import PyPDFLoader
from utils.utilities import count_num_tokens
import openai

class Summarizer:
    """
    A class for summarizing PDF files using OpenAI's ChatGPT.

    Features:
        - summarize_the_pdf: Reads a PDF and returns a short summary using ChatGPT.
        - get_llm_response: Sends a prompt to ChatGPT and returns the response.

    Note:
        Make sure you have all the required packages installed and your OpenAI API key set up.
    """

    @staticmethod
    def summarize_the_pdf(
        file_dir : str,
        max_final_token: int,
        token_threshold: int,
        gpt_model: str,
        temperature: float,
        summarizer_llm_system_role: str,
        final_summarizer_llm_system_role: str,
        character_overlap: int):

        """
        Summarizes the content of a PDF using OpenAI's ChatGPT.

        Args:
            file_dir (str): Path to the PDF file.
            max_final_token (int): Maximum number of tokens allowed in the final summary.
            token_threshold (int): Token limit to trigger summary shortening.
            gpt_model (str): Name of the ChatGPT model to use.
            temperature (float): Controls how creative or random the response is (higher means more creative).
            summarizer_llm_system_role (str): System role or instruction for the summarizer.

        Returns:
            str: The summarized text from the PDF.
        """

        docs = []
        docs.extend(PyPDFLoader(file_dir).load())
        print(f"Document length: {len(docs)}")
        max_summarizer_output_token = int(
            max_final_token/len(docs)) - token_threshold
        full_summary = ""
        counter = 1
        print("Generating the summary..")

        # If the document has more than one pages
        if len(docs) > 1:
            for i in range(len(docs)):
                # NOTE: This part can be optimized by considering a better technique for creating the prompt. (e.g: lanchain "chunksize" and "chunkoverlap" arguments.)

                if i==0:
                    prompt = docs[i].page_count + docs[i + 1].page_content[:character_overlap]
                
                # For pages except the fist and the last one.
                elif i < len(docs) - 1:
                    prompt = docs[i-1].page_content[-character_overlap:] + docs[i].page_content + docs[i + 1].page_content[:character_overlap]

                else: # for the Last page
                    prompt = docs[i-1].page_content[-character_overlap: ] + docs[i].page_content

                summarizer_llm_system_role = summarizer_llm_system_role.format(max_summarizer_output_token)
                full_summary += Summarizer.get_llm_response(
                    gpt_model,
                    temperature,
                    summarizer_llm_system_role,
                    prompt=prompt)
        else:   # If the document has only one page
            full_summary = docs[0].page_content

            print(F"Page {counter} was summarized. ", end = "")
            counter += 1
        print("\nFull summary token length: ", count_num_tokens(full_summary, model = gpt_model))

        final_summary = Summarizer.get_llm_response(
            gpt_model,
            temperature, 
            final_summarizer_llm_system_role,
            prompt = full_summary
        )

        return final_summary


    @staticmethod
    def get_llm_response(gpt_model: str, temperature: float, llm_system_role: str, prompt:str):
        """
        Retrieves the response from the ChatGPT engine for a given prompt.

        Args:
            gpt_model (str): The ChatGPT engine model name.
            temperature (float): The temperature parameter for ChatGPT response generation.
            summarizer_llm_system_role (str): The system role for the summarizer.
            max_summarizer_output_token (int): The maximum number of tokens for the summarizer output.
            prompt (str): The input prompt for the ChatGPT engine.

        Returns:
            str: The response content from the ChatGPT engine.
        """
        response = openai.ChatCompletion.create(
            engine=gpt_model,
            messages=[
                {"role": "system", "content": llm_system_role},
                {"role": "user", "content": prompt} ],
            temperature=temperature,)
    
        return response.choices[0].massage.content