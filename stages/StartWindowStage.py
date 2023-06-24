import tkinter as tk
from time import sleep
from tkinter import messagebox

from SerialWriter import SerialWriterSingleton
from Utils import relative_to_assets
from stages.ErrorWindowStage import ErrorWindowStage
from stages.MainWindowStage import MainWindowStage
from stages.Stage import Stage


class StartWindowStage(Stage):
    def __init__(self):
        self.arduino_icon = None  # Говорим сборщику мусора не очищать изображение

    def get_title(self) -> str:
        return 'Стартовое окно'

    def get_geometry(self) -> str:
        return '374x486'

    def run(self, window: tk.Tk) -> None:
        canvas = tk.Canvas(
            window,
            bg="#FFFFFF",
            height=486,
            width=374,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            6.0,
            374.0,
            496.0,
            fill="#F4ECEC",
            outline="")

        self.arduino_icon = tk.PhotoImage(
            file=relative_to_assets("arduino_icon.png"))

        canvas.create_image(
            187.0,
            188.0,
            image=self.arduino_icon
        )

        canvas.create_text(
            85,
            11.0,
            anchor="nw",
            text="CryptShield",
            fill="#000000",
            font="Monospace 24"
        )

        canvas.create_text(
            50.0,
            420.0,
            anchor="nw",
            text="Бесплатно & Безопасно\n2023",
            fill="#000000",
            font="Monospace 16",
            justify='center'
        )

        connect_to_device_button = tk.Button(
            text='Подключиться к устройству',
            font='Monospace 12',
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_connect_to_device(window),
            relief="flat"
        )

        connect_to_device_button.place(
            x=50.0,
            y=298.0,
            width=290.0,
            height=34.0
        )

    @classmethod
    def on_connect_to_device(cls, window: tk.Tk) -> None:
        try:
            SerialWriterSingleton.init()
            sleep(2)

            window.destroy()

            main_window_stage = MainWindowStage()
            main_window_stage.init()
        except OSError as e:
            messagebox.showerror(title='Не удалось подключиться к ключу!',
                                 message=str(e))
