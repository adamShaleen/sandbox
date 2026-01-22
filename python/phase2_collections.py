# ============================================================================
# PHASE 2: Collections & Comprehensions
# ============================================================================
# Python's collection types and comprehensions are a major superpower.
# This is where Python really shines vs JS.

# -----------------------------------------------------------------------------
# 1. COLLECTION TYPES
# -----------------------------------------------------------------------------
# JS has: Array, Object, Map, Set
# Python has: list, dict, tuple, set
#
#   JS              Python          Notes
#   -----------     -----------     --------------------------------
#   []              []              list - mutable, ordered
#   {}              {}              dict - mutable, key-value pairs
#   new Set()       set()           set - mutable, unique values
#   (no equiv)      ()              tuple - IMMUTABLE list
#
# Tuple = like a list but can't be changed after creation
# Use when data shouldn't change (coordinates, RGB values, etc.)

my_list = [1, 2, 3]          # mutable
my_tuple = (1, 2, 3)         # immutable - can't append/remove
my_set = {1, 2, 3}           # unique values only
my_dict = {"a": 1, "b": 2}   # key-value pairs


def test_collection_types():
    # List - mutable
    nums = [1, 2, 3]
    nums.append(4)
    assert nums == [1, 2, 3, 4]

    # Tuple - immutable (can't modify)
    point = (10, 20)
    x, y = point  # unpacking works
    assert x == 10 and y == 20

    # Set - unique values, no duplicates
    unique = {1, 2, 2, 3, 3, 3}
    assert unique == {1, 2, 3}

    # Dict
    person = {"name": "Alice", "age": 30}
    assert person["name"] == "Alice"


# -----------------------------------------------------------------------------
# 2. LIST COMPREHENSIONS
# -----------------------------------------------------------------------------
# JS:  arr.map(x => x * 2)
# Py:  [x * 2 for x in arr]
#
# JS:  arr.filter(x => x > 2)
# Py:  [x for x in arr if x > 2]
#
# JS:  arr.filter(x => x > 2).map(x => x * 2)
# Py:  [x * 2 for x in arr if x > 2]
#
# Pattern: [expression for item in iterable if condition]


def test_list_comprehensions():
    nums = [1, 2, 3, 4, 5]

    # Map equivalent
    doubled = [x * 2 for x in nums]
    assert doubled == [2, 4, 6, 8, 10]

    # Filter equivalent
    evens = [x for x in nums if x % 2 == 0]
    assert evens == [2, 4]

    # Filter + Map
    doubled_evens = [x * 2 for x in nums if x % 2 == 0]
    assert doubled_evens == [4, 8]

    # String manipulation
    words = ["hello", "world"]
    uppers = [w.upper() for w in words]
    assert uppers == ["HELLO", "WORLD"]


# -----------------------------------------------------------------------------
# 3. DICT COMPREHENSIONS
# -----------------------------------------------------------------------------
# Create dicts with a similar pattern
# Pattern: {key_expr: value_expr for item in iterable if condition}


def test_dict_comprehensions():
    # Create dict from list
    words = ["apple", "banana", "cherry"]
    lengths = {word: len(word) for word in words}
    assert lengths == {"apple": 5, "banana": 6, "cherry": 6}

    # Filter while creating
    nums = [1, 2, 3, 4, 5]
    even_squares = {x: x**2 for x in nums if x % 2 == 0}
    assert even_squares == {2: 4, 4: 16}

    # Swap keys and values
    original = {"a": 1, "b": 2}
    swapped = {v: k for k, v in original.items()}
    assert swapped == {1: "a", 2: "b"}


# -----------------------------------------------------------------------------
# 4. SET COMPREHENSIONS
# -----------------------------------------------------------------------------
# Same pattern with curly braces (no colon = set, not dict)


def test_set_comprehensions():
    words = ["hello", "world", "hello"]
    unique_lengths = {len(w) for w in words}
    assert unique_lengths == {5}  # all words are length 5


