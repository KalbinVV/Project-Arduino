import logging
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from Crypt import rsa_crypt_file, check_rsa_keys_correctness
from SerialWriter import SerialWriterSingleton
from Utils import Keys
from stages.Stage import Stage


class CryptWindowStage(Stage):
    def __init__(self, password: str):
        self.text_box = None
        self.password = password

    def get_title(self) -> str:
        return 'Шифрование'

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
            text="Шифрование в процессе...",
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

        self.text_box.insert('end', '[INFO] Хэш пароля сохранен!\n')

        crypt_thread = threading.Thread(target=self.crypt_function)
        crypt_thread.start()

    def crypt_function(self):
        serial_writer = SerialWriterSingleton.init()

        self.text_box.insert('end', f'[INFO] Пароль получен!\n')

        keys: Keys = serial_writer.generate_keys()

        self.text_box.insert('end', f'[INFO] Валидация ключа...\n')

        while not check_rsa_keys_correctness(keys):
            self.text_box.insert('end', f'[INFO] Ключи не прошли валидацию, повторная попытка!\n')

            keys = serial_writer.generate_keys()

        self.text_box.insert('end', f'[INFO] Ключи шифрования сгенерированы!\n')

        close_key_str = f'{keys.close_key[0]} {keys.close_key[1]}'

        logging.debug(f'Close key str: {close_key_str}')
        serial_writer.set_key(close_key_str)

        self.text_box.insert('end', f'[INFO] Закрытый ключ сохранен!\n')

        folder_selected = filedialog.askdirectory()

        if isinstance(folder_selected, tuple):  # Если пользователь не выбрал директорию
            messagebox.showerror(title='Директория не была выбрана!',
                                 message='Процесс шифрования прекращен!')

            return

        self.text_box.insert('end', f'[INFO] Выбрана директория: {folder_selected}\n')

        self.crypt_folder(keys.open_key, folder_selected)

        self.text_box.insert('end', f'[INFO] Процесс шифрования закончен, вы можете закрыть это окно!')

        messagebox.showinfo(title='Процесс закончен!',
                            message='Шифрование закончено, вы можете закрыть окно и извлечь ключ!')

    def crypt_file(self, open_key: tuple[int, int], folder_selected: str, file_path: str) -> None:
        self.text_box.insert('end', f'[INFO] Шифрование файла {file_path}...\n')

        rsa_crypt_file(open_key, folder_selected, file_path)
        self.text_box.insert('end', f'[INFO] Файл зашифрован: {file_path}!\n')

        os.remove(file_path)

        self.text_box.insert('end', f'[INFO] Исходный файл удален: {file_path}\n')

    def crypt_folder(self, open_key: tuple[int, int], folder_path: str) -> None:
        for f_path in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f_path)

            if os.path.isfile(file_path):
                self.crypt_file(open_key, folder_path, file_path)
            else:
                self.crypt_folder(open_key, file_path)





