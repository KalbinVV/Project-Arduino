import tkinter as tk
from abc import abstractmethod

from stages.Stage import Stage


class InputWindowStage(Stage):
    def get_title(self) -> str:
        return 'Окно ввода ключа'

    def get_geometry(self) -> str:
        return '331x486'

    @abstractmethod
    def get_input_title(self) -> str:
        ...

    def run(self, window: tk.Tk) -> None:
        canvas = tk.Canvas(
            window,
            bg="#FFFFFF",
            height=486,
            width=331,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            326.0,
            490.0,
            fill="#F4ECEC",
            outline="")

        canvas.create_text(
            93.0,
            72.0,
            anchor="nw",
            text=self.get_input_title(),
            fill="#000000",
            font="Monospace 16"
        )

        canvas.create_text(
            53.0,
            160.0,
            anchor="nw",
            text="Введите ключ:",
            fill="#000000",
            font="Monospace 16"
        )

        key_entry = tk.Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        key_entry.place(
            x=53.0,
            y=205.0,
            width=227.0,
            height=31.0
        )

        canvas.create_text(
            35.0,
            420.0,
            anchor="nw",
            text="Бесплатно & Безопасно\n2023",
            fill="#000000",
            font="Monospace 16",
            justify="center"
        )

        canvas.create_text(
            85.0,
            11.0,
            anchor="nw",
            text="Название",
            fill="#000000",
            font="Monospace 24"
        )

        next_stage_button = tk.Button(
            text='Подтвердить',
            font="Monospace 16 bold",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_next_stage(window, key_entry),
            relief="flat"
        )
        next_stage_button.place(
            x=52.0,
            y=272.0,
            width=228.0,
            height=50.0
        )

    def on_next_stage(self, window: tk.Tk, entry: tk.Entry):
        if self.input_check(entry.get()):
            window.destroy()

            self.to_next_stage()
        else:
            pass  # TODO: Добавить окно ошибки

    @abstractmethod
    def input_check(self, text: str) -> bool: # Функция проверки корректности ключа перед переходом
        ...

    @abstractmethod
    def to_next_stage(self) -> None:  # Функция, которая вызывается, если данные корректны
        pass
