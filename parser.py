from datetime import datetime
from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from pydantic import BaseModel, Field

from langchain_core.output_parsers import PydanticOutputParser

application_prompt = """
You are an AI assistant that converts free-form text into a JSON representation of an iCalendar VEvent. 
Your output must be valid JSON that follows the Pydantic model structure for the VEvent class. 
In other words, you will produce JSON where:
- The top-level keys are `properties` and optionally `alarms`.
- `properties` must match the fields of `EventProperties` (e.g., UID, DTSTAMP, DTSTART, DTEND, SUMMARY, etc.).
- `alarms` (if present) is an array of objects, each having a `properties` field matching `AlarmProperties`.

Important rules:
1. **Do not** add extra keys outside those defined in the Pydantic model.
2. Only fill in fields you have evidence for. If the user text does not provide a certain property (e.g., location), omit it.
3. Always include a unique `UID` and a `DTSTAMP`.
4. Format all date/time fields as valid ISO 8601 strings (e.g., `"2025-12-31T09:00:00"`).
5. Do not include markdown or additional explanatory text—only valid JSON.

Below is the user’s text and the current timestamp. 
Use the user’s text to infer ICS event details (e.g., start time, end time, summary, location). 
Then, produce the final JSON accordingly.

User text: {user_text}
Current timestamp: {timestamp}
"""


class CustomEvent(BaseModel):
    """Class to represent .ics file event details based on user input"""
    uid: str = Field(description="Unique identifier for the event")
    summary: str = Field(description="Summary or title of the event")
    description: str = Field(description="Detailed description of the event (default to empty string)")
    location: str = Field(description="Location of the event if provided (default to empty string)")
    start: datetime = Field(description="Start time of the event")
    end: datetime = Field(description="End time of the event")
    attendees: List[str] = Field(default_factory=list, description="List of attendees (email addresses)")


def generate_event_from_text_input(user_text: str):
    timestamp = datetime.now().isoformat()

    # Add logging to trace the execution
    print(f"Initializing with timestamp: {timestamp}")

    try:
        parser = PydanticOutputParser(pydantic_object=CustomEvent)

        prompt = PromptTemplate(
            template=application_prompt,
            input_variables=["user_text", "timestamp"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        print("Structured output configured")

        llm = OllamaLLM(model="mistral:latest")

        ollama_server_check()
        print("LLM initialized successfully")

        chain = prompt | llm | parser

        try:
            response = chain.invoke({"user_text": user_text, "timestamp": timestamp})
            print(f"Raw response received: {response}")
            return response
        except Exception as e:
            print(f"Error during model invocation: {str(e)}")
            print(f"Exception type: {type(e)}")
            raise  # Re-raise the exception for debugging

    except Exception as e:
        print(f"Error during setup: {str(e)}")
        print(f"Exception type: {type(e)}")
        return None


def ollama_server_check():
    # Add this before creating the LLM to check if Ollama is running
    import requests
    try:
        requests.get('http://localhost:11434')
    except requests.exceptions.ConnectionError:
        print("Error: Ollama server is not running. Please start it first.")
        return None
