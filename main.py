import logging

from stages.StartWindowStage import StartWindowStage


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    start_window_stage = StartWindowStage()

    start_window_stage.init()


if __name__ == '__main__':
    main()
