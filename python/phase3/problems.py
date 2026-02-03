# ============================================================================
# PHASE 3: OOP & Classes - PROBLEMS
# ============================================================================
# Practice problems for Phase 3 concepts.
# Run tests: npm run test:py -- python/phase3/problems.py


# -----------------------------------------------------------------------------
# PROBLEM 1: BankAccount
# -----------------------------------------------------------------------------
# Create a BankAccount class with:
# - __init__ that takes owner (str) and optional starting balance (default 0)
# - deposit(amount) method - adds to balance, returns new balance
# - withdraw(amount) method - subtracts from balance if sufficient funds
#   - if insufficient funds, raise ValueError with message "Insufficient funds"
#   - returns new balance on success
# - balance property (read-only) - returns current balance
# - __repr__ that returns "BankAccount(owner='...', balance=...)"
#
# Hints:
# - Use @property for read-only balance
# - Store balance in self._balance (underscore = private convention)
# - Remember to validate withdrawal amount
#
class BankAccount:
    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount: int) -> int:
        self._balance += amount
        return self._balance

    def withdraw(self, amount: int) -> int:
        new_balance = self._balance - amount

        if new_balance < 0:
            raise ValueError("Insufficient funds")

        self._balance = new_balance
        return new_balance

    @property
    def balance(self) -> int:
        return self._balance

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"


def test_bank_account():
    # Basic creation
    acc = BankAccount("Alice")
    assert acc.owner == "Alice"
    assert acc.balance == 0

    # With starting balance
    acc2 = BankAccount("Bob", 100)
    assert acc2.balance == 100

    # Deposit
    result = acc2.deposit(50)
    assert result == 150
    assert acc2.balance == 150

    # Withdraw success
    result = acc2.withdraw(30)
    assert result == 120
    assert acc2.balance == 120

    # Withdraw insufficient funds
    try:
        acc2.withdraw(200)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Insufficient funds" in str(e)

    # Balance unchanged after failed withdrawal
    assert acc2.balance == 120

    # __repr__
    assert repr(acc2) == "BankAccount(owner='Bob', balance=120)"


# -----------------------------------------------------------------------------
# PROBLEM 2: Rectangle
# -----------------------------------------------------------------------------
# Create a Rectangle class with:
# - __init__ that takes width and height (both positive numbers)
#   - raise ValueError if either is <= 0
# - width and height properties (read-only)
# - area property (computed, read-only) - returns width * height
# - perimeter property (computed, read-only) - returns 2 * (width + height)
# - is_square() method - returns True if width == height
# - __eq__ to compare two rectangles (equal if same width and height)
# - __repr__ that returns "Rectangle(width=..., height=...)"
#
# Hints:
# - All properties can use @property decorator
# - __eq__ receives `other` as second param, compare attributes
# - Consider: what should __eq__ return if `other` isn't a Rectangle?
#


