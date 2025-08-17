import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv


load_dotenv()

## langsmith tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = "Q&A Chatbot with OpenAI"

## prompt template
prompt = ChatPromptTemplate.from_messages(
    [
    ("system", "You are a helpful assistant. Please reesponse to the user queries"),
    ("user", "Question: {question}"),
    ]
    )

def generate_response(question, api_key,llm, temperature, max_tokens):
    
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain = prompt|llm| output_parser
    answer = chain.invoke({"question": question})
    return answer

## title of the app
st.title("Enhanced Q&A Chatbot with OpenAI")

##side bar for settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your AI API Key", type="password")

#dropdown for model selection
llm = st.sidebar.selectbox(
    "Select the Open AI Model",
    ["gpt-4o", "gpt-4-turbo", "gpt-4"]
)

## adjust response parameters
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

## Main interface for user input
st.write("Go ahead and ask your question!")
user_input = st.text_input("Your Question:")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get a response.")