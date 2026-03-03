# ============================================================================
# PHASE 10: Pythonic Idioms & Capstone - LESSONS
# ============================================================================
# Writing Python that feels like Python, not translated JavaScript.
# These patterns come up constantly in real codebases.
#
# Concepts covered:
#   1. Unpacking & starred assignment
#   2. Comprehension patterns (dict, set, nested)
#   3. collections module (Counter, defaultdict, deque, namedtuple)
#   4. itertools (chain, islice, groupby, product, zip_longest)
#   5. Context manager protocol (__enter__ / __exit__, contextlib)
#   6. Dunder methods (__len__, __contains__, __iter__, __getitem__)
#   7. Capstone — bring it all together

from __future__ import annotations

from collections import Counter, defaultdict, deque, namedtuple
import itertools
from contextlib import contextmanager


# -----------------------------------------------------------------------------
# 1. UNPACKING & STARRED ASSIGNMENT
# -----------------------------------------------------------------------------
# Python lets you unpack any iterable into variables in one line.
# The starred (*) operator soaks up "the rest" into a list.
#
# JS/TS comparison:
#   TS:  const [first, ...rest] = arr
#   Py:  first, *rest = arr          # same idea, no const/let needed
#
#   TS:  const [a, b] = [1, 2]
#   Py:  a, b = 1, 2                 # tuple unpacking — no brackets needed
#
# Swap without a temp variable:
#   Py:  a, b = b, a                 # right side is a tuple, unpacked into left
#
# Nested unpacking:
#   (x, y), z = (1, 2), 3           # works on any nested iterable
#
# Starred in the middle:
#   first, *middle, last = [1,2,3,4,5]
#
# Common use — ignoring values with _:
#   first, *_, last = some_list     # _ is convention for "don't care"
#
# Function return unpacking:
#   def minmax(lst): return min(lst), max(lst)
#   lo, hi = minmax([3,1,4,1,5])


def demo_unpacking() -> None:
    first, *rest = [1, 2, 3, 4, 5]
    print(first, rest)  # 1  [2, 3, 4, 5]

    first, *middle, last = [1, 2, 3, 4, 5]
    print(first, middle, last)  # 1  [2, 3, 4]  5

    a, b = 10, 20
    a, b = b, a  # swap — no temp variable needed
    print(a, b)  # 20  10

    (x, y), z = (1, 2), 3
    print(x, y, z)  # 1  2  3


def test_unpacking() -> None:
    first, *rest = [10, 20, 30, 40]
    assert first == 10
    assert rest == [20, 30, 40]

    head, *_, tail = [1, 2, 3, 4, 5]
    assert head == 1
    assert tail == 5

    a, b = 1, 2
    a, b = b, a
    assert a == 2 and b == 1

    (x, y), z = (7, 8), 9
    assert x == 7 and y == 8 and z == 9


# -----------------------------------------------------------------------------
# 2. COMPREHENSION PATTERNS
# -----------------------------------------------------------------------------
# You've seen list comprehensions. Python also has dict and set comprehensions,
# and they follow the same pattern.
#
# JS/TS comparison:
#   TS:  arr.filter(x => x > 0).map(x => x * 2)
#   Py:  [x * 2 for x in arr if x > 0]          # list comprehension
#
#   TS:  Object.fromEntries(pairs.map(([k, v]) => [k, v * 2]))
#   Py:  {k: v * 2 for k, v in pairs}            # dict comprehension
#
#   TS:  new Set(arr.map(x => x.lower()))
#   Py:  {x.lower() for x in arr}                # set comprehension (no colon)
#
# Nested comprehensions — flatten a 2D list:
#   Py:  [x for row in matrix for x in row]
#   Read left to right: "for each row, for each x in that row, give me x"
#   This is equivalent to two nested for-loops, outer loop first.
#
# Conditional expression (ternary) inside comprehension:
#   [x if x > 0 else 0 for x in nums]   # clamp negatives to 0
#   Note: `if` AFTER `for` is a filter; `if/else` BEFORE `for` is a ternary
#
# When NOT to use comprehensions:
#   - More than two clauses → use a regular loop (readability suffers)
#   - Side effects (printing, appending to external list) → use a loop
#   - When you need early exit (break) → use a loop