class Rectangle:
    def __init__(self, width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValueError("Oh Noes!")

        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def area(self) -> int:
        return self._width * self._height

    @property
    def perimeter(self) -> int:
        return (self._width + self._height) * 2

    def is_square(self) -> bool:
        return self._width == self._height

    def __eq__(self, other) -> bool:
        if not isinstance(other, Rectangle):
            return NotImplemented

        return self._height == other._height and self._width == other._width

    def __repr__(self) -> str:
        return f"Rectangle(width={self._width}, height={self._height})"


def test_rectangle():
    # Basic creation
    r1 = Rectangle(4, 5)
    assert r1.width == 4
    assert r1.height == 5

    # Computed properties
    assert r1.area == 20
    assert r1.perimeter == 18

    # is_square
    assert r1.is_square() is False
    square = Rectangle(3, 3)
    assert square.is_square() is True

    # Validation
    try:
        Rectangle(-1, 5)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        Rectangle(5, 0)
        assert False, "Should raise ValueError"
        pass
    except ValueError:
        pass

    # Equality
    r2 = Rectangle(4, 5)
    r3 = Rectangle(5, 4)
    assert r1 == r2
    assert r1 != r3

    # __repr__
    assert repr(r1) == "Rectangle(width=4, height=5)"


# -----------------------------------------------------------------------------
# PROBLEM 3: Temperature
# -----------------------------------------------------------------------------
# Create a Temperature class with:
# - __init__ that takes celsius (float)
# - celsius property (read-only)
# - fahrenheit property (computed, read-only) - converts celsius to fahrenheit
# - from_fahrenheit(f) classmethod - alternate constructor, creates Temperature from F
# - __repr__ that returns "Temperature(celsius=...)"
# - __eq__ to compare temperatures (equal if same celsius value)
#
# Formula: F = C * 9/5 + 32  (and reverse: C = (F - 32) * 5/9)
# Hints:
# - @classmethod receives `cls` as first param (like `self` but for the class)
# - cls(...) creates a new instance, like calling Temperature(...)
# - Use cls instead of Temperature to support subclasses
#
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @classmethod
    def from_fahrenheit(cls, f) -> "Temperature":
        celsius = (f - 32) * 5 / 9
        return cls(celsius)

    def __repr__(self) -> str:
        return f"Temperature(celsius={self._celsius})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented

        return other.celsius == self._celsius


def test_temperature():
    # Basic creation (Celsius)
    t1 = Temperature(0)
    assert t1.celsius == 0
    assert t1.fahrenheit == 32

    t2 = Temperature(100)
    assert t2.celsius == 100
    assert t2.fahrenheit == 212

    # Alternate constructor (from Fahrenheit)
    t3 = Temperature.from_fahrenheit(32)
    assert t3.celsius == 0

    t4 = Temperature.from_fahrenheit(212)
    assert t4.celsius == 100

    # Negative temps
    t5 = Temperature(-40)
    assert t5.fahrenheit == -40  # -40 is same in both scales!

    # Equality
    assert t1 == Temperature(0)
    assert t1 == Temperature.from_fahrenheit(32)
    assert t1 != t2

    # __repr__
    assert repr(t1) == "Temperature(celsius=0)"
    assert repr(t2) == "Temperature(celsius=100)"


# -----------------------------------------------------------------------------
# PROBLEM 4: Person & Employee (Inheritance)
# -----------------------------------------------------------------------------
# Create two classes demonstrating inheritance:
#
# Person class:
# - __init__ takes name (str) and age (int)
# - name and age properties (read-only)
# - greet() method returns "Hello, I'm {name}"
# - __repr__ returns "Person(name='...', age=...)"
#
# Employee class (inherits from Person):
# - __init__ takes name, age, and employee_id (str)
# - employee_id property (read-only)
# - greet() method returns "Hello, I'm {name}, employee #{employee_id}"
# - __repr__ returns "Employee(name='...', age=..., employee_id='...')"
# Hints:
# - class Employee(Person): to inherit
# - super().__init__(name, age) to call parent constructor
# - Override methods by redefining them in subclass
# - Can access parent's attributes (self.name works in Employee)
#


class Person:
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    def greet(self) -> str:
        return f"Hello, I'm {self._name}"

    def __repr__(self) -> str:
        return f"Person(name={self._name!r}, age={self._age})"


class Employee(Person):
    def __init__(self, name: str, age: int, employee_id: str):
        super().__init__(name, age)
        self._employee_id = employee_id

    @property
    def employee_id(self) -> str:
        return self._employee_id

    def greet(self) -> str:
        return f"Hello, I'm {self.name}, employee #{self.employee_id}"

    def __repr__(self) -> str:
        return f"Employee(name={self._name!r}, age={self._age}, employee_id={self._employee_id!r})"


def test_person():
    p = Person("Alice", 30)
    assert p.name == "Alice"
    assert p.age == 30
    assert p.greet() == "Hello, I'm Alice"
    assert repr(p) == "Person(name='Alice', age=30)"


def test_employee():
    e = Employee("Bob", 25, "E123")

    # Inherited attributes
    assert e.name == "Bob"
    assert e.age == 25

    # New attribute
    assert e.employee_id == "E123"

    # Overridden method
    assert e.greet() == "Hello, I'm Bob, employee #E123"

    # Overridden __repr__
    assert repr(e) == "Employee(name='Bob', age=25, employee_id='E123')"

    # isinstance checks
    assert isinstance(e, Employee)
    assert isinstance(e, Person)  # Employee IS-A Person


# -----------------------------------------------------------------------------
# PROBLEM 5: Counter (Operator Overloading)
# -----------------------------------------------------------------------------
# Create a Counter class that supports arithmetic and comparison operators:
#
# - __init__ takes optional starting value (default 0)
# - value property (read-only)
# - increment() adds 1, returns self (for chaining)
# - decrement() subtracts 1, returns self (for chaining)
# - __add__(other) - Counter + Counter or Counter + int, returns NEW Counter
# - __eq__(other) - compare by value
# - __lt__(other) - less than comparison (enables sorting!)
# - __repr__ returns "Counter(value=...)"
#
# JS has no equivalent - you'd manually call counter1.add(counter2)
# Python lets you write: counter1 + counter2
#
# Hints:
# - __add__ should handle both Counter and int types
# - Return NEW Counter from __add__, don't mutate self
# - __lt__ enables sorted() to work on lists of Counters
# - "returns self" pattern enables: counter.increment().increment()
#


class Counter:
    def __init__(self, value: int = 0):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def increment(self) -> "Counter":
        self._value += 1
        return self

    def decrement(self) -> "Counter":
        self._value -= 1
        return self

    def __add__(self, other) -> "Counter":
        if isinstance(other, Counter):
            return Counter(self.value + other.value)
        elif isinstance(other, int):
            return Counter(self.value + other)
        return NotImplemented

    def __eq__(self, other) -> bool:
        if not isinstance(other, Counter):
            return NotImplemented

        return self.value == other.value

    def __lt__(self, other) -> bool:
        if not isinstance(other, Counter):
            return NotImplemented

        return self.value < other.value

    def __repr__(self) -> str:
        return f"Counter(value={self.value})"


def test_counter():
    # Basic creation
    c1 = Counter()
    assert c1.value == 0

    c2 = Counter(10)
    assert c2.value == 10

    # Increment/decrement with chaining
    c1.increment().increment().increment()
    assert c1.value == 3

    c2.decrement()
    assert c2.value == 9

    # Addition: Counter + Counter
    c3 = c1 + c2
    assert c3.value == 12
    assert c1.value == 3  # originals unchanged
    assert c2.value == 9

    # Addition: Counter + int
    c4 = c1 + 5
    assert c4.value == 8

    # Equality
    assert Counter(5) == Counter(5)
    assert Counter(5) != Counter(3)

    # Less than (enables sorting)
    assert Counter(3) < Counter(5)
    assert not Counter(5) < Counter(3)

    counters = [Counter(5), Counter(2), Counter(8), Counter(1)]
    sorted_counters = sorted(counters)
    assert [c.value for c in sorted_counters] == [1, 2, 5, 8]

    # __repr__
    assert repr(c1) == "Counter(value=3)"


# -----------------------------------------------------------------------------
# PROBLEM 6: Playlist (Collection Protocol)
# -----------------------------------------------------------------------------
# Create a Playlist class that behaves like a collection.
#
# WHAT YOU IMPLEMENT:
# - __init__ takes name (str), starts with empty list of songs
# - name property (read-only)
# - add(song: str) - adds song to playlist
# - __len__ - return number of songs
# - __getitem__(index) - return song at index
# - __contains__(song) - return True if song in playlist
# - __iter__ - return iterator over songs
# - __repr__ returns "Playlist(name='...', songs=[...])"
#
# WHAT THESE ENABLE (used in tests, you don't implement these):
# - __len__      -> len(playlist) calls your __len__
# - __getitem__  -> playlist[0] calls your __getitem__(0)
# - __contains__ -> "song" in playlist calls your __contains__("song")
# - __iter__     -> for song in playlist: calls your __iter__
#
# Hints:
# - Store songs in a list: self._songs = []
# - __iter__ can simply return iter(self._songs)
# - __getitem__ can simply return self._songs[index]
# - __contains__ can use `in` on your internal list
#


class Playlist:
    def __init__(self, name: str):
        self._name = name
        self._songs = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, song: str):
        self._songs.append(song)

    def __len__(self) -> int:
        return len(self._songs)

    def __getitem__(self, index: int) -> str:
        return self._songs[index]

    def __contains__(self, song: str) -> bool:
        return song in self._songs

    def __iter__(self):
        return iter(self._songs)

    def __repr__(self):
        return f"Playlist(name={self._name!r}, songs={self._songs})"


