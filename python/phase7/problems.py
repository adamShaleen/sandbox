# ============================================================================
# PHASE 7: Modules & Packaging - PROBLEMS
# ============================================================================
# Practice problems for Phase 7 concepts.
# Run tests: npm run test:py:file python/phase7/problems.py


# -----------------------------------------------------------------------------
# PROBLEM 1: module_info
# -----------------------------------------------------------------------------
# Write a function `module_info(module)` that takes an imported module object
# and returns a dict with the following keys:
#   - "name": the module's __name__
#   - "is_package": True if it's a package (has __path__), False otherwise
#   - "has_file": True if it has a __file__ attribute
#
# Example:
#   import math
#   module_info(math) -> {"name": "math", "is_package": False, "has_file": True}
#
#   import os
#   module_info(os) -> {"name": "os", "is_package": False, "has_file": True}
#
#   import importlib
#   module_info(importlib) -> {"name": "importlib", "is_package": True, "has_file": True}
#
# JS equivalent: No real parallel — JS modules don't expose metadata like this.
#
# Hints:
# - Use hasattr() to check for optional attributes
# - __path__ only exists on packages
#


def module_info(module):
    is_package = hasattr(module, "__path__")
    has_file = hasattr(module, "__file__")
    return {"name": module.__name__, "is_package": is_package, "has_file": has_file}


def test_module_info():
    import math
    import importlib

    result = module_info(math)
    assert result["name"] == "math"
    assert result["is_package"] is False
    assert result["has_file"] is True

    result = module_info(importlib)
    assert result["name"] == "importlib"
    assert result["is_package"] is True
    assert result["has_file"] is True


# -----------------------------------------------------------------------------
# PROBLEM 2: path_stats
# -----------------------------------------------------------------------------
# Write a function `path_stats(path_str)` that takes a file path string and
# returns a dict with:
#   - "stem": filename without extension
#   - "suffix": file extension including the dot (e.g. ".py")
#   - "parts": tuple of path components
#   - "depth": number of parts in the path
#
# Use pathlib.Path — no string splitting.
#
# Example:
#   path_stats("/usr/local/bin/python.exe")
#   -> {
#       "stem": "python",
#       "suffix": ".exe",
#       "parts": ("/", "usr", "local", "bin", "python.exe"),
#       "depth": 5,
#      }
#
# JS equivalent: path.parse() partially, but no .parts equivalent
#
# Hints:
# - pathlib.Path has .stem, .suffix, .parts attributes
# - len() works on .parts
#

from pathlib import Path


def path_stats(path_str):
    p = Path(path_str)
    return {"stem": p.stem, "suffix": p.suffix, "parts": p.parts, "depth": len(p.parts)}


def test_path_stats():
    result = path_stats("/usr/local/bin/python.exe")
    assert result["stem"] == "python"
    assert result["suffix"] == ".exe"
    assert result["parts"] == ("/", "usr", "local", "bin", "python.exe")
    assert result["depth"] == 5

    result = path_stats("/some/dir/lessons.py")
    assert result["stem"] == "lessons"
    assert result["suffix"] == ".py"
    assert result["depth"] == 4


# -----------------------------------------------------------------------------
# PROBLEM 3: word_frequency
# -----------------------------------------------------------------------------
# Write a function `word_frequency(text)` that takes a string and returns a
# dict mapping each word to its count, sorted by frequency (highest first).
#
# - Case-insensitive ("Apple" and "apple" are the same word)
# - Ignore punctuation (strip .,!? from words)
# - Return a regular dict (insertion-ordered in Python 3.7+)
#
# Example:
#   word_frequency("the cat sat on the mat the cat")
#   -> {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1}
#
# JS equivalent:
#   text.toLowerCase().split(" ").reduce((acc, w) => {
#     acc[w] = (acc[w] ?? 0) + 1; return acc;
#   }, {})
#
# Hints:
# - collections.Counter does the counting for you
# - str.lower() and str.strip(".,!?") for normalisation
# - Counter.most_common() returns items sorted by frequency
# - dict() on a list of (key, value) pairs builds the final dict
#

from collections import Counter


def word_frequency(text):
    normalized = [word.lower().strip(".,!?") for word in text.split()]
    return Counter(normalized)


def test_word_frequency():
    result = word_frequency("the cat sat on the mat the cat")
    assert result == {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1}

    result = word_frequency("Hello, hello! World.")
    assert result == {"hello": 2, "world": 1}

    assert word_frequency("") == {}


