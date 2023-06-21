from stages.CryptWindowStage import CryptWindowStage
from stages.DecryptWindowStage import DecryptWindowStage
from stages.InputWindowStage import InputWindowStage


class DecryptInputWindowStage(InputWindowStage):
    def get_input_title(self) -> str:
        return 'Расшифровать'

    def input_check(self, text: str) -> bool:
        return True

    def to_next_stage(self) -> None:
        decrypt_window_stage = DecryptWindowStage()

        decrypt_window_stage.init()