def test_playlist():
    p = Playlist("Road Trip")
    assert p.name == "Road Trip"

    # Add songs
    p.add("Bohemian Rhapsody")
    p.add("Hotel California")
    p.add("Stairway to Heaven")

    # __len__ enables: len(playlist)
    assert len(p) == 3

    # __getitem__ enables: playlist[index]
    assert p[0] == "Bohemian Rhapsody"
    assert p[2] == "Stairway to Heaven"
    assert p[-1] == "Stairway to Heaven"  # negative indexing works too

    # __contains__ enables: "song" in playlist
    assert "Hotel California" in p
    assert "Wonderwall" not in p

    # __iter__ enables: for song in playlist
    songs = []
    for song in p:
        songs.append(song)
    assert songs == ["Bohemian Rhapsody", "Hotel California", "Stairway to Heaven"]

    # __iter__ also enables: list(playlist)
    assert list(p) == ["Bohemian Rhapsody", "Hotel California", "Stairway to Heaven"]

    # __repr__
    assert (
        repr(p)
        == "Playlist(name='Road Trip', songs=['Bohemian Rhapsody', 'Hotel California', 'Stairway to Heaven'])"
    )


# -----------------------------------------------------------------------------
# PROBLEM 7: Dice (staticmethod + __str__ vs __repr__)
# -----------------------------------------------------------------------------
# Create a Dice class that models rolling dice:
#
# - __init__ takes sides (int, default 6)
#   - raise ValueError if sides < 2
# - sides property (read-only)
# - roll() method - returns random int from 1 to sides (inclusive)
# - roll_multiple(n) method - returns list of n rolls
# - probability(target) staticmethod - returns 1/target as a float
#   (probability of rolling a specific number on a target-sided die)
# - __repr__ returns "Dice(sides=...)"            <- for devs
# - __str__ returns "d..." (e.g. "d6", "d20")     <- for users
#
# KEY CONCEPT: __str__ vs __repr__
# - __repr__ = developer-facing, unambiguous, ideally eval()-able
# - __str__  = user-facing, readable, used by print() and str()
# - print(obj) calls __str__, falling back to __repr__
# - repr(obj) always calls __repr__
# - f"{obj}" calls __str__
#
# JS equivalent: toString() is like __str__. Python splits this into two.
#
# Hints:
# - import random, use random.randint(1, self._sides)
# - @staticmethod doesn't take self or cls — it's just a function
#   that lives on the class for organizational purposes
# - Think of staticmethod like a JS static method: Dice.probability(6)
#

