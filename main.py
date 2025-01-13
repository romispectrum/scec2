from kivy.app import App

from controller import EventController
from view import MainView


class ScecApp(App):
    def build(self):
        view = MainView(controller=None)
        controller = EventController(view=view)
        view.controller = controller
        return view


if __name__ == "__main__":
    ScecApp().run()
