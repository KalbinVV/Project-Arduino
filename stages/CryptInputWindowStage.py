from stages.CryptWindowStage import CryptWindowStage
from stages.InputWindowStage import InputWindowStage


class CryptInputWindowStage(InputWindowStage):
    def get_input_title(self) -> str:
        return 'Зашифровать'

    def input_check(self, text: str) -> bool:
        return True

    def to_next_stage(self) -> None:
        crypt_window_stage = CryptWindowStage()

        crypt_window_stage.init()
