# ============================================================================
# PHASE 9: Type System Deep Dive - LESSONS
# ============================================================================
# Python's type system goes far beyond basic annotations.
# Coming from TS, many concepts will feel familiar — with Pythonic twists.
#
# Concepts covered:
#   1. Basic annotations & `from __future__ import annotations`
#   2. TypeVar & generics
#   3. Protocol (structural subtyping — like TS interfaces)
#   4. dataclass (typed value objects)
#   5. TypedDict (typed dicts — like TS object types)
#   6. Literal & Final
#   7. overload (@overload for multiple signatures)
#   8. TypeGuard & runtime narrowing

from __future__ import annotations

from typing import TypeVar, Sequence, Protocol, TypedDict, Literal, Final, overload
from typing_extensions import (
    TypeGuard,
)  # TypeGuard added to `typing` in 3.10; use typing_extensions on 3.9
from dataclasses import dataclass, field


# -----------------------------------------------------------------------------
# 1. BASIC ANNOTATIONS & `from __future__ import annotations`
# -----------------------------------------------------------------------------
# Python type annotations are hints — NOT enforced at runtime by default.
# Tools like mypy, pyright, or your IDE use them for static analysis.
#
# JS/TS comparison:
#   TS:  function greet(name: string): string { ... }
#   Py:  def greet(name: str) -> str: ...
#
# Union types:
#   TS:  string | number
#   Py:  Union[str, int]   (old style, Python < 3.10)
#   Py:  str | int         (new style, Python 3.10+)
#
# Optional (can be None):
#   TS:  string | undefined  or  string?
#   Py:  Optional[str]       === Union[str, None]
#   Py:  str | None          (Python 3.10+ shorthand)
#
# `from __future__ import annotations` (at top of file):
#   - Makes ALL annotations lazy strings — not evaluated at import time
#   - Lets you use new-style `str | None` syntax even on Python 3.9
#   - Lets you forward-reference your own types before they're defined
#   - Best practice: include it in every typed file
#
# Variable annotations:
#   x: int = 5
#   name: str          # declared but not assigned (type checker sees it)
#
# Collections:
#   TS:  string[]    or  Array<string>
#   Py:  list[str]                      (Python 3.9+)
#   Py:  dict[str, int]
#   Py:  tuple[int, str, float]         # fixed-length, heterogeneous
#   Py:  tuple[int, ...]                # variable-length, homogeneous


def add(a: int, b: int) -> int:
    return a + b


def first_or_default(items: list[str], default: str | None = None) -> str | None:
    return items[0] if items else default


def demo_basic_annotations() -> None:
    result: int = add(1, 2)
    names: list[str] = ["alice", "bob"]
    found: str | None = first_or_default(names)
    empty: str | None = first_or_default([], default="fallback")
    print(result, found, empty)


def test_basic_annotations() -> None:
    assert add(2, 3) == 5
    assert first_or_default(["a", "b"]) == "a"
    assert first_or_default([]) is None
    assert first_or_default([], default="x") == "x"


# -----------------------------------------------------------------------------
# 2. TypeVar & GENERICS
# -----------------------------------------------------------------------------
# A TypeVar is a placeholder for a type that gets filled in at the call site.
# It lets you write one function that works on multiple types while still
# preserving type safety — the return type stays linked to the input type.
#
# JS/TS comparison:
#   TS:  function identity<T>(value: T): T { return value }
#   Py:  T = TypeVar("T")
#        def identity(value: T) -> T: return value
#
# Without TypeVar, you'd write `def identity(value: object) -> object` —
# which loses the specific type. The caller gets back `object`, not `str`.
# TypeVar keeps the relationship: in str → out str, in int → out int.
#
# Naming convention: single uppercase letter (T, U, V) or descriptive
# (KT for key type, VT for value type, etc.).
#
# Constraints — restrict what types T can be:
#   T = TypeVar("T", int, float)   # T can only be int or float
#
# Bound — restrict T to a type or its subclasses:
#   T = TypeVar("T", bound=str)    # T must be str or a subclass of str
#
# Sequence — from typing, represents any ordered collection (list, tuple, str).
# Useful when you want "anything you can iterate and index" without locking to list.
#
# Generic classes:
#   class Stack(Generic[T]):       # T is the element type
#       def push(self, item: T) -> None: ...
#       def pop(self) -> T: ...
#
# In Python 3.12+, there's new syntax: `def fn[T](x: T) -> T`
# We're on 3.9, so we use the TypeVar form.