# -----------------------------------------------------------------------------
# PROBLEM 4: group_by
# -----------------------------------------------------------------------------
# Write a function `group_by(items, key_fn)` that takes a list and a key
# function, and returns a dict grouping items by the result of key_fn.
#
# Example:
#   group_by(["apple", "banana", "avocado", "blueberry"], lambda w: w[0])
#   -> {"a": ["apple", "avocado"], "b": ["banana", "blueberry"]}
#
#   group_by([1, 2, 3, 4, 5, 6], lambda n: "even" if n % 2 == 0 else "odd")
#   -> {"odd": [1, 3, 5], "even": [2, 4, 6]}
#
# JS equivalent:
#   items.reduce((acc, x) => {
#     const k = keyFn(x); (acc[k] ??= []).push(x); return acc;
#   }, {})
#
# Hints:
# - defaultdict(list) from collections handles the "create list if missing" part
# - Return a plain dict at the end (dict(grouped) or {**grouped})
#

from collections import defaultdict


def group_by(items, key_fn):
    groups = defaultdict(list)

    for item in items:
        key = key_fn(item)
        groups[key].append(item)

    return dict(groups)


def test_group_by():
    result = group_by(["apple", "banana", "avocado", "blueberry"], lambda w: w[0])
    assert result == {"a": ["apple", "avocado"], "b": ["banana", "blueberry"]}

    result = group_by([1, 2, 3, 4, 5, 6], lambda n: "even" if n % 2 == 0 else "odd")
    assert result == {"odd": [1, 3, 5], "even": [2, 4, 6]}

    assert group_by([], lambda x: x) == {}


# -----------------------------------------------------------------------------
# PROBLEM 5: cached_fibonacci
# -----------------------------------------------------------------------------
# Write a function `cached_fibonacci(n)` that returns the nth Fibonacci number,
# using functools.lru_cache to memoize results.
#
# Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
#   fib(0) = 0
#   fib(1) = 1
#   fib(n) = fib(n-1) + fib(n-2)
#
# After calling the function, demonstrate that the cache is working by
# checking cache_info().hits > 0 after repeated calls.
#
# JS equivalent: Manual memoization with a Map/closure — no built-in decorator
#
# Hints:
# - from functools import lru_cache
# - Apply @lru_cache as a decorator on the function
# - lru_cache decorated functions have a .cache_info() method
#   that returns hits, misses, maxsize, currsize
#

from functools import lru_cache


@lru_cache
def cached_fibonacci(n):
    if n <= 1:
        return n
    return cached_fibonacci(n - 1) + cached_fibonacci(n - 2)


def test_cached_fibonacci():
    assert cached_fibonacci(0) == 0
    assert cached_fibonacci(1) == 1
    assert cached_fibonacci(10) == 55
    assert cached_fibonacci(20) == 6765

    # Calling again should hit the cache
    cached_fibonacci(10)
    info = cached_fibonacci.cache_info()
    assert info.hits > 0


# -----------------------------------------------------------------------------
# PROBLEM 6: json_round_trip
# -----------------------------------------------------------------------------
# Write a function `json_round_trip(data)` that:
#   1. Serializes `data` to a JSON string
#   2. Deserializes it back to a Python object
#   3. Returns a tuple of (json_string, restored_object)
#
# The JSON string should be compact (no extra spaces).
#
# Example:
#   json_string, restored = json_round_trip({"name": "ada", "scores": [1, 2, 3]})
#   json_string -> '{"name": "ada", "scores": [1, 2, 3]}'
#   restored    -> {"name": "ada", "scores": [1, 2, 3]}
#
# JS equivalent: JSON.stringify / JSON.parse
#
# Hints:
# - import json (already in the stdlib)
# - json.dumps() serializes, json.loads() deserializes
# - Pass separators=(",", ":") to json.dumps() for compact output (no spaces)
#

import json


def json_round_trip(data):
    serialized = json.dumps(data, separators=(",", ":"))
    de_serialized = json.loads(serialized)
    return (serialized, de_serialized)


def test_json_round_trip():
    data = {"name": "ada", "scores": [1, 2, 3]}
    json_str, restored = json_round_trip(data)
    assert json_str == '{"name":"ada","scores":[1,2,3]}'
    assert restored == data  # same values
    assert restored is not data  # but a different object in memory

    json_str, restored = json_round_trip([1, "two", True, None])
    assert json_str == '[1,"two",true,null]'
    assert restored == [1, "two", True, None]


