import logging
from typing import Optional

import serial
from serial import SerialException

from Crypt import rsa_get_close_key, rsa_get_open_key
from Utils import get_serial_ports, Keys


class SerialWriter:
    _hash_value: Optional[str] = None
    _key_value: Optional[str] = None

    def __init__(self):
        ports = get_serial_ports()

        if len(ports) == 0:
            raise SerialException('Не удалось обнаружить устройство!')

        logging.info(f'Port: {ports[0]}')

        self.arduino = serial.Serial(ports[0], baudrate=9600, timeout=1)

    def readline(self, is_secure_read: bool = True) -> str:
        while True:
            line = self.arduino.readline()

            logging.debug(f'[Arduino] {line}')

            if line != b'0\r\n' and line != b'':
                if is_secure_read:
                    return line[0:line.rfind(b'0')].decode('ascii')
                else:
                    return line.decode('ascii')

    def set_hash(self, hash_str: str) -> None:
        hash_status = self.write_and_receive('set_hash')

        logging.debug(f'Hash status: {hash_status}')

        received_hash = self.write_and_receive(hash_str)

        logging.debug(f'Arduino received and save hash: {received_hash}')

    def get_hash(self) -> Optional[str]:
        if self._hash_value is None:

            self._hash_value = self.write_and_receive('get_hash')

            if self._hash_value == "Not":
                return None

        return self._hash_value

    def get_seconds(self) -> int:
        seconds = int(self.write_and_receive('get_seconds'))

        return seconds

    def generate_keys(self) -> Keys:
        self.arduino.write('generate_keys'.encode('ascii'))

        p = int(self.readline())

        logging.debug(f'p: {p}')

        q = int(self.readline())

        logging.debug(f'q: {q}')

        euler = (p - 1) * (q - 1)

        e = rsa_get_open_key(euler)

        n = p * q

        d = rsa_get_close_key(p, q, e)

        open_key = e, n
        close_key = d, n

        keys = Keys(open_key, close_key)

        logging.debug(f'Generated keys: {keys}')

        return keys

    def get_key(self) -> str:
        if self._key_value is None:
            self._key_value = self.write_and_receive('get_key')

        return self._key_value

    def set_key(self, key: str) -> None:
        key_status = self.write_and_receive('set_key')

        logging.debug(f'Key status: {key_status}')

        received_key = self.write_and_receive(key, False)

        logging.debug(f'Arduino received and save key: {received_key}')

    def write_and_receive(self, value: str, is_secure_read: bool = True) -> str:
        logging.debug(f'Value sent to arduino: {value}')

        self.arduino.write(value.encode('ascii'))

        value_from_arduino = self.readline(is_secure_read)

        logging.debug(f'From arduino: {value_from_arduino}')

        self.arduino.flush()

        return value_from_arduino


class SerialWriterSingleton:
    _instance: SerialWriter = None

    @classmethod
    def init(cls):
        if cls._instance is None:
            cls._instance = SerialWriter()

        return cls._instance
