

class Car:
    def __init__(self, color=None, make=None, model=None, year=None):
        self.color = color
        self.make = make
        self.model = model
        self.year = year

    def __repr__(self):
        return f"SampleClass(attribute1={self.color!r}, attribute2={self.make!r})"
