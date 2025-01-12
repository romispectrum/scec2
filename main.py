from kivy.app import App
from controller import EventController
from view import MainView


class MyApp(App):
    def build(self):
        # Initialize the controller first, passing a reference to the view
        view = MainView(controller=None)  # Temporary None to avoid circular dependency
        controller = EventController(view=view)

        # Now that the controller is initialized, update the view's controller reference
        view.controller = controller

        return view


if __name__ == "__main__":
    MyApp().run()
