from abc import ABC, abstractmethod
import tkinter as tk


class Shape(ABC):
    def __init__(self, color: str, highlight: str) -> None:
        self._color = color
        self.highlight = highlight

    @abstractmethod
    def draw(
        self, canvas: tk.Canvas, x0: float, y0: float, x1: float, y1: float
    ) -> list[int]:
        pass


class Cross(Shape):
    def draw(
        self, canvas: tk.Canvas, x0: float, y0: float, x1: float, y1: float
    ) -> list[int]:
        width = x1 - x0
        height = y1 - y0
        ipadx = width / 10
        ipady = height / 10
        thickness = min(width, height) / 10
        return [
            canvas.create_line(
                x0 + ipadx,
                y0 + ipady,
                x1 - ipadx,
                y1 - ipady,
                fill=self._color,
                width=thickness,
            ),
            canvas.create_line(
                x0 + ipadx,
                y1 - ipady,
                x1 - ipadx,
                y0 + ipady,
                fill=self._color,
                width=thickness,
            ),
        ]


class Circle(Shape):
    def draw(
        self, canvas: tk.Canvas, x0: float, y0: float, x1: float, y1: float
    ) -> list[int]:
        width = x1 - x0
        height = y1 - y0
        ipadx = width / 10
        ipady = height / 10
        thickness = min(width, height) / 10
        return [
            canvas.create_oval(
                x0 + ipadx,
                y0 + ipady,
                x1 - ipadx,
                y1 - ipady,
                outline=self._color,
                width=thickness,
            )
        ]