def demo_comprehensions() -> None:
    nums = [1, -2, 3, -4, 5]

    # list — filter and transform
    positives = [x for x in nums if x > 0]  # [1, 3, 5]

    # list — ternary (no filter, just transform)
    clamped = [x if x > 0 else 0 for x in nums]  # [1, 0, 3, 0, 5]

    # dict comprehension
    squared = {x: x**2 for x in range(5)}  # {0:0, 1:1, 2:4, 3:9, 4:16}

    # set comprehension — duplicates removed automatically
    words = ["hello", "world", "Hello", "WORLD"]
    unique_lower = {w.lower() for w in words}  # {"hello", "world"}

    # nested — flatten 2D list
    matrix = [[1, 2], [3, 4], [5, 6]]
    flat = [x for row in matrix for x in row]  # [1, 2, 3, 4, 5, 6]

    print(positives, clamped, squared, unique_lower, flat)


def test_comprehensions() -> None:
    nums = [1, -2, 3, -4, 5]

    assert [x for x in nums if x > 0] == [1, 3, 5]
    assert [x if x > 0 else 0 for x in nums] == [1, 0, 3, 0, 5]

    pairs = [("a", 1), ("b", 2), ("c", 3)]
    assert {k: v * 10 for k, v in pairs} == {"a": 10, "b": 20, "c": 30}

    words = ["hi", "HI", "Hi"]
    assert {w.lower() for w in words} == {"hi"}  # all the same after lower()

    matrix = [[1, 2], [3, 4]]
    assert [x for row in matrix for x in row] == [1, 2, 3, 4]


# -----------------------------------------------------------------------------
# 3. collections MODULE
# -----------------------------------------------------------------------------
# The `collections` module has specialized container types that replace common
# patterns you'd otherwise write by hand.
#
# Four most useful ones:
#
# Counter — counts occurrences of elements in an iterable.
#   JS equivalent: arr.reduce((acc, x) => ({...acc, [x]: (acc[x]||0)+1}), {})
#   Counter("aabbc")          → Counter({'a':2,'b':2,'c':1})
#   counter.most_common(2)    → [('a',2), ('b',2)]  — top N by count
#   Counters support +, -, & (intersection), | (union) arithmetic
#
# defaultdict — a dict that auto-creates a default value for missing keys.
#   JS equivalent: map.get(key) ?? []  (but you still have to set it back)
#   defaultdict(list)  — missing key → []
#   defaultdict(int)   — missing key → 0
#   defaultdict(set)   — missing key → set()
#   No KeyError on missing keys — just creates the default and returns it.
#
# deque — double-ended queue. O(1) append/pop from both ends.
#   JS equivalent: array, but .shift() is O(n) in JS; deque.popleft() is O(1)
#   Use when you need a queue (FIFO) or need to pop from the left efficiently.
#   deque(maxlen=N) — fixed-size sliding window; oldest item auto-dropped.
#
# namedtuple — a tuple with named fields. Immutable, memory-efficient.
#   JS equivalent: a frozen object literal, or a simple interface
#   Lighter than a dataclass — no methods, no mutability, no overhead.
#   Good for simple value objects that don't need methods.
#   Point = namedtuple("Point", ["x", "y"])
#   p = Point(1, 2); p.x == 1; p[0] == 1  — accessible by name OR index


def demo_collections() -> None:
    # Counter
    votes = ["alice", "bob", "alice", "carol", "bob", "alice"]
    tally = Counter(votes)
    print(tally.most_common(1))  # [('alice', 3)]

    # defaultdict
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for name, dept in [("ada", "eng"), ("bob", "eng"), ("carol", "hr")]:
        groups[dept].append(name)  # no KeyError — list created automatically
    print(dict(groups))  # {'eng': ['ada', 'bob'], 'hr': ['carol']}

    # deque as a sliding window (last 3 items)
    window: deque[int] = deque(maxlen=3)
    for n in range(6):
        window.append(n)
    print(list(window))  # [3, 4, 5] — oldest auto-dropped

    # namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(p.x, p.y, p[0])  # 3  4  3


def test_collections() -> None:
    # Counter
    c = Counter("mississippi")
    assert c["s"] == 4
    assert c["p"] == 2
    top_char, top_count = c.most_common(1)[0]
    assert top_count == 4  # 'i' and 's' both appear 4 times — either can be first

    # defaultdict
    dd: defaultdict[str, list[int]] = defaultdict(list)
    dd["a"].append(1)
    dd["a"].append(2)
    dd["b"].append(3)
    assert dd["a"] == [1, 2]
    assert dd["c"] == []  # missing key → empty list, no KeyError

    # deque
    dq: deque[int] = deque(maxlen=3)
    for i in [1, 2, 3, 4, 5]:
        dq.append(i)
    assert list(dq) == [3, 4, 5]
    dq.appendleft(99)
    assert list(dq) == [99, 3, 4]  # 5 dropped, 99 prepended

    # namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(10, 20)
    assert p.x == 10
    assert p[1] == 20  # index access still works
    assert p == Point(10, 20)  # equality by value