T = TypeVar("T")


def first(items: Sequence[T]) -> T:
    # Sequence[T] accepts list[T], tuple[T, ...], str, etc.
    # The return type T matches the element type of whatever was passed in.
    if not items:
        raise ValueError("sequence is empty")
    return items[0]


def demo_typevar() -> None:
    n: int = first([10, 20, 30])  # T inferred as int → returns int
    s: str = first(["a", "b", "c"])  # T inferred as str → returns str
    print(n, s)


def test_typevar() -> None:
    assert first([1, 2, 3]) == 1
    assert first(["x", "y"]) == "x"
    assert first((True, False)) is True  # tuple works too — it's a Sequence


# -----------------------------------------------------------------------------
# 3. Protocol (STRUCTURAL SUBTYPING)
# -----------------------------------------------------------------------------
# A Protocol defines a set of methods/attributes a type must have.
# Any class that has those methods satisfies the Protocol — no inheritance,
# no registration. This is called "structural subtyping" or "duck typing"
# made explicit for the type checker.
#
# JS/TS comparison:
#   TS:  interface Printable { print(): void }
#        function render(item: Printable) { item.print() }
#        // Any object with .print() satisfies Printable — no `implements` needed
#
#   Py:  class Printable(Protocol):
#            def print(self) -> None: ...
#        def render(item: Printable) -> None: item.print()
#        # Any class with .print() satisfies Printable — no subclassing needed
#
# Key difference from ABC (Abstract Base Class):
#   ABC requires explicit inheritance: class Dog(Animal)
#   Protocol requires nothing — if the shape fits, it passes. This is why
#   it's called "structural" — the structure matters, not the class hierarchy.
#
# Protocol methods use `...` as the body (ellipsis) — they're just signatures.
#
# runtime_checkable:
#   By default, Protocol checks are static only (type checker, not isinstance).
#   Add @runtime_checkable to also allow isinstance(obj, MyProtocol) at runtime.
#   Note: runtime checks only verify attribute existence, not signatures.
#
# When to use Protocol vs ABC:
#   Protocol — you don't control the classes (third-party, built-ins)
#   ABC      — you own the class hierarchy and want enforced inheritance


class Describable(Protocol):
    def describe(self) -> str: ...  # just a signature — no implementation


class Cat:
    def describe(self) -> str:
        return "I am a cat"


class Car:
    def describe(self) -> str:
        return "I am a car"


class Rock:
    pass  # no describe() — does NOT satisfy Describable


def print_description(item: Describable) -> str:
    # type checker accepts Cat and Car here, rejects Rock
    return item.describe()


def demo_protocol() -> None:
    print(print_description(Cat()))
    print(print_description(Car()))
    # print_description(Rock())  # type error — Rock has no describe()


def test_protocol() -> None:
    assert print_description(Cat()) == "I am a cat"
    assert print_description(Car()) == "I am a car"
    # Both work despite Cat and Car having no common base class


