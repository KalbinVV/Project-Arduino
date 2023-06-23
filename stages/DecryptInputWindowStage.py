import hashlib
from tkinter import messagebox

from SerialWriter import SerialWriterSingleton
from stages.CryptWindowStage import CryptWindowStage
from stages.DecryptWindowStage import DecryptWindowStage
from stages.InputWindowStage import InputWindowStage


class DecryptInputWindowStage(InputWindowStage):
    def __init__(self):
        serial_writer = SerialWriterSingleton.init()

        self.__hash_value = serial_writer.get_hash()

    def get_input_title(self) -> str:
        return 'Расшифровать'

    def input_check(self, text: str) -> bool:
        text = hashlib.md5(text.encode('ascii')).hexdigest()

        if text == self.__hash_value:
            return True
        else:
            messagebox.showerror(title='Неверный ключ!',
                                 message='Введите правильный ключ!')
            return False

    def to_next_stage(self, text: str) -> None:
        decrypt_window_stage = DecryptWindowStage()

        decrypt_window_stage.init()
