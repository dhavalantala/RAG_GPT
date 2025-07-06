"""
This module creates a simple chatbot web app using Gradio.

The app has three main sections:
1. At the top, there's a Chatbot where you can chat with the model. There's also a hidden reference bar that you can show or hide with a button. You can give feedback with like/dislike buttons.
2. In the middle, there's a box to type your message or upload PDF/doc files.
3. At the bottom, there are buttons to:
   - Submit your message
   - Show/hide the reference bar
   - Upload files
   - Change response temperature (controls how creative the bot is)
   - Select document type
   - Clear the chat

How it works:
- If you upload a file, the app processes it and updates the chatbot and input box.
- If you type a message and submit, the chatbot replies, using your selected settings.
- The reference bar may update based on the response.

You can run this module as a standalone app to interact with the chatbot in your browser.

The code also has more detailed comments explaining each part.
"""

import gradio as gr
from utils.upload_file import UploadFile
from utils.chatbot import ChatBot
from utils.ui_settings import UISettings

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("RAG-GPT"):
            ##############
            # First ROW:
            ##############

            with gr.Row() as row_one: 
                with gr.Column(visible=False) as reference_bar:
                    ref_output = gr.Markdown()

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id = "chatbot",
                        bubble_full_width = False,
                        height=500,
                        avatar_images=(
                            ("images/icons8-user-96.png"), "images/icons8-chatbot-94.png"),
                        # render=False
                    )
                    # **Adding like/dislike icons
                    chatbot.like(UISettings.feedback, None, None)
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Enter text and press enter, or upload PDF files",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="References")
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                upload_btn = gr.UploadButton(
                    "📁 Upload PDF or doc files", file_types=[
                        '.pdf',
                        '.doc'
                    ],
                    file_count="multiple")
                temperature_bar = gr.Slider(minimum=0, maximum=1, value=0, step=0.1,
                                            label="Temperature", info="Choose between 0 and 1")
                rag_with_dropdown = gr.Dropdown(
                    label="RAG with", choices=["Preprocessed doc", "Upload doc: Process for RAG", "Upload doc: Give Full Summary"], value="Preprocessed doc")
                clear_button = gr.ClearButton([input_txt, chatbot])

            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[
                upload_btn, chatbot, rag_with_dropdown], outputs=[input_txt, chatbot], queue=False)

            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown, temperature_bar],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=ChatBot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown, temperature_bar],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    demo.launch()