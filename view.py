from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup


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
        submit_button = Button(
            text="Generate Event",
            size_hint=(1, 0.2)
        )
        submit_button.bind(on_press=self.on_submit)
        self.add_widget(submit_button)

        # Result label
        self.result_label = Label(size_hint=(1, 0.6))
        self.add_widget(self.result_label)

    def on_submit(self, instance):
        user_input = self.text_input.text
        self.controller.handle_user_input(user_input)
