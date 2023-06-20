
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/qurao/dev/Макеты/build/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.title('Окно ошибки')

window.geometry("381x461")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 470,
    width = 381,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    374.0,
    490.0,
    fill="#F4ECEC",
    outline="")

canvas.create_text(
    190,
    0,
    anchor="n",
    text="Название",
    fill="#000000",
    font=("Monospace 24")
)

canvas.create_text(
    190,
    295.0,
    anchor="n",
    text="Ошибка",
    fill="#000000",
    font=("Monospace 24")
)

canvas.create_text(
    190,
    360.0,
    anchor="n",
    text="Бесплатно & Безопасно\n2023",
    fill="#000000",
    font=("Monospace 16"),
    justify='center'
)

image_image_1 = PhotoImage(
    file=relative_to_assets("error.png"))
image_1 = canvas.create_image(
    188.0,
    163.0,
    image=image_image_1
)
window.resizable(False, False)
window.mainloop()