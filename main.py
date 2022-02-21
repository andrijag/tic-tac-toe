import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('TicTacToe')
        #root.geometry('800x600')
        #root.resizable(width=False, height=False)

def main():
    app = Application()
    app.mainloop()

if __name__ == '__main__':
    main()
