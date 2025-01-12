import tempfile
from datetime import datetime

from ics import Calendar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import PydanticOutputParser
from custom_event import CustomEvent
from ics_creator import create_ics_event
from prompt import application_prompt


class FileSavePopup(Popup):
    def __init__(self, file_content, **kwargs):
        super().__init__(**kwargs)
        self.title = "Save File"
        self.file_content = file_content

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.file_chooser = FileChooserListView(filters=["*.ics"])
        layout.add_widget(self.file_chooser)

        save_button = Button(text="Save", size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_file)
        layout.add_widget(save_button)

        self.content = layout

    def save_file(self, instance):
        selected_path = self.file_chooser.path
        file_name = self.file_chooser.selection
        if selected_path and file_name:
            try:
                with open(f"{selected_path}/{file_name[0]}", "w") as file:
                    file.write(self.file_content)
                print(f"File saved successfully at: {selected_path}/{file_name[0]}")
                self.dismiss()
            except Exception as e:
                print(f"Error saving file: {e}")
        else:
            print("No path or file name selected.")


def generate_event_from_text_input(user_text: str):
    timestamp = datetime.now().isoformat()

    print(f"Initializing with timestamp: {timestamp}")

    ollama_server_check()

    try:
        parser = PydanticOutputParser(pydantic_object=CustomEvent)

        prompt = PromptTemplate(
            template=application_prompt,
            input_variables=["user_text", "timestamp"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        print("Structured output configured")

        llm = OllamaLLM(model="mistral:latest")

        print("LLM initialized successfully")

        chain = prompt | llm | parser

        try:
            response = chain.invoke({"user_text": user_text, "timestamp": timestamp})
            print(f"Raw response received: {response}")


        except Exception as e:
            print(f"Error during model invocation: {str(e)}")
            print(f"Exception type: {type(e)}")
            raise

        try:
            event = create_ics_event(response.properties)

            # Create a calendar and add the event
            calendar = Calendar()
            calendar.events.add(event)

            with tempfile.NamedTemporaryFile(suffix=".ics", delete=False) as tmp:
                tmp.writelines(calendar)
                tmp.flush()
                tmp_path = tmp.name
                print(f"Temporary file created at: {tmp_path}")

            # Display the file save popup
            popup = FileSavePopup(file_content=event)
            popup.open()
        except Exception as e:
            print(f"Error during event object construction: {str(e)}")
            print(f"Exception type: {type(e)}")
            raise

    except Exception as e:
        print(f"Error during setup: {str(e)}")
        print(f"Exception type: {type(e)}")
        return None


def ollama_server_check():
    import requests
    try:
        requests.get('http://localhost:11434')
    except requests.exceptions.ConnectionError:
        print("Error: Ollama server is not running. Please start it first.")
        return None