# -----------------------------------------------------------------------------
# 4. itertools
# -----------------------------------------------------------------------------
# itertools provides iterator-building blocks for common looping patterns.
# All functions return lazy iterators — nothing computed until you iterate.
#
# JS/TS comparison: no direct equivalent; closest is lodash or custom generators.
#
# Five most useful functions:
#
# chain(*iterables) — concatenates iterables without building a new list
#   JS: [...a, ...b, ...c]  but lazy
#   list(chain([1,2], [3,4], [5])) → [1, 2, 3, 4, 5]
#
# islice(iterable, stop) / islice(iterable, start, stop, step) — lazy slice
#   JS: arr.slice(0, n)  but works on any iterator, not just arrays
#   list(islice(range(100), 5)) → [0, 1, 2, 3, 4]
#
# groupby(iterable, key) — groups CONSECUTIVE elements by a key function
#   IMPORTANT: input must be sorted by the key first — groupby only groups
#   consecutive runs, not all matching elements across the whole iterable.
#   JS: _.groupBy(arr, fn)  but consecutive only
#
# product(*iterables) — cartesian product (all combinations)
#   JS: nested for-loops flattened
#   list(product([1,2], ['a','b'])) → [(1,'a'),(1,'b'),(2,'a'),(2,'b')]
#
# zip_longest(*iterables, fillvalue=None) — like zip but pads shorter iterables
#   JS: no built-in; zip stops at shortest, zip_longest pads to longest
#   list(zip_longest([1,2,3], ['a','b'], fillvalue=0)) → [(1,'a'),(2,'b'),(3,0)]


def demo_itertools() -> None:
    # chain — combine multiple iterables
    combined = list(itertools.chain([1, 2], [3, 4], [5]))
    print(combined)  # [1, 2, 3, 4, 5]

    # islice — take first N from any iterator
    first5 = list(itertools.islice(range(1000), 5))
    print(first5)  # [0, 1, 2, 3, 4]

    # groupby — must sort first
    words = ["ant", "ape", "bat", "bee", "cat"]
    for letter, group in itertools.groupby(words, key=lambda w: w[0]):
        print(letter, list(group))  # a [ant, ape]  b [bat, bee]  c [cat]

    # product — cartesian product
    combos = list(itertools.product([1, 2], ["a", "b"]))
    print(combos)  # [(1,'a'),(1,'b'),(2,'a'),(2,'b')]

    # zip_longest
    zipped = list(itertools.zip_longest([1, 2, 3], ["a", "b"], fillvalue=0))
    print(zipped)  # [(1,'a'),(2,'b'),(3,0)]


def test_itertools() -> None:
    # chain
    assert list(itertools.chain([1, 2], [3, 4])) == [1, 2, 3, 4]
    assert list(itertools.chain([], [1], [])) == [1]

    # islice
    assert list(itertools.islice(range(10), 4)) == [0, 1, 2, 3]
    assert list(itertools.islice(range(10), 2, 5)) == [2, 3, 4]

    # groupby — sort first
    data = sorted(["banana", "apple", "avocado", "blueberry"], key=lambda w: w[0])
    groups = {k: list(v) for k, v in itertools.groupby(data, key=lambda w: w[0])}
    assert groups == {"a": ["apple", "avocado"], "b": ["banana", "blueberry"]}

    # product
    assert list(itertools.product([0, 1], [0, 1])) == [(0, 0), (0, 1), (1, 0), (1, 1)]

    # zip_longest
    result = list(itertools.zip_longest([1, 2, 3], ["a"], fillvalue=None))
    assert result == [(1, "a"), (2, None), (3, None)]


# -----------------------------------------------------------------------------
# 5. CONTEXT MANAGER PROTOCOL
# -----------------------------------------------------------------------------
# A context manager is any object that implements __enter__ and __exit__.
# The `with` statement calls __enter__ on entry and __exit__ on exit —
# even if an exception is raised. This guarantees cleanup happens.
#
# You already used context managers in Phase 6 (open(), pytest.raises).
# Here we cover how to BUILD your own.
#
# JS/TS comparison:
#   No direct equivalent. Closest is try/finally:
#   try { doWork() } finally { cleanup() }
#   Context managers are Python's idiomatic way to express this pattern.
#
# Two ways to build a context manager:
#
# 1. Class-based — implement __enter__ and __exit__:
#   class MyCtx:
#       def __enter__(self): ...    # runs on `with` entry, return value → `as`
#       def __exit__(self, exc_type, exc_val, exc_tb):
#           ...                     # runs on exit, even on exception
#           return False            # False = don't suppress exceptions
#                                   # True  = suppress (swallow) the exception
#
# 2. Generator-based with @contextmanager (simpler for most cases):
#   @contextmanager
#   def my_ctx():
#       # setup
#       yield value    # body of `with` block runs here; value → `as`
#       # teardown     # runs after `with` block, even on exception
#
# The @contextmanager approach is usually preferred — less boilerplate.
# Use the class approach when you need to store state across multiple uses
# or implement a reusable library-style context manager.


