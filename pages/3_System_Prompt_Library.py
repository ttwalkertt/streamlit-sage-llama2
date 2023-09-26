import streamlit as st
import os
import json

# Set the title for the Streamlit app
st.title("System Prompt Library")

# File to store system prompts in JSON format
system_prompt_file = "system_prompt_library.json"

def display_prompts_with_radio_and_delete_button():
    """
    Display a list of system prompts with radio buttons and a delete button.
    
    This function reads system prompts from a JSON file, allows the user to select, delete, 
    and add new prompts. The selected prompt is stored in the session state.
    
    Returns:
    - None
    """
    
    # Load system prompts from system_prompt_library.json
    try:
        with open(system_prompt_file, "r") as f:
            system_prompts = json.load(f)
    except FileNotFoundError:
        # Use default system prompts if file not found
        system_prompts = st.session_state.default_system_prompts
        for p in system_prompts:
            p = p.replace('/n', ' ')
    
    # Initialize selected_system_prompt in session state if not already present
    if "selected_system_prompt" not in st.session_state:
        st.session_state.selected_system_prompt = ""

    # Display radio buttons for each system prompt
    if "system_prompt_index" not in st.session_state:
        st.session_state.system_prompt_index = 0
    selected_prompt = st.radio("Select a system prompt:", system_prompts, index=st.session_state.system_prompt_index)
    
    # Update session state with the selected prompt
    if selected_prompt:
        st.session_state.selected_system_prompt = selected_prompt
        st.write(f"You have selected: {st.session_state.selected_system_prompt}")
        st.session_state.clear_chat = True
        st.session_state.system_prompt_index = system_prompts.index(selected_prompt)
    
    # Delete button to remove the selected prompt
    if st.button("Delete"):
        if selected_prompt:
            system_prompts.remove(selected_prompt)
            with open(system_prompt_file, "w") as f:
                json.dump(system_prompts, f)
            st.write(f"{selected_prompt} has been archived.")
            st.experimental_rerun()
        else:
            st.write("No prompt selected to delete.")
    
    # Reset button to restore default system prompts
    if st.button("Reset"):
        system_prompts = st.session_state.default_system_prompts
        with open(system_prompt_file, "w") as f:
            json.dump(system_prompts, f)
        st.session_state.clear_chat = True
        st.experimental_rerun()

    # Text input for adding a new system prompt
    new_prompt = st.text_input("Add a new system prompt:")
    
    # Button to add the new system prompt
    if st.button("Add System Prompt"):
        if new_prompt:
            system_prompts.append(new_prompt)
            with open(system_prompt_file, "w") as f:
                json.dump(system_prompts, f)
            st.session_state.selected_system_prompt = new_prompt
            st.write(f"New system prompt added: {new_prompt}")
            st.session_state.clear_chat = True
            st.experimental_rerun()

# Call the function to display the UI elements
display_prompts_with_radio_and_delete_button()
