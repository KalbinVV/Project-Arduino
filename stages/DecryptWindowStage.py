import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from Crypt import rsa_decrypt_file
from SerialWriter import SerialWriterSingleton
from Utils import load_image, is_file_crypted, get_amount_of_crypted_files_in_folder
from stages.Stage import Stage


class DecryptWindowStage(Stage):
    def __init__(self):
        self.text_box: Optional[tk.Text] = None
        self.text_box: Optional[tk.Text] = None
        self.progressbar: Optional[ttk.Progressbar] = None
        self.current_status_label: Optional[tk.Label] = None
        self.progressbar_value = 0
        self.amount_of_files = 0
        self.file_crypted_amount = 0
        self.progress_bar_value_label: Optional[tk.Label] = None

    def get_title(self) -> str:
        return 'Расшифрование'

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

        decrypt_thread = threading.Thread(target=self.decrypt_thread)
        decrypt_thread.start()

    def decrypt_thread(self):
        serial_writer = SerialWriterSingleton.init()

        self.current_status_label.configure(text='Получение закрытого ключа...')

        self.text_box.insert('1.0', '[INFO] Получение закрытого ключа...\n')

        close_key_str = serial_writer.get_key()

        self.text_box.insert('1.0', '[INFO] Закрытый ключ получен!\n')

        self.current_status_label.configure(text='Расшифровка закрытого ключа...')

        self.text_box.insert('1.0', '[INFO] Расшифровка закрытого ключа...\n')

        close_key_tuple = tuple(map(int, close_key_str.split()))

        self.text_box.insert('1.0', '[INFO] Закрытый ключ расшифрован!\n')

        folder_selected = filedialog.askdirectory()

        if isinstance(folder_selected, tuple):  # Если пользователь не выбрал директорию
            self.current_status_label.configure(text='Процесс расшифрования прекращен!')

            messagebox.showerror(title='Директория не была выбрана!',
                                 message='Процесс шифрования прекращен!')

            return

        self.amount_of_files = get_amount_of_crypted_files_in_folder(folder_selected)

        self.text_box.insert('1.0', f'[INFO] Выбрана директория: {folder_selected}\n')

        self.decrypt_folder(close_key_tuple, folder_selected)

        self.text_box.insert('1.0', f'[INFO] Процесс расшифрования закончен, вы можете закрыть это окно!')

        self.current_status_label.configure(text='Процесс расшифрования закончен!')

        messagebox.showinfo(title='Процесс закончен!',
                            message='Расшифрование закончено, вы можете закрыть окно и извлечь ключ!')

    def decrypt_file(self, close_key: tuple, folder_selected: str, file_path: str) -> None:
        self.current_status_label.configure(text=f'Расшифрование файла: {os.path.basename(file_path)}')

        self.text_box.insert('1.0', f'[INFO] Расшифрование файла {file_path}...\n')

        rsa_decrypt_file(close_key, folder_selected, file_path)
        self.text_box.insert('1.0', f'[INFO] Файл расшифрован: {file_path}!\n')

        os.remove(file_path)

        self.text_box.insert('1.0', f'[INFO] Исходный файл удален: {file_path}\n')

        self.file_crypted_amount += 1

        self.progressbar_value = (self.file_crypted_amount * 100) // self.amount_of_files
        self.progressbar.configure(value=self.progressbar_value)
        self.progress_bar_value_label.configure(text=f'{self.progressbar_value}%')

        if self.progressbar_value >= 50:
            self.progress_bar_value_label.configure(background='black')

    def decrypt_folder(self, close_key: tuple, folder_path: str) -> None:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if os.path.isfile(file_path):
                if is_file_crypted(file_name):
                    self.decrypt_file(close_key, folder_path, file_path)
                else:
                    self.text_box.insert('1.0', f'[INFO] Файл не зашифрован, пропускаем: {file_path}\n')
            else:
                self.decrypt_folder(close_key, file_path)