# -----------------------------------------------------------------------------
# 4. dataclass
# -----------------------------------------------------------------------------
# A dataclass is a regular class where Python auto-generates boilerplate:
# __init__, __repr__, and __eq__ — based on annotated fields.
#
# JS/TS comparison:
#   TS:  interface Point { x: number; y: number }
#        // or
#        class Point { constructor(public x: number, public y: number) {} }
#
#   Py:  @dataclass
#        class Point:
#            x: float
#            y: float
#        # Python generates __init__(self, x, y), __repr__, __eq__ for you
#
# Without @dataclass you'd write:
#   class Point:
#       def __init__(self, x: float, y: float) -> None:
#           self.x = x
#           self.y = y
#       def __repr__(self): return f"Point(x={self.x}, y={self.y})"
#       def __eq__(self, other): return self.x == other.x and self.y == other.y
#
# @dataclass gives you all of that for free.
#
# Default values:
#   x: float = 0.0          # simple default
#   tags: list = field(default_factory=list)  # mutable default — MUST use field()
#   # Never use `tags: list = []` — that shares one list across all instances
#
# frozen=True — makes the instance immutable (like TS `readonly`):
#   @dataclass(frozen=True)
#   class Point: ...
#   # p.x = 5  → raises FrozenInstanceError
#
# order=True — auto-generates __lt__, __le__, __gt__, __ge__ for sorting:
#   @dataclass(order=True)
#   class Point: ...
#   # sorted([Point(3,1), Point(1,2)]) works — compares field by field
#
# field() options:
#   field(default=0)                 — explicit default value
#   field(default_factory=list)      — callable to produce default
#   field(repr=False)                — exclude from __repr__
#   field(compare=False)             — exclude from __eq__ / ordering


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Player:
    name: str
    score: int = 0  # simple default
    inventory: list[str] = field(default_factory=list)  # mutable default


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int


def demo_dataclass() -> None:
    p = Point(1.0, 2.0)
    print(p)  # Point(x=1.0, y=2.0) — __repr__ auto-generated
    print(p == Point(1.0, 2.0))  # True — __eq__ auto-generated

    player = Player("ada")
    player.inventory.append("sword")
    print(player)  # Player(name='ada', score=0, inventory=['sword'])

    # red = Color(255, 0, 0)
    # red.r = 100  # would raise FrozenInstanceError


def test_dataclass() -> None:
    # __init__ generated from field annotations
    p = Point(3.0, 4.0)
    assert p.x == 3.0
    assert p.y == 4.0

    # __eq__ compares field values, not identity
    assert Point(1.0, 2.0) == Point(1.0, 2.0)
    assert Point(1.0, 2.0) != Point(9.0, 2.0)

    # __repr__ includes field names and values
    assert repr(p) == "Point(x=3.0, y=4.0)"

    # default values
    player = Player("ada")
    assert player.score == 0
    assert player.inventory == []

    # mutable default — each instance gets its own list
    p1, p2 = Player("ada"), Player("bob")
    p1.inventory.append("sword")
    assert p2.inventory == []  # p2 unaffected

    # frozen — immutable
    color = Color(255, 0, 0)
    assert color.r == 255
    import pytest

    with pytest.raises(Exception):  # FrozenInstanceError (subclass of AttributeError)
        color.r = 100  # type: ignore


# -----------------------------------------------------------------------------
# 5. TypedDict
# -----------------------------------------------------------------------------
# TypedDict lets you annotate the shape of a plain dict — keys and value types.
# At runtime it's still a normal dict; the types are for the static checker only.
#
# JS/TS comparison:
#   TS:  type User = { id: number; name: string; active: boolean }
#        const u: User = { id: 1, name: "ada", active: true }
#
#   Py:  class User(TypedDict):
#            id: int
#            name: str
#            active: bool
#        u: User = {"id": 1, "name": "ada", "active": True}
#
# Why TypedDict instead of dataclass?
#   - You're working with JSON from an API — it comes back as a dict, not an object
#   - You need dict behaviour (json.dumps, dict unpacking, **kwargs passing)
#   - You don't control the shape (third-party data) but want type safety
#   dataclass  → when you want an object with methods
#   TypedDict  → when you want a typed dict (serialization, JSON, configs)
#
# Optional keys with total=False:
#   class Movie(TypedDict, total=False):   # ALL keys optional
#       title: str
#       year: int
#
# Mix required and optional by inheriting:
#   class MovieBase(TypedDict):            # required keys
#       title: str
#   class Movie(MovieBase, total=False):   # optional keys
#       year: int
#       rating: float
#
# At runtime, TypedDict IS just a dict — isinstance(u, dict) is True.
# No validation happens automatically — use a library like pydantic for that.


