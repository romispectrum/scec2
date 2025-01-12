import os

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class FileSavePopupWithName(Popup):
    def __init__(self, file_content, **kwargs):
        super().__init__(**kwargs)
        self.title = "Save File"
        self.file_content = file_content  # This is a string representing the .ics content

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # TextInput for filename entry
        self.filename_input = TextInput(
            hint_text="Enter file name (e.g., event.ics)",
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.filename_input)

        # Buttons layout (horizontal)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)

        # "Show Content" button
        show_content_button = Button(
            text="Show Content",
            size_hint=(0.5, 1)
        )
        show_content_button.bind(on_press=self.show_file_content)
        buttons_layout.add_widget(show_content_button)

        # "Save" button
        save_button = Button(
            text="Save",
            size_hint=(0.5, 1)
        )
        save_button.bind(on_press=self.save_file)
        buttons_layout.add_widget(save_button)

        layout.add_widget(buttons_layout)

        self.content = layout
        self.size_hint = (0.8, 0.4)

    def show_file_content(self, instance):
        """Show the file content in a popup with scroll if it's long."""
        content_layout = BoxLayout(orientation='vertical')
        scroll_view = ScrollView(size_hint=(1, 1))
        label = Label(text=self.file_content, size_hint_y=None)
        label.bind(texture_size=label.setter('size'))
        scroll_view.add_widget(label)
        content_layout.add_widget(scroll_view)

        content_popup = Popup(
            title="File Content",
            content=content_layout,
            size_hint=(0.9, 0.9)
        )
        content_popup.open()

    def show_error_message(self, message):
        popup = Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.5, 0.3)
        )
        popup.open()

    def show_success_message(self, message):
        popup = Popup(
            title="Success",
            content=Label(text=message),
            size_hint=(0.5, 0.3)
        )
        popup.open()

    def save_file(self, instance):
        file_name = self.filename_input.text.strip()

        if not file_name:
            self.show_error_message("No file name provided. Please enter a file name.")
            return

        # Ensure the filename has .ics extension
        if not file_name.endswith(".ics"):
            file_name += ".ics"

        # Resolve path to the user's Downloads folder
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        full_path = os.path.join(downloads_folder, file_name)

        # Attempt to write the file
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(self.file_content)
            self.show_success_message(f"File saved successfully at:\n{full_path}")
            self.dismiss()
        except Exception as e:
            self.show_error_message(f"Error saving file:\n{e}")


# Main application view
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MainView(BoxLayout):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Text input
        self.text_input = TextInput(
            hint_text="Enter event details",
            size_hint=(1, 0.2),
            multiline=False
        )
        self.add_widget(self.text_input)

        # Submit button
        submit_button = Button(text="Generate Event", size_hint=(1, 0.2))
        submit_button.bind(on_press=self.on_submit)
        self.add_widget(submit_button)

        # Result label
        self.result_label = Label(size_hint=(1, 0.6))
        self.add_widget(self.result_label)

    def show_message(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

    def on_submit(self, instance):
        user_input = self.text_input.text.strip()

        if not user_input:
            self.show_message("Error", "Input is empty. Please enter event details.")
            return

        try:
            # Grab the ICS string from the controller
            ics_content = self.controller.handle_user_input(user_input)

            if ics_content:
                # If we have valid content, open the save popup
                popup = FileSavePopupWithName(file_content=ics_content)
                popup.open()
            else:
                self.show_message("Error", "No event data generated.")
        except Exception as e:
            self.show_message("Error", f"An error occurred: {e}")
