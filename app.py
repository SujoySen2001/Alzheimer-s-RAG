from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import torch
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import openai

openai.api_key = "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"
#pinecone_api_key = 'cff06254-079e-4469-be51-342d2bd0f05b'

pc=Pinecone(api_key='6fff7d16-e9f7-4344-b20c-02c3811047db')
index = pc.Index('project')



# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize LangChain components
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")
buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(
    template="""Answer the question as truthfully as possible using the provided context in a minimum of 200 words. Ensure the response is well-structured with proper spacing, and highlight important words in bold. If the answer includes multiple points, present the response in a clear point-by-point format with proper spacing between points. If the answer is not contained within the text below, say 'I do not know, because it is irrelevant to our context'."""
)
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Session state simulation

session_state = {
    'responses': ["Hello, Welcome to our chatBot?"],
    'requests': []
}
# Helper functions
# def find_match(input):
#     input_em = model.encode(input).tolist()
#     result = index.query(input_em, top_k=2, includeMetadata=True)
#     return result['matches'][0]['metadata']['text'] + "\n" + result['matches'][1]['metadata']['text']
def find_match(input):
    try:
        input_em = model.encode(input).tolist()
        result = index.query(vector=input_em, top_k=2, includeMetadata=True)
        if 'matches' in result and len(result['matches']) >= 2:
            return result['matches'][0]['metadata']['text'] + "\n" + result['matches'][1]['metadata']['text']
        else:
            return "No sufficient matches found in the index."
    except Exception as e:
        print(f"Error in find_match: {e}")
        return "An error occurred while querying the index."

def query_refiner(conversation, query):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.7,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    refined_query = response.choices[0].text.strip()
    return refined_query

def get_conversation_string(responses, requests):
    conversation_string = ""
    for i in range(len(responses) - 1):
        conversation_string += "Human: " + requests[i] + "\n"
        conversation_string += "Bot: " + responses[i + 1] + "\n"
    return conversation_string

def generate_alternative_questions(query):
    # Prompt to ask for three alternative questions related to the user query
    # prompt = f"Provide only 3 alternative questions related to '{query}' and give the alternative questions in simple english and it should be sounds good. You need not to give any numbering of the question"
    prompt=f"Provide three diverse, complete one-line questions related to '{query}' that delve into various aspects of the topic, ensuring they are straightforward and directly related. Avoid repeating the same content as the query.You need not to give any numbering of the question"
    
    # Generate three alternative questions
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100,
        n=1,  # Generate one completion at a time
        stop=None,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    alternatives = response.choices[0].text.strip().split('\n')
    return [alt.strip() for alt in alternatives if alt.strip()]