import random


class Dice:
    def __init__(self, sides: int = 6):
        if sides < 2:
            raise ValueError("Oh noes!")

        self._sides = sides

    @property
    def sides(self) -> int:
        return self._sides

    def roll(self) -> int:
        return random.randint(1, self._sides)

    def roll_multiple(self, num_of_rolls: int) -> list[int]:
        return [self.roll() for _ in range(num_of_rolls)]

    @staticmethod
    def probability(target: int) -> float:
        return 1 / target

    def __repr__(self):
        return f"Dice(sides={self._sides})"

    def __str__(self):
        return f"d{self._sides}"


def test_dice():
    # Basic creation
    d6 = Dice()
    assert d6.sides == 6

    d20 = Dice(20)
    assert d20.sides == 20

    # Validation
    try:
        Dice(1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Roll returns value in range
    for _ in range(100):
        val = d6.roll()
        assert 1 <= val <= 6

    for _ in range(100):
        val = d20.roll()
        assert 1 <= val <= 20

    # Roll multiple
    rolls = d6.roll_multiple(5)
    assert len(rolls) == 5
    assert all(1 <= r <= 6 for r in rolls)

    # Static method (no instance needed)
    assert Dice.probability(6) == 1 / 6
    assert Dice.probability(20) == 1 / 20
    # Can also call on instance
    assert d6.probability(6) == 1 / 6

    # __repr__ vs __str__
    assert repr(d6) == "Dice(sides=6)"
    assert str(d6) == "d6"
    assert repr(d20) == "Dice(sides=20)"
    assert str(d20) == "d20"

    # f-string uses __str__
    assert f"Rolling a {d20}" == "Rolling a d20"


# -----------------------------------------------------------------------------
# PROBLEM 8: Product (dataclasses)
# -----------------------------------------------------------------------------
# Rewrite a typical "data holder" class using @dataclass.
#
# Without dataclass, you'd write __init__, __repr__, __eq__ manually
# (like you've been doing). @dataclass auto-generates all of that.
#
# Create a Product dataclass with:
# - name: str
# - price: float
# - quantity: int = 0          (default value)
# - total_value property       (price * quantity)
# - apply_discount(pct) method (returns NEW Product with discounted price)
#
# Also create an Inventory dataclass with:
# - products: list[Product]    (use field(default_factory=list))
# - add(product) method
# - total_value property       (sum of all product total_values)
# - most_expensive property    (product with highest price)
#
# KEY CONCEPT: @dataclass
# - Auto-generates __init__, __repr__, __eq__ from field declarations
# - Fields are declared as class-level type annotations
# - Default values work like function defaults
# - For mutable defaults (list, dict), use field(default_factory=list)
# - You can still add methods, properties, and custom dunders
#
# JS equivalent: like defining a TS interface + constructor in one shot.
# Similar vibe to a Record type or a plain object with guaranteed shape.
#
# Hints:
# - from dataclasses import dataclass, field
# - @dataclass goes above the class definition
# - Fields with defaults must come AFTER fields without defaults
# - field(default_factory=list) avoids the mutable default gotcha
#   (same issue as def foo(items=[]) in plain Python)
# - apply_discount should return Product(self.name, new_price, self.quantity)
#

from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0

    @property
    def total_value(self) -> float:
        return self.price * self.quantity

    def apply_discount(self, pct: float) -> "Product":
        discounted_price = self.price - (self.price * pct / 100)
        return Product(self.name, discounted_price, self.quantity)


@dataclass
class Inventory:
    products: list[Product] = field(default_factory=list)

    def add(self, product: Product):
        self.products.append(product)

    @property
    def total_value(self) -> float:
        return sum(product.total_value for product in self.products)

    @property
    def most_expensive(self) -> "Product":
        return max(self.products, key=lambda p: p.price)


def test_product():
    # Auto-generated __init__
    p1 = Product("Widget", 9.99, 5)
    assert p1.name == "Widget"
    assert p1.price == 9.99
    assert p1.quantity == 5

    # Default value
    p2 = Product("Gadget", 19.99)
    assert p2.quantity == 0

    # Auto-generated __repr__
    assert repr(p2) == "Product(name='Gadget', price=19.99, quantity=0)"

    # Auto-generated __eq__ (compares all fields)
    p3 = Product("Widget", 9.99, 5)
    assert p1 == p3
    assert p1 != p2

    # Custom property
    assert p1.total_value == 9.99 * 5
    assert p2.total_value == 0

    # Custom method
    p4 = p1.apply_discount(10)  # 10% off
    assert p4.price == 8.991  # 9.99 * 0.9
    assert p4.name == "Widget"
    assert p4.quantity == 5
    assert p1.price == 9.99  # original unchanged


def test_inventory():
    inv = Inventory()
    assert inv.products == []

    p1 = Product("Widget", 9.99, 5)
    p2 = Product("Gadget", 19.99, 3)
    p3 = Product("Doohickey", 4.99, 10)

    inv.add(p1)
    inv.add(p2)
    inv.add(p3)

    assert len(inv.products) == 3

    # total_value sums all products
    expected = (9.99 * 5) + (19.99 * 3) + (4.99 * 10)
    assert inv.total_value == expected

    # most_expensive by price
    assert inv.most_expensive == p2

    # Two separate inventories don't share products (default_factory)
    inv2 = Inventory()
    assert inv2.products == []
    assert len(inv.products) == 3  # original unaffected


# -----------------------------------------------------------------------------
# PROBLEM 9: Shape hierarchy (Abstract Base Classes)
# -----------------------------------------------------------------------------
# Create an abstract Shape base class and concrete subclasses.
#
# Shape (abstract):
# - area() abstract method — must be implemented by subclasses
# - perimeter() abstract method — must be implemented by subclasses
# - describe() concrete method — returns "{class_name}: area={area}, perimeter={perimeter}"
#   (round both to 2 decimal places using round())
#
# Circle(Shape):
# - __init__ takes radius (float)
# - area = pi * r^2
# - perimeter = 2 * pi * r
#
# Triangle(Shape):
# - __init__ takes a, b, c (three side lengths as floats)
# - perimeter = a + b + c
# - area uses Heron's formula:
#     s = perimeter / 2
#     area = sqrt(s * (s-a) * (s-b) * (s-c))
#
# KEY CONCEPT: Abstract Base Classes (ABCs)
# - Like TypeScript interfaces, but enforced at instantiation time
# - If you forget to implement an abstract method, Python raises TypeError
#   when you try to create an instance (not at class definition)
# - from abc import ABC, abstractmethod
# - class Shape(ABC): makes Shape abstract
# - @abstractmethod marks methods subclasses MUST implement
# - Abstract classes CAN have concrete methods (describe() here)
#
# TS equivalent:
#   abstract class Shape {
#     abstract area(): number;
#     abstract perimeter(): number;
#     describe(): string { ... }  // concrete method on abstract class
#   }
#
# Hints:
# - import math for math.pi and math.sqrt
# - type(self).__name__ gets the class name as a string
# - describe() calls self.area() and self.perimeter() — polymorphism!
#   The base class method calls methods that don't exist on itself,
#   trusting subclasses to provide them
#

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):
        return f"{type(self).__name__}: area={round(self.area(), 2)}, perimeter={round(self.perimeter(), 2)}"


