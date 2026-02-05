# ============================================================================
# PHASE 5: Iterators & Generators - LESSONS
# ============================================================================
# Iterators and generators are Python's lazy evaluation primitives.
# They let you work with sequences without loading everything into memory.
# JS equivalent: generators (function*) and iterators, but Python uses them MORE.

# -----------------------------------------------------------------------------
# 1. ITERABLES vs ITERATORS
# -----------------------------------------------------------------------------
# Iterable: anything you can loop over (list, str, dict, range, file, etc.)
# Iterator: an object that produces values one at a time via __next__()
#
# Key insight: an iterable creates an iterator when you loop over it.
# You can have multiple iterators over the same iterable.


def test_iterable_vs_iterator():
    # A list is ITERABLE (can be looped over)
    nums = [1, 2, 3]

    # iter() gets an ITERATOR from an iterable
    iterator = iter(nums)

    # next() gets the next value from an iterator
    assert next(iterator) == 1
    assert next(iterator) == 2
    assert next(iterator) == 3

    # StopIteration is raised when exhausted
    try:
        next(iterator)
        assert False, "Should have raised StopIteration"
    except StopIteration:
        pass  # Expected!

    # The original list is unchanged - iterator is separate
    assert nums == [1, 2, 3]


def test_multiple_iterators():
    nums = [1, 2, 3]

    # Each iter() call creates a NEW independent iterator
    iter1 = iter(nums)
    iter2 = iter(nums)

    assert next(iter1) == 1
    assert next(iter1) == 2
    assert next(iter2) == 1  # iter2 is independent!


# -----------------------------------------------------------------------------
# 2. THE ITERATOR PROTOCOL
# -----------------------------------------------------------------------------
# An iterator must implement:
#   __iter__() - returns self (iterators are also iterable)
#   __next__() - returns next value or raises StopIteration
#
# JS equivalent: Symbol.iterator and next()


def test_iterator_protocol():
    class CountUp:
        """Iterator that counts from start to end."""

        def __init__(self, start, end):
            self.current = start
            self.end = end

        def __iter__(self):
            return self  # Iterators return themselves

        def __next__(self):
            if self.current >= self.end:
                raise StopIteration
            value = self.current
            self.current += 1
            return value

    # Can use in for loop (which calls iter() then next() repeatedly)
    result = []
    for n in CountUp(1, 4):
        result.append(n)
    assert result == [1, 2, 3]

    # Can also use iter/next manually
    counter = CountUp(10, 13)
    assert next(counter) == 10
    assert next(counter) == 11


# -----------------------------------------------------------------------------
# 3. BUILT-IN ITERATORS
# -----------------------------------------------------------------------------
# Many Python functions return iterators, not lists.
# This is LAZY - values computed on demand, not all at once.


def test_builtin_iterators():
    # range() returns an iterator-like object (actually a sequence)
    r = range(5)
    assert list(r) == [0, 1, 2, 3, 4]

    # map() returns an iterator
    mapped = map(lambda x: x * 2, [1, 2, 3])
    assert next(mapped) == 2
    assert next(mapped) == 4

    # filter() returns an iterator
    filtered = filter(lambda x: x > 2, [1, 2, 3, 4])
    assert next(filtered) == 3

    # zip() returns an iterator
    zipped = zip([1, 2], ["a", "b"])
    assert next(zipped) == (1, "a")

    # enumerate() returns an iterator
    enumerated = enumerate(["a", "b"])
    assert next(enumerated) == (0, "a")

    # reversed() returns an iterator
    rev = reversed([1, 2, 3])
    assert next(rev) == 3


# -----------------------------------------------------------------------------
# 4. GENERATORS - THE EASY WAY
# -----------------------------------------------------------------------------
# Writing iterator classes is verbose. Generators are simpler!
# A generator function uses `yield` instead of `return`.
# Each yield pauses the function and produces a value.
#
# JS equivalent: function* and yield


def test_generator_basics():
    def count_up(start, end):
        """Generator function - note the yield keyword."""
        current = start
        while current < end:
            yield current  # Pause here, produce value
            current += 1
        # Function ends = StopIteration raised automatically

    # Calling a generator function returns a generator object
    gen = count_up(1, 4)
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3

    # StopIteration when exhausted
    try:
        next(gen)
        assert False
    except StopIteration:
        pass

    # Can use in for loop
    assert list(count_up(1, 4)) == [1, 2, 3]


