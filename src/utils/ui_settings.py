import gradio as gr

class UISettings:
    """
    Utility class for managing UI settings.

    Provides methods to show or hide UI elements like the sidebar.
    """

    @staticmethod
    def toggle_sidebar(state):
        """
        Toggles the visibility of a UI component.

        Args:
            state: The current visibility state of the UI component.

        Returns:
            Tuple: The updated component state and its new visibility state.
        """
        state = not state

        return gr.update(visible=state), state
    
    @staticmethod
    def feedback(data: gr.LikeData):
        """
        Handles user feedback on the chatbot's response.

        Args:
            data (gr.LikeData): Gradio LikeData object with the user's feedback.

        Prints whether the response was upvoted or downvoted along with the response text.
        """
        if data.liked:
            print("You upvoted this response: " + data.value)
        else:
            print("You downvoted this response: " + data.value)