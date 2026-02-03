# ============================================================================
# PHASE 4: Functional Patterns - LESSONS
# ============================================================================
# Python has strong functional programming support. Coming from JS, most
# concepts will feel familiar but with different syntax.

# -----------------------------------------------------------------------------
# 1. LAMBDAS (Anonymous Functions)
# -----------------------------------------------------------------------------
# JS:  (x) => x * 2
# Py:  lambda x: x * 2
#
# Key differences:
# - `lambda` keyword instead of arrow syntax
# - Single expression only (no statements, no multi-line)
# - Implicit return (no `return` keyword)


def test_lambda_basics():
    # JS: const double = (x) => x * 2;
    double = lambda x: x * 2
    assert double(5) == 10

    # Multiple params
    # JS: const add = (a, b) => a + b;
    add = lambda a, b: a + b
    assert add(3, 4) == 7

    # No params
    # JS: const greet = () => "Hello";
    greet = lambda: "Hello"
    assert greet() == "Hello"


# -----------------------------------------------------------------------------
# 2. LAMBDAS vs DEF
# -----------------------------------------------------------------------------
# Lambdas are limited to single expressions. For anything complex, use def.
# Python style: prefer def for named functions, lambda for inline callbacks.


def test_lambda_vs_def():
    # Lambda - good for simple inline use
    nums = [1, 2, 3, 4, 5]
    doubled = list(map(lambda x: x * 2, nums))
    assert doubled == [2, 4, 6, 8, 10]

    # def - better when you need:
    # - Multiple statements
    # - Docstrings
    # - A meaningful name
    def process(x):
        """Double and add one."""
        result = x * 2
        return result + 1

    assert process(5) == 11


# -----------------------------------------------------------------------------
# 3. HIGHER-ORDER FUNCTIONS: map, filter, reduce
# -----------------------------------------------------------------------------
# JS has these as array methods: arr.map(), arr.filter(), arr.reduce()
# Python has them as standalone functions (and prefers comprehensions)

from functools import reduce


def test_map():
    nums = [1, 2, 3, 4]

    # JS: nums.map(x => x * 2)
    # Py: map(func, iterable) - returns iterator, not list!
    result = map(lambda x: x * 2, nums)
    assert list(result) == [2, 4, 6, 8]

    # Pythonic alternative: list comprehension (usually preferred)
    assert [x * 2 for x in nums] == [2, 4, 6, 8]


def test_filter():
    nums = [1, 2, 3, 4, 5, 6]

    # JS: nums.filter(x => x % 2 === 0)
    # Py: filter(func, iterable) - returns iterator
    result = filter(lambda x: x % 2 == 0, nums)
    assert list(result) == [2, 4, 6]

    # Pythonic alternative: list comprehension with condition
    assert [x for x in nums if x % 2 == 0] == [2, 4, 6]


def test_reduce():
    nums = [1, 2, 3, 4]

    # JS: nums.reduce((acc, x) => acc + x, 0)
    # Py: reduce(func, iterable, initial)
    # Note: reduce is in functools, not built-in (Python de-emphasized it)
    result = reduce(lambda acc, x: acc + x, nums, 0)
    assert result == 10

    # Pythonic alternative for sum: just use sum()
    assert sum(nums) == 10

    # reduce is still useful for complex accumulations
    # e.g., building a dict from a list
    pairs = [("a", 1), ("b", 2), ("c", 3)]
    result = reduce(lambda d, kv: {**d, kv[0]: kv[1]}, pairs, {})
    assert result == {"a": 1, "b": 2, "c": 3}

    # But dict comprehension is cleaner:
    assert {k: v for k, v in pairs} == {"a": 1, "b": 2, "c": 3}


# -----------------------------------------------------------------------------
# 4. FUNCTIONS AS FIRST-CLASS OBJECTS
# -----------------------------------------------------------------------------
# Functions can be assigned to variables, passed as arguments, returned.
# Same as JS, but worth seeing the Python syntax.


