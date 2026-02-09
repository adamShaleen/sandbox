# ============================================================================
# PHASE 5: Iterators & Generators - PROBLEMS
# ============================================================================
# Practice problems for Phase 5 concepts.
# Run tests: npm run test:py -- python/phase5/problems.py


# -----------------------------------------------------------------------------
# PROBLEM 1: range_gen
# -----------------------------------------------------------------------------
# Create a generator function `range_gen(start, stop, step=1)` that works
# like the built-in range() but implemented as a generator.
#
# Example:
#   list(range_gen(1, 5)) -> [1, 2, 3, 4]
#   list(range_gen(0, 10, 2)) -> [0, 2, 4, 6, 8]
#
# JS equivalent: function* range(start, stop, step=1) { ... }
#
# Hints:
# - Use while loop with yield
# - Handle positive steps (start < stop)
# - Bonus: handle negative steps too
#


def range_gen(start, stop, step=1):
    current = start

    if step > 0:
        while current < stop:
            yield current
            current += step
    else:
        while current > stop:
            yield current
            current += step


def test_range_gen():
    # Basic usage
    assert list(range_gen(0, 5)) == [0, 1, 2, 3, 4]

    # With step
    assert list(range_gen(0, 10, 2)) == [0, 2, 4, 6, 8]

    # Starting from non-zero
    assert list(range_gen(5, 10)) == [5, 6, 7, 8, 9]

    # Empty range
    assert list(range_gen(5, 5)) == []

    # Verify it's a generator
    gen = range_gen(0, 3)
    assert next(gen) == 0
    assert next(gen) == 1


def test_range_gen_negative_step():
    # Negative step (bonus)
    assert list(range_gen(5, 0, -1)) == [5, 4, 3, 2, 1]
    assert list(range_gen(10, 0, -2)) == [10, 8, 6, 4, 2]


# -----------------------------------------------------------------------------
# PROBLEM 2: take
# -----------------------------------------------------------------------------
# Create a generator function `take(n, iterable)` that yields the first
# n items from an iterable.
#
# Example:
#   list(take(3, [1, 2, 3, 4, 5])) -> [1, 2, 3]
#   list(take(2, "hello")) -> ['h', 'e']
#
# JS equivalent: arr.slice(0, n) but lazy
#
# Hints:
# - enumerate() gives you the index
# - Or use a counter
# - Works on any iterable, not just lists
#


def take(n, iterable):
    for index, item in enumerate(iterable):
        if index >= n:
            return
        yield item


def test_take():
    # Basic usage
    assert list(take(3, [1, 2, 3, 4, 5])) == [1, 2, 3]

    # Take more than available
    assert list(take(10, [1, 2, 3])) == [1, 2, 3]

    # Take zero
    assert list(take(0, [1, 2, 3])) == []

    # Works with generators (infinite)
    def naturals():
        n = 1
        while True:
            yield n
            n += 1

    assert list(take(5, naturals())) == [1, 2, 3, 4, 5]


# -----------------------------------------------------------------------------
# PROBLEM 3: drop
# -----------------------------------------------------------------------------
# Create a generator function `drop(n, iterable)` that skips the first
# n items and yields the rest.
#
# Example:
#   list(drop(2, [1, 2, 3, 4, 5])) -> [3, 4, 5]
#
# JS equivalent: arr.slice(n) but lazy
#
# Hints:
# - Skip first n items (use enumerate or counter)
# - Yield all remaining items
#


def drop(n, iterable):
    for index, item in enumerate(iterable):
        if index >= n:
            yield item


def test_drop():
    # Basic usage
    assert list(drop(2, [1, 2, 3, 4, 5])) == [3, 4, 5]

    # Drop all
    assert list(drop(10, [1, 2, 3])) == []

    # Drop zero
    assert list(drop(0, [1, 2, 3])) == [1, 2, 3]

    # Works with strings
    assert list(drop(3, "hello")) == ["l", "o"]


# -----------------------------------------------------------------------------
# PROBLEM 4: chunks
# -----------------------------------------------------------------------------
# Create a generator function `chunks(iterable, size)` that yields
# successive chunks of the given size.
#
# Example:
#   list(chunks([1, 2, 3, 4, 5], 2)) -> [[1, 2], [3, 4], [5]]
#   list(chunks("abcdefg", 3)) -> [['a', 'b', 'c'], ['d', 'e', 'f'], ['g']]
#
# JS equivalent: Lodash's _.chunk()
#
# Hints:
# - Accumulate items into a list until it reaches size
# - yield the chunk, start a new one
# - Don't forget the last chunk if it's not full!
#


def chunks(iterable, size):
    current_chunk = []

    for item in iterable:
        current_chunk.append(item)
        if len(current_chunk) == size:
            yield current_chunk
            current_chunk = []

    if current_chunk:
        yield current_chunk


