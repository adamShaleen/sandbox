# ============================================================================
# PHASE 9: Type System Deep Dive - PROBLEMS
# ============================================================================

from __future__ import annotations

from typing import TypeVar, Sequence, Protocol, TypedDict, Literal, Final, overload
from typing_extensions import TypeGuard
from dataclasses import dataclass, field


# ----------------------------------------------------------------------------
# Problem 1 — Annotate a utility function
# ----------------------------------------------------------------------------
# Annotate `clamp` so mypy/pyright would be happy.
# `clamp(value, min_val, max_val)` — clamps value between min and max.
#
# All args and return are numeric. Use `int | float` (or just `float` —
# in Python, int is a subtype of float for type-checking purposes).
#
# JS/TS hint:
#   function clamp(value: number, min: number, max: number): number { ... }
#
# After you write it, also annotate a variable that holds the result.


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


def test_clamp():
    assert clamp(5, 1, 10) == 5
    assert clamp(-3, 0, 100) == 0
    assert clamp(200, 0, 100) == 100
    result: float
    result = clamp(7, 0, 10)
    assert result == 7


# ----------------------------------------------------------------------------
# Problem 2 — Write a generic `last` function
# ----------------------------------------------------------------------------
# `last(items)` returns the last element of any sequence.
# It should work on list[int], list[str], tuple, etc. — and the return type
# should match the element type of whatever was passed in.
#
# If the sequence is empty, raise a ValueError with a descriptive message.
#
# JS/TS hint:
#   function last<T>(items: T[]): T { ... }
#
# You'll need a TypeVar. Define it at module level (above the function),
# following the convention from the lesson.

T = TypeVar("T")


def last(items: Sequence[T]) -> T:
    if not items:
        raise ValueError("items cannot be empty")

    return items[-1]


def test_last():
    assert last([1, 2, 3]) == 3
    assert last(["a", "b", "c"]) == "c"
    assert last((10, 20)) == 20

    import pytest

    with pytest.raises(ValueError):
        last([])


# ----------------------------------------------------------------------------
# Problem 3 — Define a Protocol and write a function that uses it
# ----------------------------------------------------------------------------
# You're building a small reporting system. Different objects can be "reportable"
# if they have a `summary() -> str` method.
#
# Tasks:
#   1. Define a `Reportable` Protocol with a single method: `summary() -> str`
#   2. Write two classes — `Sale` and `Refund` — that satisfy it (no inheritance)
#      - Sale(amount: float): summary returns "Sale: $<amount>"
#      - Refund(amount: float, reason: str): summary returns "Refund: $<amount> (<reason>)"
#   3. Write `generate_report(items: list[Reportable]) -> list[str]` that returns
#      a list of each item's summary
#
# JS/TS hint:
#   interface Reportable { summary(): string }
#   class Sale implements Reportable { ... }  ← Python needs no `implements`


class Reportable(Protocol):
    def summary(self) -> str: ...


class Sale:
    def __init__(self, amount: float) -> None:
        self.amount = amount

    def summary(self) -> str:
        return f"Sale: ${self.amount}"


class Refund:
    def __init__(self, amount: float, reason: str) -> None:
        self.amount = amount
        self.reason = reason

    def summary(self) -> str:
        return f"Refund: ${self.amount} ({self.reason})"


def generate_report(items: list[Reportable]) -> list[str]:
    return [item.summary() for item in items]


def test_reportable():
    sales = [
        Sale(amount=99.99),
        Refund(amount=19.99, reason="damaged"),
        Sale(amount=49.00),
    ]
    report = generate_report(sales)
    assert report == [
        "Sale: $99.99",
        "Refund: $19.99 (damaged)",
        "Sale: $49.0",
    ]


# ----------------------------------------------------------------------------
# Problem 4 — Model a todo list with dataclasses
# ----------------------------------------------------------------------------
# A todo app needs two types: a single task and a todo list.
#
# `Task` — a dataclass with:
#   - title: str
#   - done: bool, defaults to False
#   - tags: list[str], defaults to empty list (watch the mutable default gotcha)
#
# `TodoList` — a dataclass with:
#   - items: list[Task], defaults to empty list
#   - Two regular methods (not generated — you write these):
#       add(self, task: Task) -> None       appends task to items
#       pending(self) -> list[Task]         returns tasks where done is False
#
# JS/TS hint:
#   interface Task { title: string; done: boolean; tags: string[] }
#   class TodoList { items: Task[] = []; add(t: Task) { ... }; pending() { ... } }


@dataclass
class Task:
    title: str
    done: bool = False
    tags: list[str] = field(default_factory=list)


@dataclass
class TodoList:
    items: list[Task] = field(default_factory=list)

    def add(self, task: Task) -> None:
        self.items.append(task)

    def pending(self) -> list[Task]:
        return [task for task in self.items if not task.done]


def test_todo():
    t1 = Task(title="buy milk")
    t2 = Task(title="write tests", done=True, tags=["dev"])
    t3 = Task(title="read docs", tags=["dev", "learning"])

    # dataclass __eq__ works on field values
    assert t1 == Task(title="buy milk")
    assert t1.done is False
    assert t1.tags == []

    # mutable default isolation — t1 and t3 must not share a list
    t1.tags.append("personal")
    assert t3.tags == ["dev", "learning"]

    todo = TodoList()
    todo.add(t1)
    todo.add(t2)
    todo.add(t3)

    assert len(todo.items) == 3
    assert todo.pending() == [t1, t3]  # t2 is done


