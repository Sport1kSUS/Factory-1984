import os

from kivy.config import Config

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "1024")
Config.set("graphics", "height", "640")

from app.ui.start_screen import StartScreen
from kivy.core.text import LabelBase
from kivy.app import App

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = "/assets/font/DejaVuSansMono.ttf"


class FactoryApp(App):
    def build(self):
        LabelBase.register(name="DejaVu", fn_regular=f"{ROOT_PATH}{FONT_PATH}")

        return StartScreen()
