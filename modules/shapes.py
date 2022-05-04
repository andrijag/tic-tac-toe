from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, color, highlight_color):
        self.color = color
        self.highlight_color = highlight_color

    @abstractmethod
    def draw(self, canvas, x0, y0, x1, y1):
        pass


class Cross(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        return [
            canvas.create_line(x0, y0, x1, y1, width=10, fill=self.color),
            canvas.create_line(x0, y1, x1, y0, width=10, fill=self.color),
        ]


class Circle(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        return [canvas.create_oval(x0, y0, x1, y1, width=9, outline=self.color)]