def test_generator_vs_return():
    # Regular function: computes ALL values, returns list
    def get_squares_list(n):
        result = []
        for i in range(n):
            result.append(i**2)
        return result  # All values computed and stored

    # Generator: computes ONE value at a time
    def get_squares_gen(n):
        for i in range(n):
            yield i**2  # Compute and yield one value

    # Both produce same results
    assert get_squares_list(5) == [0, 1, 4, 9, 16]
    assert list(get_squares_gen(5)) == [0, 1, 4, 9, 16]

    # But generator uses O(1) memory, list uses O(n)


# -----------------------------------------------------------------------------
# 5. GENERATOR EXPRESSIONS
# -----------------------------------------------------------------------------
# List comprehension: [expr for x in iterable] -> creates list
# Generator expression: (expr for x in iterable) -> creates generator
#
# Just change [] to ()!


def test_generator_expressions():
    # List comprehension - creates list immediately
    squares_list = [x**2 for x in range(5)]
    assert squares_list == [0, 1, 4, 9, 16]
    assert type(squares_list) == list

    # Generator expression - creates generator (lazy)
    squares_gen = (x**2 for x in range(5))
    assert type(squares_gen).__name__ == "generator"

    # Generator produces values on demand
    assert next(squares_gen) == 0
    assert next(squares_gen) == 1

    # Can convert to list
    remaining = list(squares_gen)
    assert remaining == [4, 9, 16]  # Only remaining values!


def test_generator_expression_memory():
    # Generator expressions are memory efficient
    # This creates a generator, NOT a billion-element list:
    big_gen = (x for x in range(1_000_000_000))

    # Only computes values as needed
    assert next(big_gen) == 0
    assert next(big_gen) == 1
    # The other 999,999,998 values were never computed!


# -----------------------------------------------------------------------------
# 6. YIELD FROM
# -----------------------------------------------------------------------------
# `yield from iterable` yields each item from another iterable.
# Cleaner than `for x in iterable: yield x`


def test_yield_from():
    def flatten(nested):
        for sublist in nested:
            yield from sublist  # Yield each item from sublist

    nested = [[1, 2], [3, 4], [5]]
    assert list(flatten(nested)) == [1, 2, 3, 4, 5]

    # Without yield from, you'd write:
    def flatten_verbose(nested):
        for sublist in nested:
            for item in sublist:
                yield item

    assert list(flatten_verbose(nested)) == [1, 2, 3, 4, 5]


def test_yield_from_delegation():
    def inner():
        yield 1
        yield 2

    def outer():
        yield "start"
        yield from inner()  # Delegate to inner generator
        yield "end"

    assert list(outer()) == ["start", 1, 2, "end"]


# -----------------------------------------------------------------------------
# 7. INFINITE GENERATORS
# -----------------------------------------------------------------------------
# Generators can be infinite - they just keep yielding.
# Only compute what you need!


def test_infinite_generators():
    def naturals():
        """Infinite generator of natural numbers."""
        n = 1
        while True:
            yield n
            n += 1

    gen = naturals()
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3
    # Could keep going forever...

    # Take first 5
    gen = naturals()
    first_five = [next(gen) for _ in range(5)]
    assert first_five == [1, 2, 3, 4, 5]


def test_infinite_fibonacci():
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    fib = fibonacci()
    first_ten = [next(fib) for _ in range(10)]
    assert first_ten == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# -----------------------------------------------------------------------------
# 8. ITERTOOLS - THE ITERATOR TOOLKIT
# -----------------------------------------------------------------------------
# itertools provides powerful iterator building blocks.
# All lazy, all composable.

import itertools


def test_itertools_count():
    # count(start, step) - infinite counter
    counter = itertools.count(10, 2)
    assert next(counter) == 10
    assert next(counter) == 12
    assert next(counter) == 14


def test_itertools_cycle():
    # cycle(iterable) - repeat forever
    colors = itertools.cycle(["red", "green", "blue"])
    assert next(colors) == "red"
    assert next(colors) == "green"
    assert next(colors) == "blue"
    assert next(colors) == "red"  # Cycles back!


def test_itertools_repeat():
    # repeat(value, times) - repeat value
    fives = itertools.repeat(5, 3)
    assert list(fives) == [5, 5, 5]


def test_itertools_chain():
    # chain(*iterables) - concatenate iterators
    a = [1, 2]
    b = [3, 4]
    c = [5]
    assert list(itertools.chain(a, b, c)) == [1, 2, 3, 4, 5]