def test_chunks():
    # Even split
    assert list(chunks([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    # Uneven split
    assert list(chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]

    # Chunk larger than input
    assert list(chunks([1, 2], 5)) == [[1, 2]]

    # Empty input
    assert list(chunks([], 3)) == []

    # Works with strings
    result = list(chunks("abcde", 2))
    assert result == [["a", "b"], ["c", "d"], ["e"]]


# -----------------------------------------------------------------------------
# PROBLEM 5: flatten_gen
# -----------------------------------------------------------------------------
# Create a generator function `flatten_gen(nested)` that flattens
# nested iterables one level deep.
#
# Example:
#   list(flatten_gen([[1, 2], [3, 4], [5]])) -> [1, 2, 3, 4, 5]
#
# JS equivalent: arr.flat()
#
# Hints:
# - Use yield from to yield items from each sublist
# - Only flatten one level (not recursive)
#


def flatten_gen(nested):
    for inner in nested:
        yield from inner


def test_flatten_gen():
    # Basic flattening
    assert list(flatten_gen([[1, 2], [3, 4], [5]])) == [1, 2, 3, 4, 5]

    # Mixed sizes
    assert list(flatten_gen([[1], [2, 3, 4], [], [5, 6]])) == [1, 2, 3, 4, 5, 6]

    # Empty input
    assert list(flatten_gen([])) == []

    # Single nested list
    assert list(flatten_gen([[1, 2, 3]])) == [1, 2, 3]


# -----------------------------------------------------------------------------
# PROBLEM 6: window
# -----------------------------------------------------------------------------
# Create a generator function `window(iterable, size)` that yields
# sliding windows of the given size.
#
# Example:
#   list(window([1, 2, 3, 4, 5], 3))
#   -> [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
#
# JS equivalent: No built-in, but common utility
#
# Hints:
# - Use collections.deque with maxlen for efficient sliding
# - Or accumulate into a list and slice
# - Only yield when window is full
#

from collections import deque


def window(iterable, size):
    sliding_window = deque(maxlen=size)

    for item in iterable:
        sliding_window.append(item)
        if len(sliding_window) == size:
            yield tuple(sliding_window)


def test_window():
    # Basic window
    result = list(window([1, 2, 3, 4, 5], 3))
    assert result == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    # Window of 2
    result = list(window([1, 2, 3, 4], 2))
    assert result == [(1, 2), (2, 3), (3, 4)]

    # Window equals size
    assert list(window([1, 2, 3], 3)) == [(1, 2, 3)]

    # Window larger than input
    assert list(window([1, 2], 3)) == []

    # Works with strings
    result = list(window("abcd", 2))
    assert result == [("a", "b"), ("b", "c"), ("c", "d")]


# -----------------------------------------------------------------------------
# PROBLEM 7: unique_gen
# -----------------------------------------------------------------------------
# Create a generator function `unique_gen(iterable)` that yields only
# unique items, preserving order.
#
# Example:
#   list(unique_gen([1, 2, 1, 3, 2, 4])) -> [1, 2, 3, 4]
#
# JS equivalent: [...new Set(arr)] but as a generator
#
# Hints:
# - Track seen items in a set
# - Only yield if not seen before
#


def unique_gen(iterable):
    seen = set()

    for item in iterable:
        if item not in seen:
            yield item
            seen.add(item)


def test_unique_gen():
    # Remove duplicates, preserve order
    assert list(unique_gen([1, 2, 1, 3, 2, 4])) == [1, 2, 3, 4]

    # All unique
    assert list(unique_gen([1, 2, 3])) == [1, 2, 3]

    # All same
    assert list(unique_gen([1, 1, 1])) == [1]

    # Empty
    assert list(unique_gen([])) == []

    # Strings
    assert list(unique_gen("mississippi")) == ["m", "i", "s", "p"]


# -----------------------------------------------------------------------------
# PROBLEM 8: interleave
# -----------------------------------------------------------------------------
# Create a generator function `interleave(*iterables)` that yields items
# from each iterable in turn, round-robin style.
#
# Example:
#   list(interleave([1, 2, 3], ['a', 'b', 'c']))
#   -> [1, 'a', 2, 'b', 3, 'c']
#
# Stops when the shortest iterable is exhausted.
#
# JS equivalent: zip then flat, but lazy
#
# Hints:
# - zip(*iterables) gives you tuples of corresponding items
# - yield from each tuple
#


def interleave(*iterables):
    for tuple in zip(
        *iterables
    ):  # A zip object yielding tuples until an input is exhausted.
        yield from tuple


def test_interleave():
    # Two iterables
    result = list(interleave([1, 2, 3], ["a", "b", "c"]))
    assert result == [1, "a", 2, "b", 3, "c"]

    # Three iterables
    result = list(interleave([1, 2], ["a", "b"], ["x", "y"]))
    assert result == [1, "a", "x", 2, "b", "y"]

    # Unequal lengths (stops at shortest)
    result = list(interleave([1, 2, 3], ["a", "b"]))
    assert result == [1, "a", 2, "b"]

    # Single iterable
    assert list(interleave([1, 2, 3])) == [1, 2, 3]


# -----------------------------------------------------------------------------
# PROBLEM 9: cycle_n
# -----------------------------------------------------------------------------
# Create a generator function `cycle_n(iterable, n)` that cycles through
# an iterable n times.
#
# Example:
#   list(cycle_n([1, 2, 3], 2)) -> [1, 2, 3, 1, 2, 3]
#
# JS equivalent: No built-in
#
# Hints:
# - itertools.cycle goes forever - this is bounded
# - Loop n times, yield from iterable each time
# - Careful: need to convert iterable to list if you want to reuse it!
#


def cycle_n(iterable, n):
    items = list(iterable)

    for _ in range(n):
        yield from items


def test_cycle_n():
    # Cycle twice
    assert list(cycle_n([1, 2, 3], 2)) == [1, 2, 3, 1, 2, 3]

    # Cycle once (same as original)
    assert list(cycle_n([1, 2], 1)) == [1, 2]

    # Cycle zero times
    assert list(cycle_n([1, 2, 3], 0)) == []

    # Works with generator input (must cache!)
    def gen():
        yield 1
        yield 2

    assert list(cycle_n(gen(), 3)) == [1, 2, 1, 2, 1, 2]


# -----------------------------------------------------------------------------
# PROBLEM 10: Iterator class - Counter
# -----------------------------------------------------------------------------
# Create a class `Counter` that is an iterator counting from start by step.
# Implements the iterator protocol (__iter__ and __next__).
# Has an optional `limit` - if provided, stops at limit (exclusive).
#
# Example:
#   c = Counter(1, 2, limit=10)
#   list(c) -> [1, 3, 5, 7, 9]
#
# Hints:
# - __iter__ returns self
# - __next__ returns next value or raises StopIteration
# - Check limit if provided
#


class Counter:
    def __init__(self, start=0, step=1, limit=None):
        self.current = start
        self.step = step
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit and self.current >= self.limit:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


def test_counter():
    # Basic counting
    c = Counter(0, 1, limit=5)
    assert list(c) == [0, 1, 2, 3, 4]

    # Custom step
    c = Counter(0, 2, limit=10)
    assert list(c) == [0, 2, 4, 6, 8]

    # Custom start
    c = Counter(5, 1, limit=8)
    assert list(c) == [5, 6, 7]

    # No limit (careful - don't list() this!)
    c = Counter(1, 1)
    assert next(c) == 1
    assert next(c) == 2
    assert next(c) == 3


# -----------------------------------------------------------------------------
# PROBLEM 11: file_lines (Practical)
# -----------------------------------------------------------------------------
# Create a generator function `file_lines(filepath)` that yields lines
# from a file one at a time (stripped of whitespace).
#
# This demonstrates the memory efficiency of generators - can process
# huge files without loading them entirely into memory.
#
# Example:
#   for line in file_lines("data.txt"):
#       print(line)
#
# Hints:
# - open() returns an iterable of lines
# - Use `with` for proper file handling
# - strip() each line
#


def file_lines(filepath):
    with open(filepath) as lines: # with ensures the file closes when the generator exhausts or is garbage collected
        for line in lines:
            yield line.strip()


def test_file_lines(tmp_path):
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("line 1\n  line 2  \nline 3\n")

    # Read with generator
    result = list(file_lines(str(test_file)))
    assert result == ["line 1", "line 2", "line 3"]


# -----------------------------------------------------------------------------
# PROBLEM 12: batch_processor (Practical)
# -----------------------------------------------------------------------------
# Create a generator function `batch_processor(items, batch_size, process_fn)`
# that:
#   1. Groups items into batches of batch_size
#   2. Applies process_fn to each batch
#   3. Yields processed batches
#
# Example:
#   items = [1, 2, 3, 4, 5, 6, 7]
#   result = batch_processor(items, 3, lambda batch: sum(batch))
#   list(result) -> [6, 15, 7]  # sum([1,2,3]), sum([4,5,6]), sum([7])
#
# Hints:
# - Reuse your chunks() function
# - Apply process_fn to each chunk
#


def batch_processor(items, batch_size, process_fn):
    for chunk in chunks(items, batch_size):
        yield process_fn(chunk)

        
def test_batch_processor():
    items = [1, 2, 3, 4, 5, 6, 7]

    # Sum each batch
    result = list(batch_processor(items, 3, sum))
    assert result == [6, 15, 7]

    # Max of each batch
    result = list(batch_processor(items, 2, max))
    assert result == [2, 4, 6, 7]

    # Join strings in batches
    strings = ["a", "b", "c", "d", "e"]
    result = list(batch_processor(strings, 2, lambda b: "".join(b)))
    assert result == ["ab", "cd", "e"]
