import serial

from SerialWriter import SerialWriterSingleton
from stages.StartWindowStage import StartWindowStage


def main() -> None:
    serial_writer = SerialWriterSingleton.init()

    while True:
        input_char = input('Enter: ')

        if input_char == 's':
            hash_str = input('Enter hash:')

            serial_writer.set_hash(hash_str)
        elif input_char == 'g':
            print(f'Hash: {serial_writer.get_hash()}')
        elif input_char == 't':
            print(f'Time: {serial_writer.get_seconds()}')
        else:
            serial_writer.write_and_receive(input_char)

    start_window_stage = StartWindowStage()

    start_window_stage.init()


if __name__ == '__main__':
    main()