def test_itertools_islice():
    # islice(iterable, stop) or islice(iterable, start, stop, step)
    # Like slicing, but for iterators
    naturals = itertools.count(1)
    first_five = list(itertools.islice(naturals, 5))
    assert first_five == [1, 2, 3, 4, 5]

    # With start and stop
    naturals = itertools.count(1)
    third_to_seventh = list(itertools.islice(naturals, 2, 7))
    assert third_to_seventh == [3, 4, 5, 6, 7]


def test_itertools_takewhile_dropwhile():
    nums = [1, 3, 5, 2, 4, 6]

    # takewhile - take while predicate is true
    taken = list(itertools.takewhile(lambda x: x < 5, nums))
    assert taken == [1, 3]  # Stops at 5

    # dropwhile - drop while predicate is true, yield rest
    dropped = list(itertools.dropwhile(lambda x: x < 5, nums))
    assert dropped == [5, 2, 4, 6]  # Starts at 5


def test_itertools_groupby():
    # groupby(iterable, key) - group consecutive items by key
    # IMPORTANT: input must be sorted by key first!
    data = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("a", 5)]

    # Group by first element
    groups = []
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        groups.append((key, list(group)))

    assert groups == [
        ("a", [("a", 1), ("a", 2)]),
        ("b", [("b", 3), ("b", 4)]),
        ("a", [("a", 5)]),  # New group because not consecutive!
    ]


def test_itertools_combinations_permutations():
    # combinations - all r-length combinations (no repetition)
    combs = list(itertools.combinations([1, 2, 3], 2))
    assert combs == [(1, 2), (1, 3), (2, 3)]

    # permutations - all r-length permutations (order matters)
    perms = list(itertools.permutations([1, 2, 3], 2))
    assert perms == [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

    # product - cartesian product
    prod = list(itertools.product([1, 2], ["a", "b"]))
    assert prod == [(1, "a"), (1, "b"), (2, "a"), (2, "b")]


# -----------------------------------------------------------------------------
# 9. GENERATOR PIPELINES
# -----------------------------------------------------------------------------
# Chain generators together for lazy data processing.
# Like Unix pipes, but in Python.


def test_generator_pipeline():
    # Each stage is a generator that transforms data
    def read_data():
        yield from [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def filter_even(nums):
        for n in nums:
            if n % 2 == 0:
                yield n

    def square(nums):
        for n in nums:
            yield n**2

    def take(n, iterable):
        for i, item in enumerate(iterable):
            if i >= n:
                break
            yield item

    # Pipeline: read -> filter even -> square -> take 3
    pipeline = take(3, square(filter_even(read_data())))
    assert list(pipeline) == [4, 16, 36]  # 2², 4², 6²


# -----------------------------------------------------------------------------
# 10. CONSUMING ITERATORS
# -----------------------------------------------------------------------------
# Various ways to consume/use iterators


def test_consuming_iterators():
    def gen():
        yield 1
        yield 2
        yield 3

    # list() - collect all into list
    assert list(gen()) == [1, 2, 3]

    # sum(), max(), min() - aggregations
    assert sum(gen()) == 6
    assert max(gen()) == 3
    assert min(gen()) == 1

    # any(), all() - boolean aggregations
    assert any(x > 2 for x in gen())  # At least one > 2?
    assert all(x > 0 for x in gen())  # All > 0?

    # join() - strings
    assert "".join(str(x) for x in gen()) == "123"

    # Unpacking
    a, b, c = gen()
    assert (a, b, c) == (1, 2, 3)


# -----------------------------------------------------------------------------
# 11. ITERATOR GOTCHAS
# -----------------------------------------------------------------------------


def test_iterator_exhaustion():
    # Iterators can only be consumed ONCE
    gen = (x**2 for x in range(3))

    assert list(gen) == [0, 1, 4]
    assert list(gen) == []  # Empty! Already exhausted.

    # If you need multiple passes, convert to list first
    # Or create a new generator each time


def test_iterator_consumption_side_effects():
    gen = (x for x in range(5))

    # any() consumes until it finds True
    assert any(x > 2 for x in gen)  # Consumes 0, 1, 2, 3

    # gen is now partially consumed!
    assert list(gen) == [4]  # Only 4 left


# -----------------------------------------------------------------------------
# SUMMARY: When to use what
# -----------------------------------------------------------------------------
# - Generator function (yield): when you need custom iteration logic
# - Generator expression (x for x in ...): simple transformations
# - itertools: complex iteration patterns (combinations, chaining, etc.)
# - list comprehension: when you need the full list in memory
# - Iterator class: rare, only for complex stateful iteration
#
# Memory rule:
# - Processing a file? Generator (one line at a time)
# - Need random access? List
# - Chaining operations? Generator pipeline
# - Infinite sequence? Generator (obviously)
