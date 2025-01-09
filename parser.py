from langchain_ollama import ChatOllama

from model import CustomEvent


def generate_event_from_text_input(user_text: str):
    llm = ChatOllama(model="llama3.2")
    structured_llm = llm.with_structured_output(CustomEvent)

    response = structured_llm.invoke(user_text)

    return response
