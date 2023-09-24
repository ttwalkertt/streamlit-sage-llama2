import streamlit as st

#st.markdown("# Main page 🎈")
#st.sidebar.markdown("# Main page 🎈")



import streamlit as st
import boto3
import json

if "ctr" not in st.session_state:
    st.session_state.ctr = 0
st.session_state.ctr += 1
print(st.session_state.ctr)
endpoint_name = "jumpstart-dft-meta-textgeneration-llama-2-13b-f"
st.session_state.default_system_prompt = """You are a chatbot. Your user is technically astute in computing hardware and system software. 
Be helpful, 
do not include too many pleasantries.
Do not ask about any further questions or topics I'd like to discuss."""
st.title(f"💬 Chatbot on {endpoint_name}f") 
st.caption('🚀 A streamlit chatbot powered by llama2 on Sagemaker LLM.')

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = st.session_state.default_system_prompt   

if "new_system_prompt" not in st.session_state:
    st.session_state.new_system_prompt = st.session_state.system_prompt

if "clear_chat" not in st.session_state:
    st.session_state.clear_chat = True
    
if st.session_state.new_system_prompt != st.session_state.system_prompt:
    st.session_state.clear_chat = True

def clear_chat():
    print("============== clearing chat ======================")
    st.session_state.messages = []
    print(f"system prompt: {st.session_state.system_prompt}\n")
    st.session_state.clear_chat = False
    
    
if st.session_state.clear_chat:
    clear_chat()
    
def query_endpoint(payload):
    client = boto3.client("sagemaker-runtime", region_name="us-east-1")
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )
    response = response["Body"].read().decode("utf8")
    response = json.loads(response)
    return response

with st.sidebar:
    "Chat with llama2 via Sagemaker"
    'Prompt "clear" to reset chat'
    temperature = st.number_input('Temperature', min_value=0.1, max_value=1.0, value=0.6, step=0.1)
    max_new_tokens = st.number_input('Max new tokens', min_value=128, max_value=4096, value=512, step=128)
    top_p = st.number_input('Top p', min_value=0.0, max_value=1.0, value=0.9, step=0.1)
    st.session_state.new_system_prompt = st.text_area('System Prompt:',  st.session_state.system_prompt)  
    if st.button("Reset System Prompt"):
        print("reset system prompt button")
        st.session_state.system_prompt = st.session_state.default_system_prompt
        st.experimental_rerun()
    if st.session_state.new_system_prompt != st.session_state.system_prompt:
        st.session_state.system_prompt = st.session_state.new_system_prompt
        st.session_state.clear_chat = True
        st.experimental_rerun()

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