def test_functions_as_values():
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    # Assign to variable
    operation = add
    assert operation(2, 3) == 5

    # Pass as argument
    def apply_operation(func, a, b):
        return func(a, b)

    assert apply_operation(add, 2, 3) == 5
    assert apply_operation(multiply, 2, 3) == 6

    # Store in data structures
    operations = {"add": add, "multiply": multiply}
    assert operations["add"](2, 3) == 5


# -----------------------------------------------------------------------------
# 5. CLOSURES
# -----------------------------------------------------------------------------
# Inner functions can capture variables from enclosing scope.
# Same concept as JS closures.


def test_closures():
    def make_multiplier(factor):
        # `factor` is captured by the inner function
        def multiplier(x):
            return x * factor

        return multiplier

    double = make_multiplier(2)
    triple = make_multiplier(3)

    assert double(5) == 10
    assert triple(5) == 15

    # Each closure has its own captured `factor`
    assert double(10) == 20
    assert triple(10) == 30


def test_closure_counter():
    def make_counter():
        count = 0

        def counter():
            nonlocal count  # Required to modify enclosed variable!
            count += 1
            return count

        return counter

    c1 = make_counter()
    c2 = make_counter()

    assert c1() == 1
    assert c1() == 2
    assert c1() == 3
    assert c2() == 1  # c2 has its own count


# KEY CONCEPT: nonlocal
# - In JS, you can freely modify outer variables
# - In Python, assignment creates a NEW local variable by default
# - `nonlocal` tells Python "this variable is from an enclosing scope"
# - Without nonlocal, `count += 1` would error: UnboundLocalError


# -----------------------------------------------------------------------------
# 6. DECORATORS - THE BIG CONCEPT
# -----------------------------------------------------------------------------
# Decorators are functions that wrap other functions to modify behavior.
# @decorator is syntactic sugar for: func = decorator(func)
#
# JS equivalent: higher-order functions, or the proposed @decorator syntax


