import math

class Shape:
    def __init__(self, side):
        self.side = side

    def get_area(self):
        pass

    def get_perimeter(self):
        pass

    def set_side(self, new_side):
        self.side = new_side

class Triangle(Shape):
    def get_area(self):
        return (math.sqrt(3) / 4) * self.side**2

    def get_perimeter(self):
        return 3 * self.side

class Square(Shape):
    def get_area(self):
        return self.side**2

    def get_perimeter(self):
        return 4 * self.side

class Circle(Shape):
    def get_area(self):
        return math.pi * self.side**2

    def get_perimeter(self):
        return 2 * math.pi * self.side

class CommandLine:
    @staticmethod
    def parse_input():
        input_str = input("Введите форму и размер (примеры triangle/square/circle 5): ")
        
        parts = input_str.split()
        if len(parts) < 2:
            return "Недостаточно аргументов"
        shape_type = parts[0].lower()
        side = float(parts[1])

        if shape_type == "triangle":
            shape = Triangle(side)
        elif shape_type == "square":
            shape = Square(side)
        elif shape_type == "circle":
            shape = Circle(side)
        else:
            return "Неподдерживаемый тип фигуры"

        area = shape.get_area()
        perimeter = shape.get_perimeter()

        print(f"Площадь: {area}, Периметр: {perimeter}")

        change_size = input("Хотите изменить размер фигуры? (yes/no): ")
        if change_size.lower() == "yes":
            new_size = float(input("Введите новый размер: "))
            shape.set_side(new_size)
            area = shape.get_area()
            perimeter = shape.get_perimeter()
            print(f"Площадь: {area}, Периметр: {perimeter}")


result = CommandLine.parse_input()
print(result)
