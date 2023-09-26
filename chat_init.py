import streamlit as st

def chat_init():
    """
    Initialize session state variables for the Streamlit chat application.
    
    This function sets up various session state variables that are used throughout the application.
    It checks if the initialization has already been done to avoid redundant operations.
    """
    
    # Check if initialization is already done
    if "init_done" in st.session_state and st.session_state.init_done:
        print("Initialization already done.")
        return
    
    # Counter for tracking the number of interactions or other metrics
    st.session_state.ctr = 0
    
    # default system prompts to guide the behavior of the chatbot
    st.session_state.default_system_prompts = [
        """You are a specialized chatbot designed for users with technical expertise. 
        Prioritize clarity and accuracy in your responses. If a query is ambiguous or lacks detail, 
        promptly ask for clarification. Eliminate unnecessary social formalities and never invent information.""",
        
        """You are a precision-oriented AI assistant. Your primary goal is to provide reliable and exact information. 
        In cases of vague or incomplete queries, your first step should be to seek additional details from the user. 
        Bypass any social niceties and always maintain factual integrity.""",
        
        """You are an ethical AI assistant committed to responsible interaction. 
        When faced with unclear or ambiguous questions, your protocol is to request further clarification to ensure accurate responses. 
        Omit superfluous pleasantries and uphold a strict policy against disseminating false or misleading information."""
    ]
    # Remove newline characters from all default system prompts 
    st.session_state.default_system_prompts = [prompt.replace('\n', ' ') for prompt in st.session_state.default_system_prompts]
    
    # Set the selected system prompt to the first default system prompt
    st.session_state.selected_system_prompt = st.session_state.default_system_prompts[0]
    
    # Initialize system prompt if not already set
    st.session_state.system_prompt = st.session_state.selected_system_prompt
    
    # Endpoint name for the text generation model
    st.session_state.endpoint_name = "jumpstart-dft-meta-textgeneration-llama-2-13b-f"
    
    # Flag to clear the chat, if needed
    st.session_state.clear_chat = True
    
    # Mark initialization as done
    st.session_state.init_done = True