# -----------------------------------------------------------------------------
# PROBLEM 7: sys_summary
# -----------------------------------------------------------------------------
# Write a function `sys_summary()` that returns a dict with info about the
# current Python runtime:
#   - "version": the major and minor version as a tuple e.g. (3, 9)
#   - "platform": the platform string (e.g. "darwin", "linux", "win32")
#   - "path_count": number of entries in sys.path
#   - "is_64bit": True if the interpreter is 64-bit, False otherwise
#
# JS equivalent: process.version, process.platform, process.arch
#
# Hints:
# - import sys
# - sys.version_info has .major and .minor attributes
# - sys.platform is the platform string
# - sys.path is a list
# - struct.calcsize("P") returns pointer size in bytes; 8 bytes = 64-bit
#

import sys
import struct


def sys_summary():
    version = (sys.version_info.major, sys.version_info.minor)
    platform = sys.platform
    path_count = len(sys.path)
    is_64bit = struct.calcsize("P") == 8

    return {
        "version": version,
        "platform": platform,
        "path_count": path_count,
        "is_64bit": is_64bit,
    }


def test_sys_summary():

    result = sys_summary()
    assert result["version"] == (sys.version_info.major, sys.version_info.minor)
    assert result["platform"] == sys.platform
    assert result["path_count"] == len(sys.path)
    assert isinstance(result["is_64bit"], bool)


# -----------------------------------------------------------------------------
# PROBLEM 8: flatten
# -----------------------------------------------------------------------------
# Write a function `flatten(nested)` that takes a list which may contain
# other lists (one level deep) and returns a single flat list.
#
# Example:
#   flatten([[1, 2], [3, 4], [5]])  -> [1, 2, 3, 4, 5]
#   flatten([[1, 2], [], [3]])      -> [1, 2, 3]
#   flatten([])                     -> []
#
# JS equivalent: [].concat(...nested)  or  nested.flat()
#
# Hints:
# - itertools.chain.from_iterable() is the stdlib tool for this exact task
#   It takes an iterable of iterables and yields each item one by one
#   e.g. chain.from_iterable([[1,2],[3,4]]) yields 1, 2, 3, 4
# - Wrap the result in list() to get a concrete list back
# - itertools is a stdlib module — no install needed, just import it
#

import itertools


def flatten(nested):
    return list(itertools.chain.from_iterable(nested))


def test_flatten():
    assert flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]
    assert flatten([]) == []
    assert flatten([[], [], []]) == []


# -----------------------------------------------------------------------------
# PROBLEM 9: date_range
# -----------------------------------------------------------------------------
# Write a function `date_range(start, end)` that takes two date strings in
# "YYYY-MM-DD" format and returns a list of all dates from start to end,
# inclusive, as formatted strings in the same format.
#
# Example:
#   date_range("2026-01-01", "2026-01-05")
#   -> ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"]
#
# JS equivalent: No built-in — you'd manually loop with Date objects or use date-fns
#
# You'll need these from the datetime module:
#   - datetime.date.fromisoformat(string) — parses a "YYYY-MM-DD" string into a date object
#   - datetime.timedelta(days=1) — represents a duration of 1 day; you can add it to a date
#   - date.strftime("%Y-%m-%d") — formats a date object back to a string
#
# Example of how these work together:
#   from datetime import date, timedelta
#   d = date.fromisoformat("2026-01-01")   # date(2026, 1, 1)
#   d + timedelta(days=1)                   # date(2026, 1, 2)
#   d.strftime("%Y-%m-%d")                  # "2026-01-01"
#
# Hints:
# - Parse both strings into date objects first
# - Use a while loop: start at `start`, keep adding timedelta(days=1) until you pass `end`
# - Append the formatted string to a result list each iteration
#

from datetime import date, timedelta


def date_range(start, end):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    current = start_date
    result = []

    while current <= end_date:
        result.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    return result


def test_date_range():
    result = date_range("2026-01-01", "2026-01-05")
    assert result == [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05",
    ]

    # single day range
    assert date_range("2026-03-15", "2026-03-15") == ["2026-03-15"]

    # crosses month boundary
    result = date_range("2026-01-30", "2026-02-02")
    assert result == ["2026-01-30", "2026-01-31", "2026-02-01", "2026-02-02"]


