from SerialWriter import SerialWriterSingleton
from stages.CryptWindowStage import CryptWindowStage
from stages.InputWindowStage import InputWindowStage

import hashlib


class CryptInputWindowStage(InputWindowStage):
    def get_input_title(self) -> str:
        return 'Зашифровать'

    def input_check(self, text: str) -> bool:
        return True

    def to_next_stage(self, text: str) -> None:
        key_hash = hashlib.md5(text.encode()).hexdigest()

        serial_writer = SerialWriterSingleton.init()

        serial_writer.set_hash(key_hash)

        crypt_window_stage = CryptWindowStage(text)

        crypt_window_stage.init()