# --- Class-based context manager ---


class Timer:
    """Measures elapsed time for a block of code."""

    def __enter__(self) -> Timer:
        import time

        self._start = time.monotonic()
        return self  # available as `as timer`

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        import time

        self.elapsed = time.monotonic() - self._start
        return False  # don't suppress exceptions


# --- Generator-based context manager ---


@contextmanager
def temp_value(d: dict, key: str, value: object):
    """Temporarily sets d[key] = value, restores original on exit."""
    old = d.get(key)
    d[key] = value
    try:
        yield d
    finally:
        if old is None:
            d.pop(key, None)
        else:
            d[key] = old


def demo_context_managers() -> None:
    with Timer() as t:
        total = sum(range(100_000))
    print(f"elapsed: {t.elapsed:.4f}s, result: {total}")

    config = {"debug": False}
    with temp_value(config, "debug", True) as cfg:
        print(cfg["debug"])  # True inside the block
    print(config["debug"])  # False restored after


def test_context_managers() -> None:
    # Timer measures something > 0
    with Timer() as t:
        _ = sum(range(1000))
    assert t.elapsed >= 0

    # temp_value restores original
    config = {"debug": False}
    with temp_value(config, "debug", True) as cfg:
        assert cfg["debug"] is True
    assert config["debug"] is False

    # temp_value removes key if it didn't exist before
    d: dict = {}
    with temp_value(d, "x", 99):
        assert d["x"] == 99
    assert "x" not in d


# -----------------------------------------------------------------------------
# 6. DUNDER METHODS
# -----------------------------------------------------------------------------
# Dunder (double-underscore) methods let your classes integrate with Python's
# built-in syntax and functions. They're how Python's data model works.
#
# JS/TS comparison:
#   TS has no equivalent — JS operators aren't overloadable.
#   The closest is implementing .toString(), .valueOf(), or Symbol.iterator.
#
# Most useful dunders:
#
#   __len__(self)            → len(obj)
#   __contains__(self, item) → item in obj
#   __iter__(self)           → for x in obj  /  list(obj)
#   __getitem__(self, key)   → obj[key]
#   __repr__(self)           → repr(obj), also fallback for str() if no __str__
#   __str__(self)            → str(obj), print(obj)
#   __eq__(self, other)      → obj == other
#   __lt__(self, other)      → obj < other  (enables sorting)
#   __add__(self, other)     → obj + other
#
# @dataclass auto-generates __init__, __repr__, __eq__ for you.
# For everything else, you implement manually.
#
# __repr__ vs __str__:
#   __repr__ — unambiguous, for developers: "ClassName(field=value)"
#   __str__  — readable, for end users: "value"
#   If only __repr__ defined, str() falls back to it.
#   Rule of thumb: always define __repr__; define __str__ only if the
#   user-facing string should differ from the developer representation.
#
# __iter__ + __len__ + __contains__ make your class feel like a built-in
# collection — usable with for, in, len(), list(), etc.


class Bag:
    """A simple multiset — like a list but unordered, focused on membership."""

    def __init__(self, items: list) -> None:
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item: object) -> bool:
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Bag({self._items!r})"

    def add(self, item: object) -> None:
        self._items.append(item)


def demo_dunders() -> None:
    b = Bag([1, 2, 3])
    print(len(b))  # 3       — __len__
    print(2 in b)  # True    — __contains__
    print(list(b))  # [1,2,3] — __iter__
    print(repr(b))  # Bag([1, 2, 3]) — __repr__
    for x in b:  # __iter__
        print(x)


def test_dunders() -> None:
    b = Bag([10, 20, 30])

    assert len(b) == 3  # __len__
    assert 20 in b  # __contains__
    assert 99 not in b
    assert list(b) == [10, 20, 30]  # __iter__
    assert repr(b) == "Bag([10, 20, 30])"  # __repr__

    b.add(40)
    assert len(b) == 4
    assert 40 in b

    # for loop uses __iter__
    total = sum(x for x in b)
    assert total == 100
