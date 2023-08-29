from mylibrary.models import Car


class Client:
    def __init__(self, url=None):
        self.url = url

    def get_cars(self):
        car = Car("red")
        return car

    def __repr__(self):
        return f"SampleClass(attribute1={self.color!r}, attribute2={self.make!r})"
