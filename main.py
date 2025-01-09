from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

from parser import generate_event_from_text_input


class MyApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # TextInput for user input
        self.text_input = TextInput(
            hint_text="Enter some text here",
            size_hint=(1, 0.2),
            multiline=False
        )
        layout.add_widget(self.text_input)

        # Button
        button = Button(
            text="Submit",
            size_hint=(1, 0.2)
        )
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)

        # Label to display the result
        self.result_label = Label(size_hint=(1, 0.6))
        layout.add_widget(self.result_label)

        return layout

    def on_button_press(self, instance):
        # Get text from the input and display it in the label
        user_input = self.text_input.text
        response = generate_event_from_text_input(user_input)
        self.result_label.text = f"LLM response: {response}"


if __name__ == "__main__":
    MyApp().run()
