import tkinter as tk

from Utils import relative_to_assets
from stages.Stage import Stage


class ErrorWindowStage(Stage):
    def __init__(self, ex: Exception):
        print(f'Exception: {str(ex)}')

        self.error_icon = None

    def get_title(self) -> str:
        return 'Ошибка'

    def get_geometry(self) -> str:
        return '381x461'

    def run(self, window: tk.Tk) -> None:
        canvas = tk.Canvas(
            window,
            bg="#FFFFFF",
            height=470,
            width=381,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            0.0,
            0.0,
            374.0,
            490.0,
            fill="#F4ECEC",
            outline="")

        canvas.create_text(
            185,
            0,
            anchor="n",
            text="CryptShield",
            fill="#000000",
            font="Monospace 24"
        )

        canvas.create_text(
            190,
            295.0,
            anchor="n",
            text="Ошибка",
            fill="#000000",
            font="Monospace 24"
        )

        canvas.create_text(
            190,
            360.0,
            anchor="n",
            text="Бесплатно & Безопасно\n2023",
            fill="#000000",
            font="Monospace 16",
            justify='center'
        )

        self.error_icon = tk.PhotoImage(
            file=relative_to_assets("error.png"))
        canvas.create_image(
            188.0,
            163.0,
            image=self.error_icon
        )