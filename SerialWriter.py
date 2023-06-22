from time import sleep
from typing import Optional

import serial


class SerialWriter:
    def __init__(self):
        self.arduino = serial.Serial('COM4', 9800, timeout=1)

    def readline(self) -> str:
        line = self.arduino.readline()

        if len(line) == 0:
            return self.readline()
        else:
            return line.decode()

    def set_hash(self, hash_str: str) -> None:
        hash_status = self.write_and_receive('set_hash')

        print(hash_status)

        received_hash = self.write_and_receive(hash_str)

        print(f'Arduino received and save hash: {received_hash}')

    def get_hash(self) -> Optional[str]:
        hash_value = self.write_and_receive('get_hash')

        if hash_value == "Not":
            return None

        return hash_value

    def get_seconds(self) -> int:
        seconds = int(self.write_and_receive('get_seconds'))

        return seconds

    def write_and_receive(self, value: str) -> str:
        print(f'Value sent to arduino: {value}')

        self.arduino.write(value.encode())

        value_from_arduino = self.readline()

        print(f'From arduino: {value_from_arduino}')

        self.arduino.flush()

        return value_from_arduino




class SerialWriterSingleton:
    _instance: SerialWriter = None

    @classmethod
    def init(cls):
        if cls._instance is None:
            cls._instance = SerialWriter()

        return cls._instance
