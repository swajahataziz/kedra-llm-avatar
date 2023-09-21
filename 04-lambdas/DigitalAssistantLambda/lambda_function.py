import json
import boto3

s3 = boto3.client('s3')
s3_res = boto3.resource('s3')
bedrock = boto3.client("bedrock")
kendra = boto3.client("kendra")
comprehend = boto3.client("comprehend")

index_id = 'e80e68b3-2e4d-4e27-969c-fe36ea3dcd65'
bucket = ''
prefix = 'kendra/'
fulfillment_state = 'Fulfilled'
closure_phrases = [
    "thank you",
    "thanks",
    "perfect, thank you",
    "perfect thank you",
    "perfect, thanks",
    "perfect thanks",
    "awesome, thank you",
    "awesome thank you",
    "awesome, thanks",
    "awesome thanks",
    "amazing, thank you",
    "amazing thank you",
    "amazing, thanks",
    "amazing thanks"
]

model = "CLAUDE-INSTANT"

def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']

def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}

def elicit_intent_text(intent_request, session_attributes, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [message] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def elicit_slot(intent_request, session_attributes, message):
    intent_request['sessionState']['intent']['state'] = 'InProgress'

    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': 'Question'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message]
    }

def elicit_slot_im(intent_request, session_attributes, message, response_card):
    intent_request['sessionState']['intent']['state'] = 'InProgress'

    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': 'Question'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message, response_card]
    }

def close(intent_request, session_attributes, fulfillment_state, message, response_card):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'intent': intent_request['sessionState']['intent'],
            'dialogAction': {
                'type': 'Close',
                },
            },
            'messages':[message, response_card]
        }
def close_text(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'intent': intent_request['sessionState']['intent'],
            'dialogAction': {
                'type': 'Close',
                },
            },
            'messages':[message]
        }

def FallbackIntent(intent_request):
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)

    text = "Can you please try rephrasing your question?"
    message =  {
            'contentType': 'PlainText',
            'content': text
        }
    return elicit_slot(intent_request, session_attributes, message)

def call_bedrock(query, faq_result, max_tokens=1024, stop_sequences=[], temperature=0.2, top_p=0.9, model_type="CLAUDE-INSTANT", verbose=False):
    if model_type == "TITAN":
        if faq_result == "" or faq_result == " ":
            template = f"""
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """
        else:
            template = f"""
                Human: Answer from {faq_result}.
                
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """

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
        if faq_result == "" or faq_result == " ":
            template = f"""
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent at Jeep.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """

        else:
            template = f"""
                Human: Answer from {faq_result}.
                
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent at Jeep.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """

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
        if faq_result == "" or faq_result == " ":
            template = f"""
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent at Jeep.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """
        else:
            template = f"""
                Human: Answer from {faq_result}.
                
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent at Jeep.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """

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
        if faq_result == "" or faq_result == " ":
            template = f"""
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent at Jeep.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """
        else:
            template = f"""
                Human: Answer from {faq_result}.
                
                Human: You are Stella, an automotive specialist agent. You only answer questions related to vehicles, automotive and you are specialized on Jeep.
                Do not answer questions not related to your role. Keep the answer conversational. Please keep the answer between 50 to 60 words as a reply in a natural conversation without preamble.
                Assistant: OK, got it, I'll be Stella, a talkative truthful automotive specialist agent at Jeep.
                
                Human: If questions topics are vehicles, or automotive in general, but are not related to Jeep, you should answer the question but propose a Jeep alternative at the end.
                Assistant: OK, I will propose a Jeep alternatives only if questions are not related to Jeep.
                
                Human: Hi
                Assistant: Hello , my name is Stella, How may I help you today? please note that these chats maybe recorded for training or quality assurance purposes.

                Human: {query}
                Assistant:
            """

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

    print("Template:")
    print(template)

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
        result_text = json_obj['completion'].strip()
    elif model_type == "J2":
        result_text = json_obj['completions'][0]['data']['text'].strip()
    else:
        raise Exception("Unsupported model")

    return result_text

def call_kendra(query_string):
    print("Function call_kendra")

    response = kendra.query(
        QueryText=query_string,
        IndexId=index_id)
    print(response['ResultItems'])
    d = 0
    a = 0
    answer_text = ''
    document_text = ''
    for query_result in response["ResultItems"]:

        print("-------------------")
        print("Type: " + str(query_result["Type"]))

        if query_result["Type"] == "ANSWER":
            a += 1
            if a <= 1:
                answer_text = query_result["DocumentExcerpt"]["Text"]

            print(answer_text)

        if query_result["Type"] == "DOCUMENT":
            d += 1
            if "DocumentTitle" in query_result:
                document_title = query_result["DocumentTitle"]["Text"]
                print("Title: " + document_title)
            if d <= 3:
                document_text += query_result["DocumentExcerpt"]["Text"]
            print(document_text)

    result = answer_text + ' ' + document_text

    return result

def call_kendra_faq(query_string):
    print("Function call_kendra_faq")

    a = 0
    answer_text = ""

    response = kendra.query(
        QueryText=query_string,
        IndexId=index_id)

    print(response['ResultItems'])

    for query_result in response["ResultItems"]:

        print("-------------------")
        print("Type: " + str(query_result["Type"]))

        if query_result["Type"] == "ANSWER" or query_result["Type"] == "QUESTION_ANSWER":
            a += 1
            if a <= 1:
                answer_text = query_result["DocumentExcerpt"]["Text"]

            print(answer_text)

    faq_result = answer_text

    return faq_result

def GetAutoAnswers(intent_request):
    session_attributes = get_session_attributes(intent_request)
    answer = ''
    slots = get_slots(intent_request)
    print('Slot values are: ' + str(slots))
    # Get question
    query = str(get_slot(intent_request,'Question'))
    print('query is:  ' + query)

    # pii_list = []
    # sentiment = comprehend.detect_sentiment(Text=query, LanguageCode='en')['Sentiment']
    # resp_pii = comprehend.detect_pii_entities(Text=query, LanguageCode='en')
    # for pii in resp_pii['Entities']:
    #     if pii['Type'] not in ['ADDRESS', 'DATE_TIME']:
    #         pii_list.append(pii['Type'])
    # if len(pii_list) > 0:
    #     answer = "I am sorry but I found PII entities " + str(pii_list) + " in your query. Please remove PII entities and try again."
    #     message = {
    #         'contentType': 'PlainText',
    #         'content': answer
    #     }
    #     return elicit_slot(intent_request, session_attributes, message)

    if query.lower() == "cancel":
        message = {
            'contentType': 'PlainText',
            'content': "It was swell chatting with you. Goodbye for now"
        }
        return close_text(intent_request, session_attributes, fulfillment_state, message)
    elif query.lower() in closure_phrases:
        message = {
            'contentType': 'PlainText',
            'content': "You are welcome. Is there anything else I can help you with?"
        }
        return elicit_slot(intent_request, session_attributes, message)

    else:
        print('Original query: ' + query)
        faq_result = call_kendra_faq(query)
        print("now calling anthropic with: *" + faq_result+"*")

        answer = call_bedrock(
            query,
            faq_result,
            model_type=model)
        print("Answer is: " + answer)
        message =  {
            'contentType': 'PlainText',
            'content': answer
        }

        return elicit_slot(intent_request, session_attributes, message)

def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'AskAmari':
        return GetAutoAnswers(intent_request)
    elif intent_name == 'FallbackIntent':
        return FallbackIntent(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    print(event)
    response = dispatch(event)
    return response
