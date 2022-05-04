from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, color, highlight):
        self.color = color
        self.highlight = highlight

    @abstractmethod
    def draw(self, canvas, x0, y0, x1, y1):
        pass


class Cross(Shape):
    def __init__(self, *args):
        super().__init__(*args)
        self.kwargs = {"width": 10, "fill": self.color}

    def draw(self, canvas, x0, y0, x1, y1):
        return [
            canvas.create_line(x0, y0, x1, y1, **self.kwargs),
            canvas.create_line(x0, y1, x1, y0, **self.kwargs),
        ]


class Circle(Shape):
    def __init__(self, *args):
        super().__init__(*args)
        self.kwargs = {"width": 9, "outline": self.color}

    def draw(self, canvas, x0, y0, x1, y1):
        return [canvas.create_oval(x0, y0, x1, y1, **self.kwargs)]
