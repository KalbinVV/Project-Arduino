import logging
import os
import threading
import tkinter as tk
from time import sleep
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from Crypt import rsa_crypt_file, check_rsa_keys_correctness
from SerialWriter import SerialWriterSingleton
from Utils import Keys, load_image, get_amount_of_files_in_folder
from stages.Stage import Stage


class CryptWindowStage(Stage):
    def __init__(self, password: str):
        self.text_box: Optional[tk.Text] = None
        self.password = password
        self.progressbar: Optional[ttk.Progressbar] = None
        self.current_status_label: Optional[tk.Label] = None
        self.progressbar_value = 0
        self.amount_of_files = 0
        self.file_crypted_amount = 0
        self.progress_bar_value_label: Optional[tk.Label] = None

    def get_title(self) -> str:
        return 'Шифрование'

    def get_geometry(self) -> str:
        return '800x400'

    def run(self, window: tk.Tk) -> None:
        background_label = tk.Label(window, background='#000036')
        background_label.place(relx=0.5, rely=0, anchor='center', width=800, relheight=0.6)

        title_label = tk.Label(window, text="CryptShield", font='Monospace 18 bold',
                               background='#000036',
                               foreground='white')

        logo_image = load_image('white-shield.png', (32, 32))

        logo_image_label = tk.Label(window, image=logo_image, background='#000036')
        logo_image_label.image = logo_image

        title_label.place(relx=0.5, rely=0.1, anchor='center', relheight=0.1)
        logo_image_label.place(relx=0.65, rely=0.1, anchor='center', relheight=0.1)

        self.current_status_label = tk.Label(window, background='#000036', font='Monospace 12 bold',
                                             text='Генерация ключа...',
                                             foreground='white')
        self.current_status_label.place(relx=0.5, rely=0.2, anchor='center', relheight=0.1)

        style = ttk.Style()

        style.configure("blue.Horizontal.TProgressbar", foreground='#000036', background='black',
                        troughcolor='#000036')

        self.progressbar_value = 0

        self.progressbar = ttk.Progressbar(window, orient="horizontal", length=100,
                                           maximum=100,
                                           style="blue.Horizontal.TProgressbar",
                                           mode="determinate")
        self.progressbar.place(relx=0.5, rely=0.3, anchor='center', relheight=0.1, relwidth=1)

        self.progress_bar_value_label = tk.Label(window, text='0%',
                                                 font='Monospace 8 bold',
                                                 background='#000036',
                                                 foreground='white')
        self.progress_bar_value_label.place(relx=0.5, rely=0.3, anchor='center')

        self.text_box = tk.Text(window, font='Monospace 8 bold', background='white')
        self.text_box.place(relx=0.5, rely=0.68, anchor='center', relheight=0.65, relwidth=1)

        self.text_box.insert('end', '[INFO] Хэш пароля сохранен!\n')

        crypt_thread = threading.Thread(target=self.crypt_function)
        crypt_thread.start()

    def crypt_function(self):
        serial_writer = SerialWriterSingleton.init()

        self.text_box.insert('end', f'[INFO] Пароль получен!\n')

        keys: Keys = serial_writer.generate_keys()

        self.current_status_label.configure(text='Валидация ключа...')

        self.text_box.insert('end', f'[INFO] Валидация ключа...\n')

        while not check_rsa_keys_correctness(keys):
            self.text_box.insert('end', f'[INFO] Ключи не прошли валидацию, повторная попытка!\n')

            sleep(3)

            keys = serial_writer.generate_keys()

        self.current_status_label.configure(text='Сохранение ключа...')

        self.text_box.insert('end', f'[INFO] Ключи шифрования сгенерированы!\n')

        close_key_str = f'{keys.close_key[0]} {keys.close_key[1]}'

        logging.debug(f'Close key str: {close_key_str}')
        serial_writer.set_key(close_key_str)

        self.text_box.insert('end', f'[INFO] Закрытый ключ сохранен!\n')

        folder_selected = filedialog.askdirectory()

        if isinstance(folder_selected, tuple):  # Если пользователь не выбрал директорию
            self.current_status_label.configure(text='Шифрование прекращено!')

            messagebox.showerror(title='Директория не была выбрана!',
                                 message='Процесс шифрования прекращен!')

            return

        self.text_box.insert('end', f'[INFO] Выбрана директория: {folder_selected}\n')

        self.amount_of_files = get_amount_of_files_in_folder(folder_selected)

        self.current_status_label.configure(text='Шифрование файлов...')

        self.crypt_folder(keys.open_key, folder_selected)

        self.text_box.insert('end', f'[INFO] Процесс шифрования закончен, вы можете закрыть это окно!')

        self.current_status_label.configure(text='Шифрование закончено!')

        messagebox.showinfo(title='Процесс закончен!',
                            message='Шифрование закончено, вы можете закрыть окно и извлечь ключ!')

    def crypt_file(self, open_key: tuple[int, int], folder_selected: str, file_path: str) -> None:
        self.current_status_label.configure(text=f'Шифрование файла: {os.path.basename(file_path)}')

        self.text_box.insert('end', f'[INFO] Шифрование файла {file_path}...\n')

        rsa_crypt_file(open_key, folder_selected, file_path)
        self.text_box.insert('end', f'[INFO] Файл зашифрован: {file_path}!\n')

        os.remove(file_path)

        self.text_box.insert('end', f'[INFO] Исходный файл удален: {file_path}\n')

        self.file_crypted_amount += 1

        self.progressbar_value = (self.file_crypted_amount * 100) // self.amount_of_files
        self.progressbar.configure(value=self.progressbar_value)
        self.progress_bar_value_label.configure(text=f'{self.progressbar_value}%')

        if self.progressbar_value >= 50:
            self.progress_bar_value_label.configure(background='black')

    def crypt_folder(self, open_key: tuple[int, int], folder_path: str) -> None:
        for f_path in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f_path)

            if os.path.isfile(file_path):
                self.crypt_file(open_key, folder_path, file_path)
            else:
                self.crypt_folder(open_key, file_path)
