import streamlit as st

#st.markdown("# Main page 🎈")
#st.sidebar.markdown("# Main page 🎈")

import streamlit as st
import boto3
import json

from chat_init import chat_init
chat_init()

st.session_state.ctr += 1
print(st.session_state.ctr)

st.title(f"💬 Chatbot on {st.session_state.endpoint_name}f") 
st.caption('🚀 A streamlit chatbot powered by llama2 on Sagemaker LLM.')

def clear_chat():
    print("============== clearing chat ======================")
    st.session_state.messages = []
    print(f"system prompt: {st.session_state.system_prompt}\n")
    st.session_state.clear_chat = False
    
if st.session_state.clear_chat:
    clear_chat()
    
with st.sidebar:
    "Chat with llama2 via Sagemaker"
    'Prompt "clear" to reset chat'
    temperature = st.number_input('Temperature', min_value=0.1, max_value=1.0, value=0.6, step=0.1)
    max_new_tokens = st.number_input('Max new tokens', min_value=128, max_value=4096, value=512, step=128)
    top_p = st.number_input('Top p', min_value=0.0, max_value=1.0, value=0.9, step=0.1)
   # st.session_state.new_system_prompt = st.text_area('System Prompt:',  st.session_state.system_prompt)  
    
def query_endpoint(payload):
    client = boto3.client("sagemaker-runtime", region_name="us-east-1")
    response = client.invoke_endpoint(
        EndpointName=st.session_state.endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response


st.session_state.system_prompt = st.session_state.selected_system_prompt

if "messages" not in st.session_state or st.session_state.messages is None or len(st.session_state.messages) == 0:
    st.session_state.messages = []
    st.session_state["messages"] = [{"role": "system", "content":  st.session_state.system_prompt}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if prompt == "clear":
        st.session_state.clear_chat = True
        st.experimental_rerun()
        
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with open("log.txt", "a") as f:
        f.write(f"{st.session_state.messages}\n")
    # print(st.session_state.messages)
    payload = {
        "inputs": [st.session_state.messages], 
        "parameters": {"max_new_tokens": max_new_tokens, "top_p": top_p, "temperature": temperature}
    }
    response =  query_endpoint(payload)[0]
    
    #print(f"response: {response}")
    
    msg = response['generation']
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg['content'])
