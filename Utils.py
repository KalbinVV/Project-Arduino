import glob
import sys
from pathlib import Path
from tkinter import PhotoImage
from typing import NamedTuple

from PIL import ImageTk, Image

import serial


class Keys(NamedTuple):
    open_key: tuple[int, int]
    close_key: tuple[int, int]


ASSETS_PATH = Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def load_image(image_name: str, image_size: tuple[int, int]) -> PhotoImage:
    usb_logo_image = Image.open(relative_to_assets(image_name))
    usb_logo_image = usb_logo_image.resize(image_size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(usb_logo_image)


def get_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyUSB*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result