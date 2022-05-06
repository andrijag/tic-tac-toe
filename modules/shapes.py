from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, color, highlight):
        self.color = color
        self.highlight = highlight

    @abstractmethod
    def draw(self, canvas, x0, y0, x1, y1, width=1):
        pass


class Cross(Shape):
    def draw(self, canvas, x0, y0, x1, y1, width=1):
        kwargs = {"width": width, "fill": self.color}
        return [
            canvas.create_line(x0, y0, x1, y1, **kwargs),
            canvas.create_line(x0, y1, x1, y0, **kwargs),
        ]


class Circle(Shape):
    def draw(self, canvas, x0, y0, x1, y1, width=1):
        kwargs = {"width": width, "outline": self.color}
        return [canvas.create_oval(x0, y0, x1, y1, **kwargs)]