class UserDict(TypedDict):
    id: int
    name: str
    active: bool


class MovieBase(TypedDict):
    title: str


class Movie(MovieBase, total=False):
    year: int
    rating: float


def format_user(user: UserDict) -> str:
    status = "active" if user["active"] else "inactive"
    return f"{user['name']} ({status})"


def demo_typeddict() -> None:
    u: UserDict = {"id": 1, "name": "ada", "active": True}
    print(format_user(u))

    m: Movie = {"title": "Dune"}  # year and rating are optional
    m2: Movie = {"title": "Dune", "year": 2021, "rating": 8.0}
    print(m, m2)


def test_typeddict() -> None:
    u: UserDict = {"id": 1, "name": "ada", "active": True}
    assert format_user(u) == "ada (active)"

    u2: UserDict = {"id": 2, "name": "bob", "active": False}
    assert format_user(u2) == "bob (inactive)"

    # It's still a plain dict at runtime
    assert isinstance(u, dict)
    assert u["id"] == 1

    # Optional keys — title required, rest optional
    m: Movie = {"title": "Dune"}
    assert m["title"] == "Dune"
    assert "year" not in m


# -----------------------------------------------------------------------------
# 6. Literal & Final
# -----------------------------------------------------------------------------
# Literal — restricts a type to a specific set of values.
# Final   — marks a variable as a constant that must not be reassigned.
#
# JS/TS comparison:
#   TS:  type Direction = "north" | "south" | "east" | "west"
#   Py:  Direction = Literal["north", "south", "east", "west"]
#
#   TS:  const MAX_RETRIES = 3   (const prevents reassignment)
#   Py:  MAX_RETRIES: Final = 3  (Final prevents reassignment — type checker only)
#
# Literal is useful for:
#   - Function params that only accept specific strings or ints
#   - Replacing stringly-typed APIs with something the type checker understands
#   - Narrowing return types ("success" | "error" instead of plain str)
#
# Final is useful for:
#   - Module-level constants (API keys, config values, limits)
#   - Class attributes that must not be overridden
#   - Communicating intent clearly — "this is not meant to change"
#
# Note: Final does NOT make the value immutable at runtime.
#   Final[list] = []  — the list contents can still be mutated.
#   Final prevents *reassignment* of the variable name, not mutation of the object.
#
# Combining them:
#   DEFAULT_DIR: Final = Literal["north"]   # rarely needed — usually one or the other
#
# Literal with functions:
#   def move(direction: Literal["north", "south", "east", "west"]) -> None: ...
#   move("north")   # OK
#   move("up")      # type error — "up" not in the Literal


Direction = Literal["north", "south", "east", "west"]

MAX_SPEED: Final = 120
APP_NAME: Final[str] = "myapp"


def move(direction: Direction) -> str:
    # type checker rejects any string not in the Literal
    return f"moving {direction}"


def demo_literal_final() -> None:
    print(move("north"))  # OK
    # move("up")           # type error — caught by checker, not at runtime
    print(MAX_SPEED)


def test_literal_final() -> None:
    assert move("north") == "moving north"
    assert move("south") == "moving south"
    assert move("east") == "moving east"
    assert move("west") == "moving west"

    # Final values are accessible normally
    assert MAX_SPEED == 120
    assert APP_NAME == "myapp"


