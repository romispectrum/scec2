from datetime import datetime

from ics import Calendar
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from model import create_ics_event, EventModel


class EventController:
    def __init__(self, view):
        self.view = view
        self.view.controller = self

    def handle_user_input(self, user_text):
        timestamp = datetime.now().isoformat()
        event_data = self.generate_event_data(user_text, timestamp)
        if event_data:
            # Now we return the ICS string generated by process_event_data
            return self.process_event_data(event_data)
        return None

    def generate_event_data(self, user_text, timestamp):
        try:
            parser = PydanticOutputParser(pydantic_object=EventModel)
            prompt = PromptTemplate(
                template=self.application_prompt,
                input_variables=["user_text", "timestamp"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )

            llm = OllamaLLM(model="mistral:latest")
            chain = prompt | llm | parser
            return chain.invoke({"user_text": user_text, "timestamp": timestamp})
        except Exception as e:
            print(f"Error generating event data: {e}")
            return None

    def process_event_data(self, event_data):
        try:
            event = create_ics_event(event_data.properties)
            calendar = Calendar()
            calendar.events.add(event)

            # Return the string representation of the calendar
            return str(calendar)
        except Exception as e:
            print(f"Error processing event data: {e}")
            return None

    @property
    def application_prompt(self):
        return """
        You are an AI assistant that converts free-form text into a JSON representation of an iCalendar Event. 
        Your output must be valid JSON that follows the Pydantic model structure for the Event class. 
        In other words, you will produce JSON where:
        - The top-level keys are `properties` and optionally `alarms`.
        - `properties` must match the fields of `EventProperties` (e.g., UID, DTSTAMP, DTSTART, DTEND, SUMMARY, etc.).
        - `alarms` (if present) is an array of objects, each having a `properties` field matching `AlarmProperties`.

        Important rules:
        1. **Do not** add extra keys outside those defined in the Pydantic model.
        2. Only fill in fields you have evidence for. If the user text does not provide a certain property (e.g., location), omit it.
        3. Format all date/time fields as valid ISO 8601 strings (e.g., "2025-12-31T09:00:00").
        4. Always include a unique `UID` and a `DTSTAMP`.
        5. Do not include markdown or additional explanatory text—only valid JSON.

        Below is the user’s text and the current timestamp. 
        Use the user’s text to infer ICS event details (e.g., start time, end time, summary, location). 
        Then, produce the final JSON accordingly.

        User text: {user_text}
        Current timestamp: {timestamp}
        """
