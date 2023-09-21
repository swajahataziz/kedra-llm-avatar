import boto3
import json
import streamlit as st
from streamlit_chat import message
from random import randint
import os


bedrock = boto3.client('bedrock')

def generate_answer(query, model_type="CLAUDE-INSTANT", max_tokens=50, stop_sequences=["\n\nHuman:"], temperature=0.2, top_p=0.9, verbose=True):
    template = f"""
    
        Human: You are Amari, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
        Do not answer questions not related to your role. Keep the answer conversational.
        Assistant: OK, got it, I'll be Amari, a talkative truthful automotive specialist agent.
        Human: Provide a detailed answer for {query}  

        Assistant:

    """

    if model_type == "TITAN":
        model_id = "amazon.titan-tg1-large"

        body = {
            "inputText": template,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": temperature,
                "topP": top_p,
                "stopSequences": stop_sequences
            }
        }
        body_string = json.dumps(body)
    elif model_type == "CLAUDE":
        model_id = "anthropic.claude-v1"

        body = {
            "prompt": template,
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stop_sequences": stop_sequences
        }
        body_string = json.dumps(body)
    elif model_type == "CLAUDE-INSTANT":
        model_id = "anthropic.claude-instant-v1"

        body = {
            "prompt": template,
            "max_tokens_to_sample": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stop_sequences": stop_sequences
        }
        body_string = json.dumps(body)
    elif model_type == "J2":
        model_id = "ai21.j2-jumbo-instruct"

        body = {
            "prompt": template,
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p,
            "stopSequences": stop_sequences
        }
        body_string = json.dumps(body)
    else:
        raise Exception("Unsupported model")

    response = bedrock.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body_string)

    json_obj = json.loads(response.get("body").read().decode())

    if verbose:
        json_formatted_str = json.dumps(json_obj, indent=2)
        print(json_formatted_str)

    if model_type == "TITAN":
        result_text = json_obj['results'][0]['outputText'].strip()
    elif model_type == "CLAUDE" or model_type == "CLAUDE-INSTANT":
        result_text = json_obj.get('completion').strip()
    elif model_type == "J2":
        result_text = json_obj['completions'][0]['data']['text'].strip()
    else:
        raise Exception("Unsupported model")

    return result_text

# initialise session variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'widget_key' not in st.session_state:
    st.session_state['widget_key'] = str(randint(1000, 100000000))

# Sidebar - the clear button is will flush the memory of the conversation
st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['widget_key'] = str(randint(1000, 100000000))

response_container = st.container()
container = st.container()

with container:
    # define the input text box
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    # when the submit button is pressed we send the user query to the chatchain object and save the chat history
    if submit_button and user_input:
        output = generate_answer(user_input, model_type="CLAUDE")
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
    # when a file is uploaded we also send the content to the chatchain object and ask for confirmation

# this loop is responsible for displaying the chat history
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
