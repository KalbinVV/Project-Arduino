import tkinter as tk

from stages.Stage import Stage


class InitKeyWindowStage(Stage):
    def __init__(self):
        self.text_box = None

    def get_title(self) -> str:
        return 'Создание ключа'

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
            260.0,
            77.0,
            anchor="nw",
            text="Создание ключа в процессе...",
            fill="#000000",
            font="Monospace 16 bold"
        )
        self.text_box = tk.Text(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font="Monospace 8 bold"
        )
        self.text_box.place(
            x=0.0,
            y=155.0,
            width=822.0,
            height=245.0
        )
