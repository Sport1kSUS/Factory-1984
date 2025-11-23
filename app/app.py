from kivy.config import Config

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "640")

from app.ui.start_screen import StartScreen
from kivy.app import App


class FactoryApp(App):
    def build(self):
        return StartScreen()