def test_decorator_basics():
    # A decorator is a function that takes a function and returns a function
    def loud(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()

        return wrapper

    # Without @ syntax (how it works under the hood)
    def greet(name):
        return f"hello, {name}"

    greet = loud(greet)  # manually apply decorator
    assert greet("world") == "HELLO, WORLD"


def test_decorator_syntax():
    def loud(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()

        return wrapper

    # With @ syntax (syntactic sugar for the above)
    @loud
    def greet(name):
        return f"hello, {name}"

    # @loud above is equivalent to: greet = loud(greet)
    assert greet("world") == "HELLO, WORLD"


# -----------------------------------------------------------------------------
# 7. DECORATORS WITH ARGUMENTS
# -----------------------------------------------------------------------------
# To pass arguments to a decorator, you need THREE levels of nesting:
# 1. Outer function takes decorator arguments
# 2. Middle function takes the function being decorated
# 3. Inner function is the wrapper that runs


def test_decorator_with_args():
    def repeat(times):
        def decorator(func):
            def wrapper(*args, **kwargs):
                results = []
                for _ in range(times):
                    results.append(func(*args, **kwargs))
                return results

            return wrapper

        return decorator

    @repeat(3)
    def say_hi():
        return "hi"

    # @repeat(3) is equivalent to: say_hi = repeat(3)(say_hi)
    assert say_hi() == ["hi", "hi", "hi"]

    @repeat(2)
    def greet(name):
        return f"hello {name}"

    assert greet("world") == ["hello world", "hello world"]


# -----------------------------------------------------------------------------
# 8. FUNCTOOLS.WRAPS - PRESERVING METADATA
# -----------------------------------------------------------------------------
# Decorators replace the original function with wrapper.
# This loses the original function's name and docstring.
# functools.wraps copies metadata from original to wrapper.

from functools import wraps


def test_wraps():
    def bad_decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    def good_decorator(func):
        @wraps(func)  # Copies __name__, __doc__, etc. from func to wrapper
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @bad_decorator
    def bad_example():
        """This is bad_example's docstring."""
        pass

    @good_decorator
    def good_example():
        """This is good_example's docstring."""
        pass

    # Without @wraps, metadata is lost
    assert bad_example.__name__ == "wrapper"
    assert bad_example.__doc__ is None

    # With @wraps, metadata is preserved
    assert good_example.__name__ == "good_example"
    assert good_example.__doc__ == "This is good_example's docstring."


# -----------------------------------------------------------------------------
# 9. COMMON DECORATOR PATTERNS
# -----------------------------------------------------------------------------


def test_timing_decorator():
    import time

    def timing(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            wrapper.last_duration = end - start  # attach timing to function
            return result

        return wrapper

    @timing
    def slow_function():
        time.sleep(0.01)
        return "done"

    result = slow_function()
    assert result == "done"
    assert slow_function.last_duration >= 0.01


def test_memoization_decorator():
    call_count = 0

    def memoize(func):
        cache = {}

        @wraps(func)
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]

        return wrapper

    @memoize
    def expensive(n):
        nonlocal call_count
        call_count += 1
        return n * 2

    # First call computes
    assert expensive(5) == 10
    assert call_count == 1

    # Second call uses cache
    assert expensive(5) == 10
    assert call_count == 1  # didn't increment

    # Different arg computes
    assert expensive(10) == 20
    assert call_count == 2


# Note: Python has @functools.cache and @functools.lru_cache built-in!
from functools import cache, lru_cache


def test_builtin_cache():
    call_count = 0

    @cache  # Simple unbounded cache
    def fib(n):
        nonlocal call_count
        call_count += 1
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    assert fib(10) == 55
    # Without cache, fib(10) would make 177 calls
    # With cache, only 11 calls (one per unique n)
    assert call_count == 11


# -----------------------------------------------------------------------------
# 10. PARTIAL APPLICATION
# -----------------------------------------------------------------------------
# functools.partial creates a new function with some arguments pre-filled.
# Similar to JS .bind() for arguments (not `this`).

from functools import partial


def test_partial():
    def power(base, exponent):
        return base**exponent

    # Create specialized functions
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)

    assert square(5) == 25
    assert cube(5) == 125

    # First positional arg can also be fixed
    powers_of_two = partial(power, 2)
    assert powers_of_two(8) == 256  # 2^8


def test_partial_with_callbacks():
    def greet(greeting, name):
        return f"{greeting}, {name}!"

    # Useful for callbacks where you want to fix some args
    say_hello = partial(greet, "Hello")
    say_bye = partial(greet, "Goodbye")

    names = ["Alice", "Bob"]
    hellos = list(map(say_hello, names))
    assert hellos == ["Hello, Alice!", "Hello, Bob!"]


# -----------------------------------------------------------------------------
# 11. SORTED WITH KEY FUNCTIONS
# -----------------------------------------------------------------------------
# sorted() takes a key function - a perfect use case for lambdas.


def test_sorted_with_key():
    words = ["banana", "pie", "apple", "cherry"]

    # Sort by length
    by_length = sorted(words, key=lambda w: len(w))
    assert by_length == ["pie", "apple", "banana", "cherry"]

    # Sort by last letter
    by_last = sorted(words, key=lambda w: w[-1])
    assert by_last == ["banana", "apple", "pie", "cherry"]

    # Sort dicts by a field
    people = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35},
    ]
    by_age = sorted(people, key=lambda p: p["age"])
    assert [p["name"] for p in by_age] == ["Bob", "Alice", "Charlie"]


# operator.itemgetter and attrgetter are cleaner for simple cases
from operator import itemgetter, attrgetter


def test_operator_getters():
    people = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
    ]

    # itemgetter for dict keys
    by_age = sorted(people, key=itemgetter("age"))
    assert by_age[0]["name"] == "Bob"

    # attrgetter for object attributes
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    persons = [Person("Alice", 30), Person("Bob", 25)]
    by_age = sorted(persons, key=attrgetter("age"))
    assert by_age[0].name == "Bob"


# -----------------------------------------------------------------------------
# SUMMARY: When to use what
# -----------------------------------------------------------------------------
# - lambda: simple inline callbacks (sorting keys, map/filter args)
# - def: anything complex, anything that needs a name or docstring
# - map/filter: occasionally, but list comprehensions usually preferred
# - reduce: rare, usually there's a cleaner alternative
# - decorators: cross-cutting concerns (logging, timing, caching, auth)
# - partial: fixing arguments for callbacks
# - closures: stateful functions, factory functions