class Circle(Shape):
    def __init__(self, radius):
        self._radius = radius

    def area(self) -> float:
        return math.pi * (self._radius**2)

    def perimeter(self) -> float:
        return 2 * math.pi * self._radius


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self._a = a
        self._b = b
        self._c = c

    def perimeter(self) -> float:
        return self._a + self._b + self._c

    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self._a) * (s - self._b) * (s - self._c))


def test_shape_abstract():
    # Can't instantiate abstract class
    try:
        Shape()
        assert False, "Should raise TypeError"
    except TypeError:
        pass


def test_circle():
    c = Circle(5)
    assert round(c.area(), 2) == 78.54
    assert round(c.perimeter(), 2) == 31.42
    assert c.describe() == "Circle: area=78.54, perimeter=31.42"
    assert isinstance(c, Shape)


def test_triangle():
    # 3-4-5 right triangle
    t = Triangle(3, 4, 5)
    assert t.area() == 6.0
    assert t.perimeter() == 12
    assert t.describe() == "Triangle: area=6.0, perimeter=12"
    assert isinstance(t, Shape)

    # Equilateral triangle (side=10)
    eq = Triangle(10, 10, 10)
    assert round(eq.area(), 2) == 43.3
    assert eq.perimeter() == 30


def test_polymorphism():
    # Different shapes, same interface
    shapes = [Circle(5), Triangle(3, 4, 5)]
    areas = [round(s.area(), 2) for s in shapes]
    assert areas == [78.54, 6.0]

    # describe() works on all shapes — polymorphism via ABC
    descriptions = [s.describe() for s in shapes]
    assert descriptions == [
        "Circle: area=78.54, perimeter=31.42",
        "Triangle: area=6.0, perimeter=12",
    ]