# -----------------------------------------------------------------------------
# PROBLEM 10: import_or_default
# -----------------------------------------------------------------------------
# Write a function `import_or_default(module_name, attr, default)` that:
#   - Tries to import a module by name
#   - If successful, returns the value of `attr` from that module
#   - If the module doesn't exist, returns `default` instead of raising an error
#
# Example:
#   import_or_default("math", "pi", 0)       -> 3.141592653589793
#   import_or_default("math", "e", 0)        -> 2.718281828459045
#   import_or_default("nope", "anything", 42) -> 42  (module doesn't exist)
#
# JS equivalent: A try/catch around a dynamic import(), falling back to a default
#
# You'll need these:
#   - importlib.import_module(name) — imports a module by its string name,
#     the same as writing `import name` but works dynamically at runtime.
#     Raises ModuleNotFoundError if the module doesn't exist.
#   - getattr(obj, name) — gets an attribute from an object by string name,
#     the same as obj.name but works when you don't know the name until runtime.
#     e.g. getattr(math, "pi") is the same as math.pi
#
# Hints:
# - Use a try/except to catch ModuleNotFoundError
# - importlib is already imported earlier in the lessons file, but you'll
#   need to import it here in problems.py
#

import importlib


def import_or_default(module_name, attr, default):
    try:
        module_type = importlib.import_module(module_name)
        return getattr(module_type, attr)
    except ModuleNotFoundError:
        return default


def test_import_or_default():
    import math

    assert import_or_default("math", "pi", 0) == math.pi
    assert import_or_default("math", "e", 0) == math.e
    assert import_or_default("totally_fake_module", "anything", 42) == 42
    assert import_or_default("os", "sep", "/") == __import__("os").sep


# -----------------------------------------------------------------------------
# PROBLEM 11: make_counter
# -----------------------------------------------------------------------------
# Write a function `make_counter(start=0)` that returns a closure — a function
# that increments and returns a count each time it's called.
#
# A closure is a function that "remembers" variables from the scope it was
# defined in, even after that outer function has returned.
#
# Example:
#   counter = make_counter()
#   counter()  -> 1
#   counter()  -> 2
#   counter()  -> 3
#
#   counter_from_10 = make_counter(start=10)
#   counter_from_10()  -> 11
#   counter_from_10()  -> 12
#
# JS equivalent:
#   function makeCounter(start = 0) {
#     let count = start;
#     return () => ++count;
#   }
#
# You'll need:
#   - `nonlocal` — tells Python that a variable inside an inner function
#     refers to the one in the enclosing (outer) function's scope, not a new local.
#     Without it, assigning to `count` inside the inner function creates a new
#     local variable instead of modifying the outer one.
#
#     Example:
#       def outer():
#           x = 0
#           def inner():
#               nonlocal x   # refers to outer's x
#               x += 1
#               return x
#           return inner
#
# Hints:
# - Define an inner function inside make_counter
# - Use nonlocal to modify the count variable from the outer scope
# - Return the inner function (not the result of calling it)
#


def make_counter(start=0):
    count = start

    def inner():
        nonlocal count
        count += 1
        return count

    return inner


def test_make_counter():
    counter = make_counter()
    assert counter() == 1
    assert counter() == 2
    assert counter() == 3

    counter_from_10 = make_counter(start=10)
    assert counter_from_10() == 11
    assert counter_from_10() == 12

    # each counter is independent
    assert counter() == 4


# -----------------------------------------------------------------------------
# PROBLEM 12: safe_import
# -----------------------------------------------------------------------------
# Write a function `safe_import(module_name)` that tries to import a module
# and returns a tuple of (success, result) where:
#   - On success: (True, the module object)
#   - On failure: (False, the error message string)
#
# Example:
#   success, result = safe_import("math")
#   success -> True
#   result  -> <module 'math' ...>
#
#   success, result = safe_import("fake_module")
#   success -> False
#   result  -> "No module named 'fake_module'"
#
# JS equivalent:
#   try {
#     const mod = await import(name);
#     return [true, mod];
#   } catch (e) {
#     return [false, e.message];
#   }
#
# You'll need:
#   - importlib.import_module(name) — same as problem 10
#   - str(e) — converts an exception object to its message string.
#     When you catch an exception with `except ModuleNotFoundError as e`,
#     calling str(e) gives you the human-readable error message.
#
# Hints:
# - Return a tuple using (value1, value2) syntax
# - Catch ModuleNotFoundError and return the error as a string with str(e)
#


def safe_import(module_name):
    try:
        module_type = importlib.import_module(module_name)
        return (True, module_type)
    except ModuleNotFoundError as e:
        err_msg = str(e)
        return (False, err_msg)


def test_safe_import():
    success, result = safe_import("math")
    assert success is True
    assert result.__name__ == "math"  # type: ignore

    success, result = safe_import("fake_module")
    assert success is False
    assert "fake_module" in result  # type: ignore
    assert isinstance(result, str)
