# ============================================================================
# PHASE 1: Syntax Bridge (JS → Python) - LESSONS
# ============================================================================

# -----------------------------------------------------------------------------
# WHAT IS "PYTHONIC"?
# -----------------------------------------------------------------------------
# "Pythonic" = code that follows Python's idioms, not just code that works.
# Python has a "preferred way" to do things — readable, simple, using built-ins.
#
# Examples:
#   NOT Pythonic                      Pythonic
#   --------------------------------  --------------------------------
#   if len(my_list) > 0:              if my_list:  # truthy check
#
#   result = []                       result = [x * 2 for x in items]
#   for i in range(len(items)):       # list comprehension
#       result.append(items[i] * 2)
#
#   if x >= 0 and x <= 10:            if 0 <= x <= 10:  # chained comparison
#
# The Zen of Python (run `import this`):
#   - "Beautiful is better than ugly"
#   - "Simple is better than complex"
#   - "Readability counts"
#
# Key style conventions:
#   - snake_case for variables/functions (not camelCase)
#   - 4-space indentation
#   - Use built-in functions and comprehensions over manual loops
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# 1. VARIABLES & TYPES
# -----------------------------------------------------------------------------
# JS:  const name = "Alice"   let age = 30
# Py:  name = "Alice"         age = 30  (no const/let, all mutable by default)

# Type hints (like TypeScript annotations - optional but recommended)
# JS/TS: function greet(name: string): string
# Py:    def greet(name: str) -> str:


def greet(name: str) -> str:
    return f"Hello, {name}!"  # f-strings = template literals (`Hello, ${name}!`)


def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"


# -----------------------------------------------------------------------------
# 2. FUNCTIONS: def, *args, **kwargs
# -----------------------------------------------------------------------------
# JS:  function add(a, b) { return a + b }
# Py:  def add(a, b): return a + b  (or multi-line with indentation)


def add(a: int, b: int) -> int:
    return a + b


# Default params (same concept as JS)
def greet_with_default(name: str = "World") -> str:
    return f"Hello, {name}!"


# *args = rest params (...args in JS)
# JS:  function sum(...nums) { return nums.reduce((a,b) => a+b, 0) }
def sum_all(*nums: int) -> int:
    total = 0
    for n in nums:
        total += n
    return total


# **kwargs = object destructuring for named params
# JS:  function config({host = 'localhost', port = 8080}) { ... }
def config(**kwargs) -> dict:
    defaults = {"host": "localhost", "port": 8080}
    return {**defaults, **kwargs}  # spread works same as JS!


def test_functions():
    assert add(2, 3) == 5
    assert greet_with_default() == "Hello, World!"
    assert greet_with_default("Python") == "Hello, Python!"
    assert sum_all(1, 2, 3, 4) == 10
    assert config(port=3000) == {"host": "localhost", "port": 3000}


# -----------------------------------------------------------------------------
# 3. CONTROL FLOW
# -----------------------------------------------------------------------------
# if/elif/else (elif not else if)
# No braces - indentation defines blocks (like significant whitespace)


def classify_number(n: int) -> str:
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


# for loops - iterate directly (no index needed usually)
# JS:  for (const item of items) { ... }
# Py:  for item in items: ...


def double_all(nums: list[int]) -> list[int]:
    result = []
    for n in nums:
        result.append(n * 2)
    return result


# range() for index-based loops
# JS:  for (let i = 0; i < 5; i++) { ... }
# Py:  for i in range(5): ...


def test_control_flow():
    assert classify_number(-5) == "negative"
    assert classify_number(0) == "zero"
    assert classify_number(10) == "positive"
    assert double_all([1, 2, 3]) == [2, 4, 6]


# -----------------------------------------------------------------------------
# 4. TRUTHINESS DIFFERENCES
# -----------------------------------------------------------------------------
# Python falsy: False, None, 0, 0.0, "", [], {}, set()
# JS falsy:     false, null, undefined, 0, "", NaN
#
# Key difference: empty list [] is falsy in Python, but [] is truthy in JS!


def is_empty(collection) -> bool:
    if collection:
        return False
    return True


def test_truthiness():
    assert is_empty([]) == True  # empty list is falsy
    assert is_empty([1]) == False
    assert is_empty("") == True  # empty string is falsy (same as JS)
    assert is_empty({}) == True  # empty dict is falsy


# -----------------------------------------------------------------------------
# 5. NONE vs null/undefined
# -----------------------------------------------------------------------------
# Python has ONE null type: None (no undefined)
# Use `is None` not `== None` for checking


def find_first_even(nums: list[int]):  # -> int | None
    for n in nums:
        if n % 2 == 0:
            return n
    return None


def test_none():
    assert find_first_even([1, 3, 5]) is None
    assert find_first_even([1, 2, 3]) == 2
