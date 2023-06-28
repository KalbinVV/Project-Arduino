import tkinter as tk
from Utils import relative_to_assets, load_image
from stages.CryptInputWindowStage import CryptInputWindowStage
from stages.DecryptInputWindowStage import DecryptInputWindowStage
from stages.KeyTestWindowStage import KeyTestWindowStage
from stages.Stage import Stage


class MainWindowStage(Stage):
    def __init__(self):
        self.create_key_icon = None
        self.crypt_icon = None
        self.decrypt_icon = None

    def get_title(self) -> str:
        return 'Главное окно'

    def get_geometry(self) -> str:
        return '600x400'

    def run(self, window: tk.Tk) -> None:
        title_label = tk.Label(window, text="CryptShield", font='Monospace 28 bold',
                               background='#000036', fg='white')
        title_label.place(relx=0.5, rely=0.1, anchor='center')

        crypt_button_image = load_image('crypt_button.png', (600, 100))

        crypt_button = tk.Button(window, image=crypt_button_image,
                                 command=lambda: self.on_crypt(window),
                                 background='#000036', activebackground='black')
        crypt_button.image = crypt_button_image

        crypt_button.place(x=0, rely=0.25, width=600, height=100)

        decrypt_button_image = load_image('decrypt_button.png', (600, 100))

        decrypt_button = tk.Button(window, image=decrypt_button_image,
                                   command=lambda: self.on_decrypt(window),
                                   background='#000036', activebackground='black')
        decrypt_button.image = decrypt_button_image

        decrypt_button.place(x=0, rely=0.55, width=600, height=100)

        university_title = tk.Button(window, text='Orenburg 2023',
                                     font='Monospace 18 bold', background='#000036',
                                     fg='white',
                                     command=lambda: self.on_key_test(window))
        university_title.place(relx=0.5, rely=0.9, anchor='center')

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
    def on_key_test(cls, window: tk.Tk) -> None:
        window.destroy()

        key_test_stage = KeyTestWindowStage()
        key_test_stage.init()