# -----------------------------------------------------------------------------
# 7. @overload
# -----------------------------------------------------------------------------
# @overload lets you declare multiple type signatures for a single function —
# so the type checker knows the return type depends on the input type.
#
# JS/TS comparison:
#   TS:  function double(x: number): number
#        function double(x: string): string
#        function double(x: number | string): number | string { ... }
#
#   Py:  @overload
#        def double(x: int) -> int: ...
#        @overload
#        def double(x: str) -> str: ...
#        def double(x: int | str) -> int | str:   # real implementation
#            ...
#
# Why bother? Without @overload, you'd write:
#   def double(x: int | str) -> int | str: ...
# But then the checker doesn't know that int → int and str → str.
# The caller gets back `int | str` even when they passed an `int`.
# @overload narrows the return type based on what was passed in.
#
# Rules:
#   1. All @overload signatures come FIRST — bodies are just `...`
#   2. The real implementation comes LAST — no @overload decorator
#   3. The real implementation is NOT visible to the type checker —
#      only the @overload signatures are used for type inference
#   4. The real implementation must handle all cases the overloads declare
#
# When to use @overload vs TypeVar:
#   TypeVar  — when input and output are the same type (identity-like)
#   @overload — when different input types produce different output types


@overload
def double(x: int) -> int: ...


@overload
def double(x: str) -> str: ...


def double(x: int | str) -> int | str:
    if isinstance(x, int):
        return x * 2
    return x + x  # string repetition


def demo_overload() -> None:
    n: int = double(5)  # checker knows this is int
    s: str = double("ha")  # checker knows this is str
    print(n, s)


def test_overload() -> None:
    assert double(5) == 10
    assert double("ha") == "haha"
    assert double(0) == 0
    assert double("") == ""


# -----------------------------------------------------------------------------
# 8. TypeGuard & RUNTIME NARROWING
# -----------------------------------------------------------------------------
# Type narrowing is when the type checker refines a broad type to a narrower
# one based on a condition. Python does this automatically with isinstance(),
# but TypeGuard lets you teach the checker to narrow through your own functions.
#
# JS/TS comparison:
#   TS:  function isString(x: unknown): x is string { return typeof x === "string" }
#        if (isString(val)) { val.toUpperCase() }  // TS knows val is string here
#
#   Py:  def is_string(x: object) -> TypeGuard[str]:
#            return isinstance(x, str)
#        if is_string(val):
#            val.upper()  # checker knows val is str here
#
# Without TypeGuard:
#   def is_string(x: object) -> bool: ...
#   if is_string(val):
#       val.upper()   # type error — checker still thinks val is `object`
#
# With TypeGuard[str]:
#   The return type tells the checker: "if this returns True, the argument is str"
#
# Automatic narrowing (no TypeGuard needed):
#   The checker already narrows automatically for isinstance(), is None checks,
#   and equality checks. TypeGuard is only needed for custom predicate functions.
#
#   x: int | str
#   if isinstance(x, int):
#       x + 1       # checker knows x is int here — no TypeGuard needed
#
# TypeGuard is one-directional:
#   True branch → narrowed to TypeGuard[T]
#   False branch → NOT narrowed (still the original type)
#   This differs from TS where both branches can be narrowed.


def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    # Returns True only if every element is a string.
    # TypeGuard[list[str]] tells the checker: if True, treat val as list[str].
    return all(isinstance(x, str) for x in val)


def demo_typeguard() -> None:
    items: list[object] = ["a", "b", "c"]
    if is_str_list(items):
        # checker knows items is list[str] here — .upper() is valid
        print([s.upper() for s in items])


def test_typeguard() -> None:
    assert is_str_list(["a", "b", "c"]) is True
    assert is_str_list([1, 2, 3]) is False
    assert is_str_list(["a", 1, "c"]) is False
    assert is_str_list([]) is True  # vacuously true — all() on empty is True

    # narrowing in action
    mixed: list[object] = ["x", "y"]
    if is_str_list(mixed):
        result = [s.upper() for s in mixed]  # checker allows .upper() here
        assert result == ["X", "Y"]