# -----------------------------------------------------------------------------
# PROBLEM 10: Engine & Car (Composition)
# -----------------------------------------------------------------------------
# Demonstrate "has-a" relationships using composition instead of inheritance.
#
# Engine class:
# - __init__ takes horsepower (int) and fuel_type (str, e.g. "gasoline", "diesel")
# - horsepower and fuel_type properties (read-only)
# - start() method returns "Engine started" and sets is_running to True
# - stop() method returns "Engine stopped" and sets is_running to False
# - is_running property (read-only, starts False)
# - __repr__ returns "Engine(horsepower=..., fuel_type='...')"
#
# Car class:
# - __init__ takes make (str), model (str), and engine (Engine instance)
# - make, model, engine properties (read-only)
# - start() method - calls engine.start(), returns "Car started"
#   - if engine already running, return "Engine already running"
# - stop() method - calls engine.stop(), returns "Car stopped"
#   - if engine not running, return "Engine not running"
# - honk() method returns "Beep beep!"
# - describe() returns "{make} {model} with {horsepower}hp {fuel_type} engine"
# - __repr__ returns "Car(make='...', model='...', engine=...)"
#
# KEY CONCEPT: Composition vs Inheritance
# - Inheritance = "is-a" (Employee IS-A Person)
# - Composition = "has-a" (Car HAS-AN Engine)
# - Favor composition when objects have different lifecycles or can be swapped
# - Engine could be replaced; Car delegates to Engine rather than being one
#
# JS equivalent: In JS you'd store engine as a property and call this.engine.start()
# Same pattern, just more formalized in OOP terminology.
#
# Hints:
# - Car doesn't inherit from Engine — it CONTAINS an Engine
# - Car.start() delegates to self._engine.start()
# - describe() accesses engine properties via self._engine.horsepower etc.
#


