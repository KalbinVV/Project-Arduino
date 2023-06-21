import tkinter as tk

from Utils import relative_to_assets
from stages.CryptInputWindowStage import CryptInputWindowStage
from stages.DecryptInputWindowStage import DecryptInputWindowStage
from stages.InitKeyWindowStage import InitKeyWindowStage
from stages.Stage import Stage


class MainWindowStage(Stage):
    def __init__(self):
        self.create_key_icon = None
        self.crypt_icon = None
        self.decrypt_icon = None

    def get_title(self) -> str:
        return 'Главное окно'

    def get_geometry(self) -> str:
        return '822x481'

    def run(self, window: tk.Tk) -> None:
        canvas = tk.Canvas(
            window,
            bg="#FFFFFF",
            height=481,
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
            340.0,
            8.0,
            anchor="nw",
            text="Название",
            fill="#000000",
            font="Monospace 24 bold"
        )

        canvas.create_text(
            280.0,
            424.0,
            anchor="nw",
            text="Бесплатно & Безопасно\n2023",
            fill="#000000",
            font="Monospace 16",
            justify="center"
        )

        self.crypt_icon = tk.PhotoImage(
            file=relative_to_assets("crypt_icon.png"))
        canvas.create_image(
            124.0,
            227.0,
            image=self.crypt_icon
        )

        self.decrypt_icon = tk.PhotoImage(
            file=relative_to_assets("decrypt_icon.png"))
        canvas.create_image(
            418.0,
            227.0,
            image=self.decrypt_icon
        )

        crypt_button = tk.Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_crypt(window),
            relief="flat",
            text="Зашифровать",
            font="Monospace 12 bold"
        )
        crypt_button.place(
            x=68.0,
            y=303.0,
            width=114.0,
            height=38.0
        )

        decrypt_button = tk.Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_decrypt(window),
            relief="flat",
            text="Расшифровать",
            font="Monospace 12 bold"
        )
        decrypt_button.place(
            x=339.0,
            y=303.0,
            width=152.0,
            height=44.0
        )

        create_key_button = tk.Button(
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_key_create(window),
            relief="flat",
            text="Создать ключ",
            font="Monospace 12 bold"
        )
        create_key_button.place(
            x=622.0,
            y=307.0,
            width=127.0,
            height=44.0
        )

        self.create_key_icon = tk.PhotoImage(
            file=relative_to_assets("create_key_icon.png"))
        canvas.create_image(
            685.0,
            245.0,
            image=self.create_key_icon
        )

    @classmethod
    def on_crypt(cls, window: tk.Tk) -> None:
        window.destroy()

        crypt_input_stage = CryptInputWindowStage()
        crypt_input_stage.init()

    @classmethod
    def on_decrypt(cls, window: tk.Tk) -> None:
        window.destroy()

        decrypt_input_stage = DecryptInputWindowStage()
        decrypt_input_stage.init()

    @classmethod
    def on_key_create(cls, window: tk.Tk) -> None:
        window.destroy()

        key_create_stage = InitKeyWindowStage()
        key_create_stage.init()
