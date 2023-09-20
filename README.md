# streamlit-sage-llama2
A Streamlit chat interface to an AWS Sagemaker hosted llama2 LLM

Have your AWS credentials in the ususal place.

## Setup:
pip -r requiements.txt

## Run:
streamlit run streamlit-chat-llama2.py

It's a straightforward chatbot application using streamlit's chat model. Use the sidebar to adjust the model settings as well as the system prompt.

<img width="1174" alt="image" src="https://github.com/ttwalkertt/streamlit-sage-llama2/assets/3143588/8b4c9dc7-a9b6-4c8f-9e9b-5bd8ba6807f3">

The general architecture is compatible with any Sagemaker LLM endpoint, but query payload is llama2 specific:
```
payload = {
        "inputs": [st.session_state.messages], 
        "parameters": {"max_new_tokens": max_new_tokens, "top_p": top_p, "temperature": temperature}
    }
```
as well as the query_endpoint(payload) function:
```
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
```
