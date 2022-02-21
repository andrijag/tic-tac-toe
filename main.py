import tkinter as tk
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TicTacToe')
        self.geometry('200x200')
        self.resizable(width=True, height=True)

        view = View(self)
        view.pack(fill=tk.BOTH, expand=True)


def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
