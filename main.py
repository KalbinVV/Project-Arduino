from time import sleep

from SerialWriter import SerialWriterSingleton
from stages.StartWindowStage import StartWindowStage


def main() -> None:
    start_window_stage = StartWindowStage()

    start_window_stage.init()


if __name__ == '__main__':
    main()
