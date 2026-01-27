# ============================================================================
# PHASE 3: OOP & Classes - LESSONS
# ============================================================================
# Python classes are similar to JS/TS classes but with some key differences.
# Main gotchas: explicit `self`, __init__ instead of constructor, dunder methods (double underscore).

# -----------------------------------------------------------------------------
# 1. BASIC CLASS SYNTAX
# -----------------------------------------------------------------------------
# JS:
#   class Person {
#     constructor(name, age) {
#       this.name = name;
#       this.age = age;
#     }
#   }
#
# Python:
#   class Person:
#     def __init__(self, name, age):
#       self.name = name
#       self.age = age
#
# Key differences:
# - `__init__` instead of `constructor`
# - `self` instead of `this` (and it's EXPLICIT - must be first param)
# - No `new` keyword: Person("Alice", 30) not new Person("Alice", 30)


class Person:
    def __init__(self, name: str, age: int):
        self.name = name  # instance attribute
        self.age = age

    def greet(self) -> str:
        # `self` required as first param in ALL instance methods
        return f"Hi, I'm {self.name}"


def test_basic_class():
    p = Person("Alice", 30)  # no `new` keyword
    assert p.name == "Alice"
    assert p.age == 30
    assert p.greet() == "Hi, I'm Alice"


# -----------------------------------------------------------------------------
# 2. INSTANCE vs CLASS ATTRIBUTES
# -----------------------------------------------------------------------------
# Instance attributes: unique to each instance (defined in __init__ with self.x)
# Class attributes: shared by all instances (defined at class level)
#
# JS doesn't have true class attributes (static fields are different)


class Dog:
    species = "Canis familiaris"  # class attribute - shared by all dogs

    def __init__(self, name: str):
        self.name = name  # instance attribute - unique to each dog


def test_class_vs_instance_attrs():
    fido = Dog("Fido")
    buddy = Dog("Buddy")

    # Instance attributes are unique
    assert fido.name == "Fido"
    assert buddy.name == "Buddy"

    # Class attribute is shared
    assert fido.species == "Canis familiaris"
    assert buddy.species == "Canis familiaris"
    assert Dog.species == "Canis familiaris"  # can access on class itself


# -----------------------------------------------------------------------------
# 3. METHODS: instance, class, static
# -----------------------------------------------------------------------------
# - Instance methods: take `self`, operate on instance
# - Class methods: take `cls`, operate on class (like factory methods)
# - Static methods: no self/cls, just namespaced functions
#
# JS equivalent:
#   instance method → regular method
#   class method → static method that uses `this` (the class)
#   static method → static method


class Calculator:
    def __init__(self, value: int = 0):
        self.value = value

    # Instance method - has access to self
    def add(self, n: int) -> "Calculator":
        self.value += n
        return self  # return self for chaining

    # Class method - @classmethod decorator, first param is `cls` (the class)
    # Good for alternative constructors
    @classmethod
    def from_string(cls, s: str) -> "Calculator":
        return cls(int(s))  # cls() calls __init__

    # Static method - no self or cls, just a regular function namespaced to class
    @staticmethod
    def is_valid_number(s: str) -> bool:
        return s.lstrip("-").isdigit()


def test_method_types():
    # Instance method
    calc = Calculator(10)
    calc.add(5)
    assert calc.value == 15

    # Class method - alternative constructor
    calc2 = Calculator.from_string("42")
    assert calc2.value == 42

    # Static method - utility function
    assert Calculator.is_valid_number("123") is True
    assert Calculator.is_valid_number("-45") is True
    assert Calculator.is_valid_number("abc") is False


# -----------------------------------------------------------------------------
# 4. DUNDER METHODS (Magic Methods)
# -----------------------------------------------------------------------------
# "Dunder" = double underscore: __method__
# These customize how objects behave with operators and built-in functions.
#
# Common ones:
#   __init__     → constructor
#   __str__      → str(obj), print(obj) - human-readable
#   __repr__     → repr(obj), debugger display - unambiguous
#   __eq__       → obj1 == obj2
#   __lt__       → obj1 < obj2 (enables sorting)
#   __len__      → len(obj)
#   __getitem__  → obj[key]
#   __iter__     → for item in obj
#
# JS equivalent: Symbol.iterator, valueOf, toString, etc.


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        # For debugging - should be unambiguous
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        # For display - can be friendlier
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        # Define equality - without this, == compares identity (like JS ===)
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Point") -> "Point":
        # Enable: point1 + point2
        return Point(self.x + other.x, self.y + other.y)


def test_dunder_methods():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)

    # __repr__
    assert repr(p1) == "Point(1, 2)"

    # __str__
    assert str(p1) == "(1, 2)"

    # __eq__ - without this, p1 == p2 would be False (different objects)
    assert p1 == p2
    assert p1 != p3

    # __add__
    assert p1 + p3 == Point(4, 6)


# -----------------------------------------------------------------------------
# 5. PROPERTIES (@property)
# -----------------------------------------------------------------------------
# Properties let you define getters/setters that look like attribute access.
# Useful for computed values or validation.
#
# JS equivalent:
#   get fullName() { return ... }
#   set fullName(value) { ... }


class Circle:
    def __init__(self, radius: float):
        self._radius = radius  # underscore = "private by convention"

    @property
    def radius(self) -> float:
        # Getter - accessed as circle.radius (no parentheses)
        return self._radius

    @radius.setter
    def radius(self, value: float):
        # Setter - called when circle.radius = x
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:
        # Read-only computed property (no setter)
        return 3.14159 * self._radius**2


def test_properties():
    c = Circle(5)

    # Getter
    assert c.radius == 5

    # Computed property
    assert round(c.area, 2) == 78.54

    # Setter with validation
    c.radius = 10
    assert c.radius == 10

    # Setter validation
    try:
        c.radius = -1
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # expected


# -----------------------------------------------------------------------------
# 6. INHERITANCE
# -----------------------------------------------------------------------------
# Python uses parentheses for inheritance: class Child(Parent)
# super() calls parent methods
#
# JS: class Child extends Parent { constructor() { super(); } }
# Py: class Child(Parent): def __init__(self): super().__init__()


class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."


class Cat(Animal):  # Cat inherits from Animal
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name)  # call parent __init__
        self.indoor = indoor

    def speak(self) -> str:  # override parent method
        return "Meow!"


class Dog2(Animal):
    def speak(self) -> str:
        return "Woof!"


def test_inheritance():
    cat = Cat("Whiskers")
    dog = Dog2("Rex")

    # Inherited attribute
    assert cat.name == "Whiskers"
    assert dog.name == "Rex"

    # Overridden method
    assert cat.speak() == "Meow!"
    assert dog.speak() == "Woof!"

    # isinstance checks inheritance
    assert isinstance(cat, Cat)
    assert isinstance(cat, Animal)


# -----------------------------------------------------------------------------
# 7. DATACLASSES (Python 3.7+)
# -----------------------------------------------------------------------------
# Dataclasses auto-generate __init__, __repr__, __eq__ and more.
# Great for simple data containers - less boilerplate.
#
# Similar to TypeScript interfaces or records.

from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    pages: int
    price: float = 9.99  # default value


def test_dataclass():
    book1 = Book("1984", "Orwell", 328)
    book2 = Book("1984", "Orwell", 328)

    # Auto-generated __init__
    assert book1.title == "1984"
    assert book1.price == 9.99  # default

    # Auto-generated __repr__
    assert "Book(" in repr(book1)

    # Auto-generated __eq__
    assert book1 == book2  # compares all fields
