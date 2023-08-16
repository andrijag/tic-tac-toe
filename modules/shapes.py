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
        ipadx = (x1 - x0) / 10
        ipady = (y1 - y0) / 10
        return [
            canvas.create_line(
                x0 + ipadx,
                y0 + ipady,
                x1 - ipadx,
                y1 - ipady,
                width=5,
                fill=self._color,
            ),
            canvas.create_line(
                x0 + ipadx,
                y1 - ipady,
                x1 - ipadx,
                y0 + ipady,
                width=5,
                fill=self._color,
            ),
        ]


class Circle(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        ipadx = (x1 - x0) / 10
        ipady = (y1 - y0) / 10
        return [
            canvas.create_oval(
                x0 + ipadx,
                y0 + ipady,
                x1 - ipadx,
                y1 - ipady,
                width=5,
                outline=self._color,
            )
        ]
