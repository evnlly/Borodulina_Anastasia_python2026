class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.height * self.width

    def perimetr(self):
        return 2 * (self.height + self.width)

    def __eq__(self, other):
        return self.area == other.area

    def __lt__(self, other):
        return self.area < other.area

    def __add__(self, other):
        if self.width == other.width:
            return Rectangle(self.width, self.height + other.height)
        if self.height == other.height:
            return Rectangle(self.width + other.width, self.height)
        if self.height == other.width:
            return Rectangle(self.width + other.height, self.height)
        if self.width == other.height:
            return Rectangle(self.width, self.height + other.width)
        raise ValueError('Нет подходящих сторон')

    def __repr__(self):
        return f"Rectangle({self.width}, {self.height})"

    def __str__(self):
        return f"Прямоугольник {self.width}X{self.height}"
