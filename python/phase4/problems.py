# ============================================================================
# PHASE 4: Functional Patterns - PROBLEMS
# ============================================================================
# Practice problems for Phase 4 concepts.
# Run tests: npm run test:py -- python/phase4/problems.py


# -----------------------------------------------------------------------------
# PROBLEM 1: Transform Pipeline
# -----------------------------------------------------------------------------
# Create a function `pipeline` that takes a value and a list of functions,
# then applies each function in sequence, passing the result to the next.
#
# Example:
#   pipeline(5, [lambda x: x + 1, lambda x: x * 2, str])
#   -> "12"  (5 -> 6 -> 12 -> "12")
#
# JS equivalent:
#   const pipeline = (val, fns) => fns.reduce((acc, fn) => fn(acc), val)
#
# Hints:
# - Use reduce from functools
# - The accumulator starts as the initial value
# - Each step applies the next function to the accumulator
#

from functools import reduce


def pipeline(value, functions):
    return reduce(lambda accumulator, func: func(accumulator), functions, value)


def alternative_pipeline(value, functions):
    for func in functions:
        value = func(value)
    return value


def test_pipeline():
    # Simple chain
    result = pipeline(5, [lambda x: x + 1, lambda x: x * 2])
    assert result == 12  # 5 -> 6 -> 12

    # Type conversions
    result = pipeline(5, [lambda x: x * 2, str, lambda s: s + "!"])
    assert result == "10!"

    # Empty functions list returns original value
    assert pipeline(42, []) == 42

    # Single function
    assert pipeline(10, [lambda x: x // 2]) == 5

    # String processing
    result = pipeline("  HELLO  ", [str.strip, str.lower, lambda s: s + " world"])
    assert result == "hello world"


# -----------------------------------------------------------------------------
# PROBLEM 2: Compose
# -----------------------------------------------------------------------------
# Create a function `compose` that takes multiple functions and returns
# a new function that applies them right-to-left.
#
# This is the opposite of pipeline - last function runs first.
#
# Example:
#   add_one = lambda x: x + 1
#   double = lambda x: x * 2
#   composed = compose(str, double, add_one)
#   composed(5) -> "12"  (add_one first: 6, then double: 12, then str: "12")
#
# JS equivalent:
#   const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x)
#
# Hints:
# - Return a new function (closure!)
# - reversed() or slice [::-1] to reverse the function list
# - Can reuse pipeline internally
#


def compose(*functions):
    def composed(value):
        return pipeline(value, list(reversed(functions)))

    return composed


def test_compose():
    add_one = lambda x: x + 1
    double = lambda x: x * 2
    to_string = str

    # Right-to-left: add_one(5)=6, double(6)=12, str(12)="12"
    composed = compose(to_string, double, add_one)
    assert composed(5) == "12"

    # Single function
    just_double = compose(double)
    assert just_double(5) == 10

    # Identity when no functions (returns input unchanged)
    identity = compose()
    assert identity(42) == 42

    # String operations (right to left)
    shout = compose(lambda s: s + "!", str.upper, str.strip)
    assert shout("  hello  ") == "HELLO!"


# -----------------------------------------------------------------------------
# PROBLEM 3: once
# -----------------------------------------------------------------------------
# Create a decorator `once` that ensures a function only executes once.
# Subsequent calls return the cached result from the first call.
#
# JS equivalent: Lodash's _.once()
#
# Hints:
# - Store the result in the wrapper's closure
# - Use a flag to track if function has been called
# - Use functools.wraps to preserve metadata
#

from functools import wraps


def once(func):
    was_called = False
    cached_result = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal was_called, cached_result

        if was_called:
            return cached_result

        cached_result = func(*args, **kwargs)
        was_called = True
        return cached_result

    return wrapper


def test_once():
    call_count = 0

    @once
    def expensive_init():
        nonlocal call_count
        call_count += 1
        return "initialized"

    # First call executes
    assert expensive_init() == "initialized"
    assert call_count == 1

    # Subsequent calls return cached result
    assert expensive_init() == "initialized"
    assert expensive_init() == "initialized"
    assert call_count == 1  # Still 1!


def test_once_with_args():
    call_count = 0

    @once
    def greet(name):
        nonlocal call_count
        call_count += 1
        return f"Hello, {name}!"

    # First call with "Alice"
    assert greet("Alice") == "Hello, Alice!"
    assert call_count == 1

    # Second call with "Bob" still returns first result
    assert greet("Bob") == "Hello, Alice!"  # Cached!
    assert call_count == 1


def test_once_preserves_metadata():
    @once
    def documented_function():
        """This is the docstring."""
        return 42

    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "This is the docstring."


# -----------------------------------------------------------------------------
# PROBLEM 4: retry
# -----------------------------------------------------------------------------
# Create a decorator `retry(max_attempts)` that retries a function
# if it raises an exception, up to max_attempts times.
#
# Example usage:
#   @retry(3)
#   def flaky_api_call():
#       # might fail sometimes
#       return fetch_data()
#
#   flaky_api_call()  # Will try up to 3 times before giving up
#
# Behavior:
# - Call the function
# - If it succeeds, return the result immediately
# - If it raises an exception, try again
# - After max_attempts failures, raise the last exception
#
# Why three levels of nesting?
#
#   @retry(3)        <-- retry(3) is called FIRST, must return a decorator
#   def foo(): ...   <-- that decorator receives foo
#
#   This is equivalent to: foo = retry(3)(foo)
#
#   So you need:
#   1. retry(max_attempts) - receives the argument (3), returns a decorator
#   2. decorator(func)     - receives the function (foo), returns a wrapper
#   3. wrapper(*args)      - runs when foo() is called, does the retry logic
#
# Structure:
#   def retry(max_attempts):          # Level 1: gets the config
#       def decorator(func):          # Level 2: gets the function
#           def wrapper(*args, **kwargs):  # Level 3: runs on each call
#               # retry logic here
#           return wrapper
#       return decorator
#
# Hints:
# - for attempt in range(max_attempts): try/except inside
# - On success: return result
# - On failure: if last attempt, raise; otherwise continue loop
#


def retry(max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

            raise last_exception

        return wrapper

    return decorator


def test_retry_succeeds_first_try():
    call_count = 0

    @retry(3)
    def always_works():
        nonlocal call_count
        call_count += 1
        return "success"

    assert always_works() == "success"
    assert call_count == 1


def test_retry_succeeds_after_failures():
    attempt = 0

    @retry(3)
    def fails_twice():
        nonlocal attempt
        attempt += 1
        if attempt < 3:
            raise ValueError("not yet")
        return "finally!"

    assert fails_twice() == "finally!"
    assert attempt == 3


def test_retry_exhausts_attempts():
    call_count = 0

    @retry(3)
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise RuntimeError("nope")

    try:
        always_fails()
        assert False, "Should have raised"
    except RuntimeError as e:
        assert str(e) == "nope"

    assert call_count == 3  # Tried 3 times


# -----------------------------------------------------------------------------
# PROBLEM 5: throttle
# -----------------------------------------------------------------------------
# Create a decorator `throttle(min_interval)` that ensures a function
# is called at most once per min_interval seconds.
#
# - If called again before min_interval has passed, return None
# - If enough time has passed, call the function and return result
#
# Hints:
# - Store last_called timestamp in closure
# - time.time() returns current time in seconds
# - Initialize last_called to 0 (or None) so first call always runs
#

import time


def throttle(min_interval):
    def decorator(func):
        last_called = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called
            now = time.time()
            elapsed = now - last_called

            if elapsed < min_interval:
                return None

            last_called = now
            return func(*args, **kwargs)

        return wrapper

    return decorator


def test_throttle():
    call_count = 0

    @throttle(0.1)  # 100ms minimum interval
    def rapid_fire():
        nonlocal call_count
        call_count += 1
        return "fired"

    # First call works
    assert rapid_fire() == "fired"
    assert call_count == 1

    # Immediate second call is throttled
    assert rapid_fire() is None
    assert call_count == 1

    # Wait for interval to pass
    time.sleep(0.15)

    # Now it works again
    assert rapid_fire() == "fired"
    assert call_count == 2


# -----------------------------------------------------------------------------
# PROBLEM 6: Map with index
# -----------------------------------------------------------------------------
# Create a function `map_with_index` that works like map but also passes
# the index to the function.
#
# JS equivalent: arr.map((item, index) => ...)
#
# Hints:
# - enumerate() gives you (index, item) pairs
# - Return a list, not an iterator (for simplicity)
#


def map_with_index(func, iterable):
    return [func(item, i) for i, item in enumerate(iterable)]


def test_map_with_index():
    # Add index to each item
    result = map_with_index(lambda x, i: f"{i}:{x}", ["a", "b", "c"])
    assert result == ["0:a", "1:b", "2:c"]

    # Multiply by index
    result = map_with_index(lambda x, i: x * i, [1, 2, 3, 4])
    assert result == [0, 2, 6, 12]  # [1*0, 2*1, 3*2, 4*3]

    # Empty list
    assert map_with_index(lambda x, i: x, []) == []


# -----------------------------------------------------------------------------
# PROBLEM 7: group_by
# -----------------------------------------------------------------------------
# Create a function `group_by` that groups items by the result of a key function.
# Returns a dict where keys are the results of key_func and values are lists.
#
# JS equivalent: Lodash's _.groupBy()
#
# Example:
#   group_by(lambda x: x % 2, [1, 2, 3, 4, 5]) -> {1: [1, 3, 5], 0: [2, 4]}
#
# Hints:
# - defaultdict(list) is perfect for this
# - Or use dict.setdefault()
#


def group_by(key_func, iterable):
    output = dict()

    for item in iterable:
        output.setdefault(key_func(item), []).append(item)

    return output


def test_group_by():
    # Group by even/odd
    result = group_by(lambda x: x % 2, [1, 2, 3, 4, 5, 6])
    assert result == {1: [1, 3, 5], 0: [2, 4, 6]}

    # Group strings by length
    words = ["cat", "dog", "elephant", "rat", "giraffe"]
    result = group_by(len, words)
    assert result == {3: ["cat", "dog", "rat"], 8: ["elephant"], 7: ["giraffe"]}

    # Group by first letter
    result = group_by(lambda s: s[0], ["apple", "apricot", "banana", "avocado"])
    assert result == {"a": ["apple", "apricot", "avocado"], "b": ["banana"]}

    # Empty input
    assert group_by(lambda x: x, []) == {}


# -----------------------------------------------------------------------------
# PROBLEM 8: curry (Advanced)
# -----------------------------------------------------------------------------
# Create a decorator `curry` that converts a function to curried form.
# A curried function can be called with arguments one at a time.
#
# Example:
#   @curry
#   def add(a, b, c):
#       return a + b + c
#
#   add(1)(2)(3)  -> 6
#   add(1, 2)(3)  -> 6
#   add(1)(2, 3)  -> 6
#   add(1, 2, 3)  -> 6
#
# JS equivalent: Lodash's _.curry() or Ramda's R.curry()
#
# Hints:
# - inspect.signature(func).parameters tells you how many args func takes
# - Return a new function that accumulates arguments
# - When you have enough args, call the original function
# - This is tricky! Think recursively or use a helper closure
#

import inspect


def curry(func):
    # How many args does the original function need? e.g., add(a,b,c) → 3
    num_params = len(inspect.signature(func).parameters)

    # helper creates a function that "remembers" previously collected args
    def helper(accumulated_args):
        @wraps(func)
        # inner is what gets called each time: add(1), then (2), then (3)
        def inner(*new_args):
            # Combine what we had + what we just received
            # e.g., accumulated=[1], new_args=(2,) → all_args=[1,2]
            all_args = accumulated_args + list(new_args)

            # Do we have enough args now?
            if len(all_args) >= num_params:
                # Yes! Call the original function with all collected args
                return func(*all_args)

            # Not enough yet — return a NEW inner that remembers all_args
            # e.g., helper([1,2]) returns an inner waiting for the 3rd arg
            return helper(all_args)

        return inner

    # Start with empty accumulator — first call to add() uses this inner
    return helper([])


def test_curry():
    @curry
    def add(a, b, c):
        return a + b + c

    # All at once
    assert add(1, 2, 3) == 6

    # # One at a time
    assert add(1)(2)(3) == 6

    # # Mixed
    assert add(1, 2)(3) == 6
    assert add(1)(2, 3) == 6

    # # Partial application returns function
    add_one = add(1)
    assert callable(add_one)
    assert add_one(2, 3) == 6

    add_three = add(1, 2)
    assert callable(add_three)
    assert add_three(3) == 6


def test_curry_two_args():
    @curry
    def multiply(a, b):
        return a * b

    assert multiply(3, 4) == 12
    assert multiply(3)(4) == 12

    double = multiply(2)
    assert double(5) == 10
    assert double(10) == 20
