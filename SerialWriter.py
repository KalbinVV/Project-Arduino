from time import sleep
from typing import Optional

import serial
from serial import SerialException

from Utils import get_serial_ports


class SerialWriter:
    def __init__(self):
        ports = get_serial_ports()

        if len(ports) == 0:
            raise SerialException('Can\'t find arduino!')

        print(ports[0])

        self.arduino = serial.Serial(ports[0], baudrate=9600, timeout=1)

    def readline(self) -> str:
        while True:
            line = self.arduino.readline()

            print(line)

            if line != b'0\r\n' and line != b'':
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

    def get_keys(self) -> list[tuple[int, int]]:
        self.arduino.write('get_keys'.encode())

        n = int(self.readline())

        print(f'N: {n}')

        e = int(self.readline())

        print(f'E: {e}')

        d = int(self.readline())

        print(f'D: {d}')

        open_key = e, n
        close_key = d, n

        return [open_key, close_key]

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
