import logging
import os.path
from functools import cache
from math import isqrt, gcd


def phi(n: int) -> int:
    result = n

    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            while n % i == 0:
                n //= i

            result -= result // i

    if n > 1:
        result -= result // n

    return result


@cache
def mod_pow(number: int, power: int, modulo: int):
    result = 1

    while power > 1:
        if power & 1:
            result = (result * number) % modulo

        number = number ** 2 % modulo
        power >>= 1

    return (number * result) % modulo


def get_file_content(file_name: str) -> str | bytes:
    content = None

    with open(file_name, 'rb') as file:
        content = file.read()

    return content


def rsa_decrypt(content, close_key: tuple) -> bytes:
    d, n = close_key

    return bytes([mod_pow(byte, d, n) for byte in content])


def rsa_crypt_file(open_key: tuple[int, int], directory_path: str, file_path: str) -> None:
    file_name = os.path.basename(file_path)

    crypted_file_name = f'{file_name}.crypted'

    crypted_file_path = os.path.join(directory_path, crypted_file_name)

    e, n = open_key

    with open(file_path, 'rb') as source_file:
        with open(crypted_file_path, 'w') as dst_file:
            byte = source_file.read(1)
            while byte:
                int_value = int.from_bytes(byte, byteorder='big')

                dst_file.write(f'{mod_pow(int_value, e, n)} ')

                byte = source_file.read(1)

    logging.info(f'File crypted as {crypted_file_name}')


def rsa_decrypt_file(close_key: tuple, directory_path: str, file_path: str) -> None:
    file_name = os.path.basename(file_path)

    decrypted_file_name = file_name[0:file_name.rfind('.crypted')]

    decrypted_file_path = os.path.join(directory_path, decrypted_file_name)

    d, n = close_key

    with open(file_path, 'r') as source_file:
        with open(decrypted_file_path, 'wb') as dst_file:
            byte = source_file.read(1)

            while byte:
                value = byte

                while True:
                    byte = source_file.read(1)

                    if not byte or byte == ' ':
                        break

                    value += byte

                int_value = int(value)

                decrypted_byte = bytes([mod_pow(int_value, d, n)])

                dst_file.write(decrypted_byte)

                byte = source_file.read(1)

    logging.info(f'File decrypted as {decrypted_file_name}')


def is_prime(n: int) -> bool:
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            return False

    return True


def get_multiplicative_inverse(number: int, modulo: int) -> int:
    return mod_pow(number, phi(modulo) - 1, modulo)


def rsa_get_open_key(euler: int) -> int:
    a = 0
    b = 0

    for i in range(2, euler):
        if is_prime(i):
            if gcd(i, euler) == 1:
                return i

    return 0


def rsa_get_close_key(p: int, q: int, e: int) -> int:
    return get_multiplicative_inverse(e, phi(p * q))
