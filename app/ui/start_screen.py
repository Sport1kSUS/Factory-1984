import os

from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

ASCII_FRAME = r"""
┌─Factory1984────────────────────────────────────────────────────────────────────────┐
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                                                    │
│                                                             |\      _,,,---,,_     │
│                                                       ZZZzz /,`.-'`'    -.  ;-;;,_ │
│                                                            |,4-  ) )-,_. ,\ (  `'-'│
│                                                           '---''(_/--'  `-'\_)     │
└────────────────────────────────────────────────────────────────────────────────────┘
"""

ASCII_BUTTON = "┌──────────────┐\n│ browse files │\n└──────────────┘"


class StartScreen(BoxLayout):
    file_path = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"

        label = Label(
            text=ASCII_FRAME,
            font_size=20,
            font_name="DejaVu",
            size_hint=(1, 1),
            color=(0.8, 0.816, 0.855, 1),
            markup=True,
        )

        button = Button(
            text=ASCII_BUTTON,
            font_size=20,
            font_name="DejaVu",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0, 0, 0, 0),
            color=(0.8, 0.816, 0.855, 1),
            markup=True,
        )

        # TODO:  button.bind(on_press=self.pick_file)

        overlay_layout = FloatLayout(size_hint=(1, 1))
        overlay_layout.add_widget(label)
        overlay_layout.add_widget(button)

        self.add_widget(overlay_layout)

        Window.bind(on_dropfile=self.on_drop)

    def on_drop(self, _window, file_path: bytes) -> None:
        path = file_path.decode("utf-8")
        abs_path = os.path.abspath(path)
        self.file_path = abs_path

    # def pick_file(self, _instance) -> None:
    # TODO:
    # сделать нормальный выбор файлов, чтобы оно
    # открывало нативный файл менеджер