# -----------------------------------------------------------------------------
# 5. SLICING
# -----------------------------------------------------------------------------
# JS:  arr.slice(1, 3)
# Py:  arr[1:3]
#
# Syntax: arr[start:stop:step]
# - start: inclusive (default 0)
# - stop: exclusive (default len)
# - step: increment (default 1)


def test_slicing():
    nums = [0, 1, 2, 3, 4, 5]

    assert nums[1:4] == [1, 2, 3]      # index 1 to 3
    assert nums[:3] == [0, 1, 2]       # first 3
    assert nums[3:] == [3, 4, 5]       # from index 3 to end
    assert nums[-2:] == [4, 5]         # last 2
    assert nums[::2] == [0, 2, 4]      # every 2nd item
    assert nums[::-1] == [5, 4, 3, 2, 1, 0]  # reversed!

    # Works on strings too
    text = "hello"
    assert text[1:4] == "ell"
    assert text[::-1] == "olleh"


# -----------------------------------------------------------------------------
# 6. USEFUL BUILT-INS: enumerate, zip, map, filter
# -----------------------------------------------------------------------------


def test_enumerate():
    # JS: arr.forEach((item, index) => ...)
    # Py: for index, item in enumerate(arr):

    words = ["a", "b", "c"]
    result = []
    for i, word in enumerate(words):
        result.append(f"{i}:{word}")
    assert result == ["0:a", "1:b", "2:c"]

    # With list comprehension
    indexed = [f"{i}:{w}" for i, w in enumerate(words)]
    assert indexed == ["0:a", "1:b", "2:c"]


def test_zip():
    # Combine multiple lists element-wise
    names = ["Alice", "Bob"]
    ages = [30, 25]

    # JS: names.map((name, i) => ({ name, age: ages[i] }))
    pairs = list(zip(names, ages))
    assert pairs == [("Alice", 30), ("Bob", 25)]

    # Common pattern: create dict from two lists
    name_to_age = dict(zip(names, ages))
    assert name_to_age == {"Alice": 30, "Bob": 25}


def test_unpacking():
    # Unpack into variables
    a, b, c = [1, 2, 3]
    assert a == 1 and b == 2 and c == 3

    # Rest operator (*) - like JS spread
    first, *rest = [1, 2, 3, 4]
    assert first == 1
    assert rest == [2, 3, 4]

    # Works in middle too
    first, *middle, last = [1, 2, 3, 4, 5]
    assert first == 1
    assert middle == [2, 3, 4]
    assert last == 5


# -----------------------------------------------------------------------------
# PRACTICE: Matrix Transpose
# -----------------------------------------------------------------------------
# Given a 2D list (matrix), return its transpose.
# Transpose = rows become columns, columns become rows.
#
# Example:
#   [[1, 2, 3],       [[1, 4],
#    [4, 5, 6]]  -->   [2, 5],
#                      [3, 6]]
#
# Hints:
# - zip(*matrix) unpacks rows and zips them together
# - list() converts zip result to list
# - You'll need nested comprehension or list(zip(...))
#
# JS equivalent:
# function transpose(matrix) {
#   return matrix[0].map((_, colIdx) =>
#     matrix.map(row => row[colIdx])
#   );
# }

def transpose(matrix: list[list[int]]) -> list[list[int]]:
    # Example: matrix = [[1, 2, 3], [4, 5, 6]]

    # Step 1: *matrix unpacks the outer list into separate arguments
    # zip(*matrix) is equivalent to:
    # zip([1, 2, 3], [4, 5, 6])

    # Step 2: zip() pairs up items at the same index
    # zip([1, 2, 3], [4, 5, 6]) → (1,4), (2,5), (3,6)
    #      ↑           ↑           row0   row1   row2  ← these become new rows
    #     col0        col1

    # Step 3: zip returns tuples, but we need lists
    # list(x) converts each tuple (1,4) → [1,4]

    # Step 4: list comprehension collects all converted rows
    # Result: [[1,4], [2,5], [3,6]]

    return [list(x) for x in zip(*matrix)]

def test_transpose():
    assert transpose([[1]]) == [[1]]
    assert transpose([[1, 2]]) == [[1], [2]]
    assert transpose([[1], [2]]) == [[1, 2]]
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
