import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TicTacToe')
        self.geometry('200x200')
        self.resizable(width=True, height=True)

def main():
    app = Application()
    app.mainloop()

if __name__ == '__main__':
    main()
