import tkinter as tk
from abc import abstractmethod
from typing import Optional

from stages.Stage import Stage


class InputWindowStage(Stage):
    def __init__(self):
        self.__input_text_box: Optional[tk.Entry] = None

    def get_title(self) -> str:
        return 'Окно ввода ключа'

    def get_geometry(self) -> str:
        return '400x300'

    @abstractmethod
    def get_input_title(self) -> str:
        ...

    def run(self, window: tk.Tk) -> None:
        title_label = tk.Label(window, text="CryptShield",
                               font='Monospace 28 bold',
                               background='white')
        title_label.place(relx=0.5, rely=0.1, anchor='center')

        university_label = tk.Label(window, text="Orenburg 2023",
                                    font='Monospace 16 bold',
                                    background='white')
        university_label.place(relx=0.46, rely=0.25, anchor='nw')

        self.__input_text_box = tk.Entry(window, font='Monospace 16 bold',
                                         background='white', borderwidth=2)
        self.__input_text_box.insert('end', 'example-key')

        self.__input_text_box.place(relx=0.5, rely=0.5, anchor='center', width=400, height=40)

        next_step_button = tk.Button(window, text='Продолжить',
                                     font='Monospace 16 bold',
                                     background='white',
                                     activebackground='black',
                                     activeforeground='white',
                                     command=lambda: self.on_next_stage(window))
        next_step_button.place(relx=0.5, rely=0.7, anchor='center', width=400, height=70)

        return_button = tk.Button(window, text='Назад',
                                  font='Monospace 16 bold',
                                  background='white',
                                  activebackground='black',
                                  activeforeground='white',
                                  command=lambda: self.on_return_button(window))
        return_button.place(relx=0.5, rely=0.9, anchor='center', width=400, height=60)

    @classmethod
    def on_return_button(cls, window: tk.Tk):
        window.destroy()

        from stages.MainWindowStage import MainWindowStage
        main_window_stage = MainWindowStage()
        main_window_stage.init()

    def on_next_stage(self, window: tk.Tk):
        text = self.__input_text_box.get()

        if self.input_check(text):
            window.destroy()

            self.to_next_stage(text)
        else:
            pass  # TODO: Добавить окно ошибки

    @abstractmethod
    def input_check(self, text: str) -> bool: # Функция проверки корректности ключа перед переходом
        ...

    @abstractmethod
    def to_next_stage(self, text: str) -> None:  # Функция, которая вызывается, если данные корректны
        pass
