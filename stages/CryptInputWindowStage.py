from tkinter import messagebox

from SerialWriter import SerialWriterSingleton
from stages.CryptWindowStage import CryptWindowStage
from stages.InputWindowStage import InputWindowStage

import hashlib


class CryptInputWindowStage(InputWindowStage):
    def get_input_title(self) -> str:
        return 'Зашифровать'

    def input_check(self, text: str) -> bool:
        text_length = len(text)

        if text_length not in [16, 24, 32]:
            messagebox.showerror(title='Неверная длина ключа!',
                                 message='Длина ключа должна равняться 16,24, либо 32 битам!')
            return False
        else:
            return True

    def to_next_stage(self, text: str) -> None:
        key_hash = hashlib.md5(text.encode('ascii')).hexdigest()

        serial_writer = SerialWriterSingleton.init()

        serial_writer.set_hash(key_hash)

        crypt_window_stage = CryptWindowStage(text)

        crypt_window_stage.init()
