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
