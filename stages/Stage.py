from abc import abstractmethod
import tkinter as tk


class Stage:
    @abstractmethod
    def get_title(self) -> str:
        ...

    @abstractmethod
    def get_geometry(self) -> str:
        ...

    @abstractmethod
    def run(self, window: tk.Tk) -> None:
        ...

    def before_loop(self) -> None:
        pass

    def init(self) -> None:
        window = tk.Tk()

        window.resizable(False, False)

        window.title(self.get_title())
        window.geometry(self.get_geometry())

        # Удаляем все прошлые виджеты
        for widget in window.winfo_children():
            widget.destroy()

        self.run(window)

        self.before_loop()
        window.mainloop()

