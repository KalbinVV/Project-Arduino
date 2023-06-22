import glob
import sys
from pathlib import Path

import serial

ASSETS_PATH = Path(r"assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
