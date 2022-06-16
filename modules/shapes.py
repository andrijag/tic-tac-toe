from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, color, highlight):
        self._color = color
        self.highlight = highlight

    @abstractmethod
    def draw(self, canvas, x0, y0, x1, y1):
        pass


class Cross(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        return [
            canvas.create_line(x0, y0, x1, y1, width=10, fill=self._color),
            canvas.create_line(x0, y1, x1, y0, width=10, fill=self._color),
        ]


class Circle(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        return [canvas.create_oval(x0, y0, x1, y1, width=11, outline=self._color)]