class Engine:
    def __init__(self, horsepower: int, fuel_type: str):
        self._horsepower = horsepower
        self._fuel_type = fuel_type
        self._is_running = False

    @property
    def horsepower(self) -> int:
        return self._horsepower

    @property
    def fuel_type(self) -> str:
        return self._fuel_type

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool):
        self._is_running = value

    def start(self) -> str:
        self.is_running = True
        return f"Engine started"

    def stop(self) -> str:
        self.is_running = False
        return f"Engine stopped"

    def __repr__(self) -> str:
        return f"Engine(horsepower={self._horsepower}, fuel_type='{self.fuel_type}')"


class Car:
    def __init__(self, make: str, model: str, engine: Engine):
        self._make = make
        self._model = model
        self._engine = engine

    @property
    def make(self) -> str:
        return self._make

    @property
    def model(self) -> str:
        return self._model

    @property
    def engine(self) -> Engine:
        return self._engine

    def start(self) -> str:
        if self._engine.is_running:
            return "Engine already running"

        self._engine.start()
        return "Car started"

    def stop(self) -> str:
        if not self._engine.is_running:
            return "Engine not running"

        self._engine.stop()
        return "Car stopped"

    def honk(self) -> str:
        return "Beep beep!"

    def describe(self) -> str:
        return f"{self.make} {self.model} with {self._engine.horsepower}hp {self._engine.fuel_type} engine"

    def __repr__(self):
        return f"Car(make='{self.make}', model='{self.model}', engine={self.engine})"


def test_engine():
    e = Engine(250, "gasoline")
    assert e.horsepower == 250
    assert e.fuel_type == "gasoline"
    assert e.is_running is False

    # Start
    result = e.start()
    assert result == "Engine started"
    assert e.is_running is True

    # Stop
    result = e.stop()
    assert result == "Engine stopped"
    assert e.is_running is False

    # __repr__
    assert repr(e) == "Engine(horsepower=250, fuel_type='gasoline')"


def test_car():
    engine = Engine(200, "diesel")
    car = Car("Toyota", "Hilux", engine)

    assert car.make == "Toyota"
    assert car.model == "Hilux"
    assert car.engine is engine  # same object, not a copy

    # Start delegates to engine
    result = car.start()
    assert result == "Car started"
    assert engine.is_running is True

    # Already running
    result = car.start()
    assert result == "Engine already running"

    # Stop
    result = car.stop()
    assert result == "Car stopped"
    assert engine.is_running is False

    # Not running
    result = car.stop()
    assert result == "Engine not running"

    # Other methods
    assert car.honk() == "Beep beep!"
    assert car.describe() == "Toyota Hilux with 200hp diesel engine"

    # __repr__
    assert (
        repr(car)
        == "Car(make='Toyota', model='Hilux', engine=Engine(horsepower=200, fuel_type='diesel'))"
    )


def test_composition_benefits():
    # Same engine can be inspected independently
    engine = Engine(300, "gasoline")
    car = Car("Ford", "Mustang", engine)

    # Engine state accessible both ways
    car.start()
    assert engine.is_running is True
    assert car.engine.is_running is True

    # Could theoretically swap engines (not required, just demonstrating concept)
    # This is why composition > inheritance for this relationship
