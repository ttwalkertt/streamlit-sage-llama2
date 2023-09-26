import streamlit as st
import os

st.title("System Prompt Library")

system_prompt_file = "system_prompt_library.txt"

def display_prompts_with_radio_and_delete_button():
    """
    Display a list of system prompts with radio buttons and a delete button.
    
    Returns:
    - None
    """
 
    
    # Load system prompts from system_prompt.txt
    try:
        with open(system_prompt_file, "r") as f:
            system_prompts = f.read().splitlines()
    except FileNotFoundError:
        # Default system prompts
        system_prompts = st.session_state.default_system_prompts
        for p in system_prompts:
            p = p.replace('/n', ' ')
    
    # Initialize st.session_state.system_prompt if not
    if "selected_system_prompt" not in st.session_state:
        st.session_state.selected_system_prompt = ""

    # Display radio buttons next to each prompt
    if "system_prompt_index" not in st.session_state:
        st.session_state.system_prompt_index = 0
    selected_prompt = st.radio("Select a system prompt:", system_prompts, index = st.session_state.system_prompt_index)
    
    # Display the selected prompt
    if selected_prompt:
        st.session_state.selected_system_prompt = selected_prompt
        st.write(f"You have selected: {st.session_state.selected_system_prompt}")
        st.session_state.clear_chat = True
        st.session_state.system_prompt_index = system_prompts.index(selected_prompt)
    
    # Delete button to archive the selected prompt
    if st.button("Delete"):
        if selected_prompt:
            # Remove the selected prompt from the original list
            system_prompts.remove(selected_prompt)
            # Save the updated list to the file
            with open(system_prompt_file, "w") as f:
                for prompt in system_prompts:
                    prompt = prompt.replace('\n',' ')
                    f.write(f"{prompt}\n")
            st.write(f"{selected_prompt} has been archived.")
            st.experimental_rerun()
        else:
            st.write("No prompt selected to delete.")
    
    if st.button("Reset"):
        system_prompts = st.session_state.default_system_prompts
        with open(system_prompt_file, "w") as f:
                for prompt in system_prompts:
                    prompt = prompt.replace('\n',' ')
                    f.write(f"{prompt}\n")
        st.session_state.clear_chat = True
        st.experimental_rerun()
         
    
    # Text input box for new system prompt
    new_prompt = st.text_input("Add a new system prompt:")
    
    # Button to add new system prompt
    if st.button("Add System Prompt"):
        if new_prompt:
            # Add the new prompt to the list
            system_prompts.append(new_prompt)
            # Save the updated list to the file
            with open(system_prompt_file, "w") as f:
                for prompt in system_prompts:
                    prompt = prompt.replace('\n',' ')
                    f.write(f"{prompt}\n")
            # Make the new prompt the selected one
            st.session_state.selected_system_prompt = new_prompt
            st.write(f"New system prompt added: {new_prompt}")
            st.session_state.clear_chat = True
            st.experimental_rerun()

# Call the function to display the prompts with radio buttons and delete button
display_prompts_with_radio_and_delete_button()
