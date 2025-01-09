from datetime import datetime

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from model import CustomEvent
from prompt import application_prompt


def generate_event_from_text_input(user_text: str):
    timestamp = datetime.now().isoformat()

    llm = ChatOllama(model="llama3.2")

    structured_llm = llm.with_structured_output(CustomEvent)

    prompt = PromptTemplate(
        template=application_prompt,
        input_variables=["user_text", "timestamp"]
    )

    formatted_prompt = prompt.format(user_text=user_text, timestamp=timestamp)

    try:
        response = structured_llm.invoke(formatted_prompt)
    except Exception as e:
        print(f"Error during model invocation: {e}")
        response = None

    return response
