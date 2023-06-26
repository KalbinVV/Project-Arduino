import os
import threading
import tkinter as tk
from time import sleep
from tkinter import filedialog, messagebox
from typing import Optional

from Crypt import rsa_decrypt_file
from SerialWriter import SerialWriterSingleton
from stages.Stage import Stage


class DecryptWindowStage(Stage):
    def __init__(self):
        self.text_box: Optional[tk.Text] = None

    def get_title(self) -> str:
        return 'Расшифрование'

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
            text="Расшифрование в процессе...",
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

        decrypt_thread = threading.Thread(target=self.decrypt_thread)
        decrypt_thread.start()

    def decrypt_thread(self):
        serial_writer = SerialWriterSingleton.init()

        self.text_box.insert('end', '[INFO] Получение закрытого ключа...\n')

        close_key_str = serial_writer.get_key()

        self.text_box.insert('end', '[INFO] Закрытый ключ получен!\n')

        self.text_box.insert('end', '[INFO] Расшифровка закрытого ключа...\n')

        close_key_tuple = tuple(map(int, close_key_str.split()))

        self.text_box.insert('end', '[INFO] Закрытый ключ расшифрован!\n')

        folder_selected = filedialog.askdirectory()

        if isinstance(folder_selected, tuple):  # Если пользователь не выбрал директорию
            messagebox.showerror(title='Директория не была выбрана!',
                                 message='Процесс шифрования прекращен!')

            return

        self.text_box.insert('end', f'[INFO] Выбрана директория: {folder_selected}\n')

        self.decrypt_folder(close_key_tuple, folder_selected)

        self.text_box.insert('end', f'[INFO] Процесс расшифрования закончен, вы можете закрыть это окно!')

        messagebox.showinfo(title='Процесс закончен!',
                            message='Расшифрование закончено, вы можете закрыть окно и извлечь ключ!')

    def decrypt_file(self, close_key: tuple, folder_selected: str, file_path: str) -> None:
        self.text_box.insert('end', f'[INFO] Расшифрование файла {file_path}...\n')

        rsa_decrypt_file(close_key, folder_selected, file_path)
        self.text_box.insert('end', f'[INFO] Файл расшифрован: {file_path}!\n')

        os.remove(file_path)

        self.text_box.insert('end', f'[INFO] Исходный файл удален: {file_path}\n')

    def decrypt_folder(self, close_key: tuple, folder_path: str) -> None:
        for f_path in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f_path)

            if os.path.isfile(file_path):
                self.decrypt_file(close_key, folder_path, file_path)
            else:
                self.decrypt_folder(close_key, file_path)
