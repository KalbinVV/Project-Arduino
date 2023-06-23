import os.path
from math import isqrt

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


def rsa_crypt(content, open_key: tuple) -> str:
    e, n = open_key

    return ' '.join(map(str, [mod_pow(byte, e, n) for byte in content]))


def rsa_decrypt(content, close_key: tuple) -> bytes:
    d, n = close_key

    return bytes([mod_pow(byte, d, n) for byte in content])


def crypt_file(open_key: tuple[int, int], directory_path: str, file_path: str) -> None:
    content = get_file_content(file_path)

    crypted_content = rsa_crypt(content, open_key)

    file_name = os.path.basename(file_path)

    crypted_file_name = f'{file_name}.crypted'

    crypted_file_path = os.path.join(directory_path, crypted_file_name)

    with open(crypted_file_path, 'w') as f:
        f.write(crypted_content)

    print(f'File crypted as {crypted_file_name}')


def decrypt_file(close_key: tuple, directory_path: str, file_path: str) -> None:
    content = get_file_content(file_path)

    file_name = os.path.basename(file_path)

    decrypted_content = rsa_decrypt(map(int, content.split()), close_key)

    decrypted_file_name = f'{file_name}.decrypted'

    decrypted_file_path = os.path.join(directory_path, decrypted_file_name)

    with open(decrypted_file_path, 'wb') as file:
        file.write(decrypted_content)

    print(f'File decrypted as {decrypted_file_name}')
