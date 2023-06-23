import tkinter as tk
from time import sleep
from typing import Optional

from SerialWriter import SerialWriterSingleton
from stages.Stage import Stage


class KeyTestWindowStage(Stage):
    def __init__(self):
        self.text_box: Optional[tk.Text] = None

    def get_title(self) -> str:
        return 'Тест ключа'

    def get_geometry(self) -> str:
        return '822x483'

    def run(self, window: tk.Tk) -> None:
        canvas = tk.Canvas(
            window,
            bg="#FFFFFF",
            height=483,
            width=822,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            822.0,
            490.0,
            fill="#F4ECEC",
            outline="")

        canvas.create_text(
            390.0,
            417.0,
            anchor="nw",
            text="OSU\n2023",
            fill="#000000",
            font="Monospace 16 bold",
            justify="center"
        )

        canvas.create_text(
            40.0,
            12.0,
            anchor="nw",
            text="CryptShield",
            fill="#000000",
            font="Monospace 16 bold"
        )

        canvas.create_text(
            350.0,
            77.0,
            anchor="nw",
            text="Тест ключа:",
            fill="#000000",
            font="Monospace 16 bold"
        )
        self.text_box = tk.Text(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font="Monospace 16 bold"
        )
        self.text_box.place(
            x=0.0,
            y=155.0,
            width=822.0,
            height=245.0
        )

    def before_loop(self) -> None:
        serial_writer = SerialWriterSingleton.init()

        seconds = serial_writer.get_seconds()
        generated_keys = serial_writer.generate_keys()
        hash_value = serial_writer.get_hash()

        self.text_box.insert('end', f'Хэш: {hash_value}\n')
        self.text_box.insert('end', f'Время на внутренних часах: {seconds}\n')
        self.text_box.insert('end', f'Тест генерации ключей: {generated_keys}\n')
        self.text_box.insert('end', f'Если все поля выводятся корректно, то ключ функционирует исправно!')

        self.text_box.configure(state='disabled')
