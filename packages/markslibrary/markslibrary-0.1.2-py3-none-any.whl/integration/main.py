from mylibrary.module1 import hello_world
from mylibrary.models import Car

def main():
    greeting = hello_world()
    print(greeting)

    car = Car("red", "Ford", "Mustang", 1966)
    print(car)

if __name__ == "__main__":
    main()
