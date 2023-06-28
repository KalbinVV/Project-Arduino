import tkinter as tk
from time import sleep
from tkinter import messagebox

from SerialWriter import SerialWriterSingleton
from Utils import relative_to_assets, load_image
from stages.ErrorWindowStage import ErrorWindowStage
from stages.MainWindowStage import MainWindowStage
from stages.Stage import Stage


class StartWindowStage(Stage):
    def __init__(self):
        self.arduino_icon = None  # Говорим сборщику мусора не очищать изображение

    def get_title(self) -> str:
        return 'Стартовое окно'

    def get_geometry(self) -> str:
        return '500x300'

    def run(self, window: tk.Tk) -> None:
        title_label = tk.Label(window, text="CryptShield",
                               font='Monospace 48 bold',
                               background='white')
        title_label.place(relx=0.5, rely=0.3, anchor='center')

        university_label = tk.Label(window, text="Orenburg 2023",
                                    font='Monospace 24 bold',
                                    background='white')
        university_label.place(relx=0.46, rely=0.45, anchor='nw')

        connect_to_device_button = tk.Button(window, text='Подключиться к устройству',
                                             font='Monospace 16 bold',
                                             borderwidth=0,
                                             command=lambda: self.on_connect_to_device(window),
                                             background='white',
                                             activebackground='black',
                                             activeforeground='white')
        connect_to_device_button.place(relx=0.5, rely=0.8, anchor='center')

        usb_logo_image = load_image('usb.png', (32, 32))

        usb_logo_label = tk.Label(window, image=usb_logo_image, borderwidth=0, background='white')
        usb_logo_label.image = usb_logo_image

        usb_logo_label.place(relx=0.9, rely=0.8, anchor='center')

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