# ----------------------------------------------------------------------------
# Problem 5 — Type an API response with TypedDict
# ----------------------------------------------------------------------------
# You're consuming a REST API that returns JSON shaped like this:
#
#   {
#     "id": 42,
#     "username": "ada",
#     "email": "ada@example.com",
#     "bio": "hello"          ← optional, may be missing
#   }
#
# Tasks:
#   1. Define a `UserBase` TypedDict with required keys: id (int), username (str), email (str)
#   2. Define a `User` TypedDict that extends UserBase with one optional key: bio (str)
#      Hint: use the total=False inheritance pattern from the lesson
#   3. Write `display_user(user: User) -> str` that returns:
#        "ada <ada@example.com> — hello"   if bio is present
#        "ada <ada@example.com>"           if bio is missing
#
# JS/TS hint:
#   type UserBase = { id: number; username: string; email: string }
#   type User = UserBase & { bio?: string }


class UserBase(TypedDict):
    id: int
    username: str
    email: str


class User(UserBase, total=False):
    bio: str


def display_user(user: User) -> str:
    output = f"{user['username']} <{user['email']}>"
    bio = user.get("bio")

    if bio:
        return output + f" — {bio}"

    return output


def test_user_typeddict():
    u1: User = {"id": 1, "username": "ada", "email": "ada@example.com", "bio": "hello"}
    u2: User = {"id": 2, "username": "bob", "email": "bob@example.com"}

    assert display_user(u1) == "ada <ada@example.com> — hello"
    assert display_user(u2) == "bob <bob@example.com>"

    # still a plain dict at runtime
    assert isinstance(u1, dict)


# ----------------------------------------------------------------------------
# Problem 6 — Traffic light with Literal & Final
# ----------------------------------------------------------------------------
# You're modeling a traffic light system.
#
# Tasks:
#   1. Define a `LightState` type alias using Literal for the three valid states:
#      "red", "yellow", "green"
#
#   2. Define two Final constants:
#      - DEFAULT_STATE: the light starts on "red"
#      - CYCLE: a tuple of the states in order — ("red", "green", "yellow")
#        (in traffic lights: red → green → yellow → red)
#
#   3. Write `next_state(current: LightState) -> LightState` — returns the next
#      state in the cycle. Given "red" → "green", "green" → "yellow", "yellow" → "red"
#      Hint: use CYCLE and its index to find the next state

LightState = Literal["red", "yellow", "green"]

DEFAULT_STATE: Final = "red"
CYCLE: Final = ("red", "green", "yellow")


def next_state(current: LightState) -> LightState:
    return CYCLE[(CYCLE.index(current) + 1) % len(CYCLE)]


def test_traffic_light():
    assert DEFAULT_STATE == "red"
    assert next_state("red") == "green"
    assert next_state("green") == "yellow"
    assert next_state("yellow") == "red"

    # full cycle starting from default
    state: LightState = DEFAULT_STATE
    states = [state]
    for _ in range(3):
        state = next_state(state)
        states.append(state)
    assert states == ["red", "green", "yellow", "red"]


# ----------------------------------------------------------------------------
# Problem 7 — Overloaded `stringify`
# ----------------------------------------------------------------------------
# Write a `stringify` function that converts a value to a string, but with
# type-specific behaviour:
#   - int   → zero-padded to 5 digits:  42 → "00042"
#   - float → 2 decimal places:         3.14159 → "3.14"
#   - bool  → "yes" or "no":            True → "yes"
#
# The type checker should know:
#   stringify(42)     → str
#   stringify(3.14)   → str
#   stringify(True)   → str
#
# Use @overload to declare all three signatures, then implement the real function.
#
# Important Python gotcha: bool is a subclass of int, so isinstance(x, int)
# will match bools too. Check for bool BEFORE int in your implementation.
#
# JS/TS hint:
#   function stringify(x: number): string
#   function stringify(x: boolean): string


@overload
def stringify(value: int) -> str: ...


@overload
def stringify(value: float) -> str: ...


@overload
def stringify(value: bool) -> str: ...


def stringify(value: int | float | bool) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"

    if isinstance(value, int):
        return f"{value:05d}"

    return f"{value:.2f}"


def test_stringify():
    assert stringify(42) == "00042"
    assert stringify(0) == "00000"
    assert stringify(3.14159) == "3.14"
    assert stringify(1.0) == "1.00"
    assert stringify(True) == "yes"
    assert stringify(False) == "no"


# ----------------------------------------------------------------------------
# Problem 8 — TypeGuard for a mixed list
# ----------------------------------------------------------------------------
# You're processing a list of values from an untrusted source — it could
# contain ints, strings, None, or anything else.
#
# Tasks:
#   1. Write `is_int_list(val: list[object]) -> TypeGuard[list[int]]`
#      Returns True only if every element is an int (and NOT a bool —
#      remember bool is a subclass of int, so exclude bools explicitly).
#
#   2. Write `sum_if_ints(val: list[object]) -> int | None`
#      - If val passes the TypeGuard, return the sum of the list
#      - Otherwise return None
#      Inside the True branch, the checker should know val is list[int].
#
# JS/TS hint:
#   function isIntList(val: unknown[]): val is number[] { ... }


def is_int_list(values: list[object]) -> TypeGuard[list[int]]:
    return all(
        isinstance(value, int) and not isinstance(value, bool) for value in values
    )


def sum_if_ints(values: list[object]) -> int | None:
    if is_int_list(values):
        return sum(values)
    return None


def test_int_list_guard():
    assert is_int_list([1, 2, 3]) is True
    assert is_int_list([]) is True
    assert is_int_list([1, "two", 3]) is False
    assert is_int_list([1, None, 3]) is False
    assert is_int_list([True, False]) is False  # bools excluded

    assert sum_if_ints([1, 2, 3]) == 6
    assert sum_if_ints([1, "x"]) is None
    assert sum_if_ints([]) == 0
