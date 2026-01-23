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

my_list = [1, 2, 3]  # mutable
my_tuple = (1, 2, 3)  # immutable - can't append/remove
my_set = {1, 2, 3}  # unique values only
my_dict = {"a": 1, "b": 2}  # key-value pairs


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
# COMPREHENSION STRUCTURE - reads like an English sentence:
# "give me [WHAT] for each [ITEM] in [SOURCE] if [CONDITION]"
#
# [ WHAT_TO_COLLECT   for ITEM in SOURCE   if CONDITION ]
#         ↓                 ↓                    ↓
#     expression         loop                 filter (optional)
#
# Single loop:
#   [x * 2 for x in nums]           → "x*2 for each x in nums"
#   [x for x in nums if x > 2]      → "x for each x in nums if x > 2"
#
# Nested loops (for 2D lists):
#   [item for row in matrix for item in row]
#          ↑ outer loop      ↑ inner loop
#   → "item for each row in matrix, for each item in row"


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

    assert nums[1:4] == [1, 2, 3]  # index 1 to 3
    assert nums[:3] == [0, 1, 2]  # first 3
    assert nums[3:] == [3, 4, 5]  # from index 3 to end
    assert nums[-2:] == [4, 5]  # last 2
    assert nums[::2] == [0, 2, 4]  # every 2nd item
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
# 7. max/min/sorted WITH key=
# -----------------------------------------------------------------------------
# key= tells these functions HOW to compare items
# It's a function that extracts the comparison value
#
# max(iterable, key=function)
#              ↑ "compare by what?"
#
# lambda = inline anonymous function:
#   lambda x: x[1]   is equivalent to   def func(x): return x[1]
#
# Examples:
#   words = ["banana", "pie", "apple"]
#
#   max(words, key=len)              → "banana" (longest)
#   min(words, key=len)              → "pie" (shortest)
#   sorted(words, key=len)           → ["pie", "apple", "banana"]
#
#   max(words, key=lambda w: w[-1])  → "pie" (highest last letter)
#
# Common key functions:
#   key=len          # by length
#   key=str.lower    # case-insensitive
#   key=abs          # by absolute value
#   key=lambda x: x[1]  # by second element (for tuples/lists)


def test_max_min_with_key():
    words = ["banana", "pie", "apple"]

    assert max(words, key=len) == "banana"
    assert min(words, key=len) == "pie"
    assert sorted(words, key=len) == ["pie", "apple", "banana"]

    # With dict - find key with highest value
    scores = {"alice": 85, "bob": 92, "carol": 78}
    assert max(scores, key=lambda k: scores[k]) == "bob"


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


# -----------------------------------------------------------------------------
# PRACTICE: Flatten and Filter
# -----------------------------------------------------------------------------
# Given a 2D list, flatten it to 1D and keep only values that pass a condition.
#
# Example:
#   flatten_evens([[1, 2, 3], [4, 5, 6]]) → [2, 4, 6]
#
# Hints:
# - Nested comprehension: [item for row in matrix for item in row]
# - Add condition at the end: ... if item % 2 == 0
#
# JS equivalent:
# function flattenEvens(matrix) {
#   return matrix.flat().filter(x => x % 2 === 0);
# }


# Equivalent to nested for-loops:
#   result = []
#   for row in matrix:
#       for item in row:
#           if item % 2 == 0:
#               result.append(item)


def flatten_evens(matrix: list[list[int]]) -> list[int]:
    return [item for row in matrix for item in row if item % 2 == 0]


def test_flatten_evens():
    assert flatten_evens([]) == []
    assert flatten_evens([[]]) == []
    assert flatten_evens([[1, 2]]) == [2]
    assert flatten_evens([[1, 3, 5]]) == []
    assert flatten_evens([[1, 2, 3], [4, 5, 6]]) == [2, 4, 6]
    assert flatten_evens([[2, 4], [6, 8]]) == [2, 4, 6, 8]
    assert flatten_evens([[1], [2], [3], [4]]) == [2, 4]


# -----------------------------------------------------------------------------
# PRACTICE: Invert Dict
# -----------------------------------------------------------------------------
# Given a dict, swap keys and values. If multiple keys have the same value,
# collect them into a list.
#
# Example:
#   {"a": 1, "b": 2, "c": 1}  →  {1: ["a", "c"], 2: ["b"]}
#
# Hints:
# - You'll need to build a new dict
# - Check if a key already exists before deciding what to do
# - Consider what tools from this phase might help (comprehensions, .items(), etc.)
#
# JS equivalent:
# function invertDict(obj) {
#   return Object.entries(obj).reduce((acc, [k, v]) => {
#     acc[v] = acc[v] || [];
#     acc[v].push(k);
#     return acc;
#   }, {});
# }


def invert_dict_fancy(d: dict) -> dict[any, list]:
    output = {}

    # iterate over each item (key, value) in the dictionary
    for key, value in d.items():
        # setdefault: if key missing, create it with empty list; either way, return the list
        # append: add the key to that list (whether newly created or existing)
        output.setdefault(value, []).append(key)

    return output


def test_invert_dict_fancy():
    assert invert_dict_fancy({}) == {}
    assert invert_dict_fancy({"a": 1}) == {1: ["a"]}
    assert invert_dict_fancy({"a": 1, "b": 2}) == {1: ["a"], 2: ["b"]}
    assert invert_dict_fancy({"a": 1, "b": 1}) == {1: ["a", "b"]}
    assert invert_dict_fancy({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}
    assert invert_dict_fancy({"x": "foo", "y": "bar", "z": "foo"}) == {
        "foo": ["x", "z"],
        "bar": ["y"],
    }


# this was my first attempt without any help - it works but isn't as pythonic
def invert_dict(d: dict) -> dict[any, list]:
    output = {}

    for key, value in d.items():
        if output.get(value):
            output[value].append(key)
        else:
            output[value] = [key]

    return output


def test_invert_dict():
    assert invert_dict({}) == {}
    assert invert_dict({"a": 1}) == {1: ["a"]}
    assert invert_dict({"a": 1, "b": 2}) == {1: ["a"], 2: ["b"]}
    assert invert_dict({"a": 1, "b": 1}) == {1: ["a", "b"]}
    assert invert_dict({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}
    assert invert_dict({"x": "foo", "y": "bar", "z": "foo"}) == {
        "foo": ["x", "z"],
        "bar": ["y"],
    }


# -----------------------------------------------------------------------------
# PRACTICE: Merge Sorted Lists
# -----------------------------------------------------------------------------
# Given two sorted lists, merge them into a single sorted list.
# Do NOT use the built-in sorted() function.
#
# Example:
#   merge_sorted([1, 3, 5], [2, 4, 6]) → [1, 2, 3, 4, 5, 6]
#
# Hints:
# - Use two pointers (indices) to track position in each list
# - Compare elements at each pointer, take the smaller one
# - Handle leftover elements when one list is exhausted
# - Slicing can help grab remaining elements
#
# JS equivalent:
# function mergeSorted(a, b) {
#   const result = [];
#   let i = 0, j = 0;
#   while (i < a.length && j < b.length) {
#     if (a[i] <= b[j]) result.push(a[i++]);
#     else result.push(b[j++]);
#   }
#   return [...result, ...a.slice(i), ...b.slice(j)];
# }


def merge_sorted(list1: list[int], list2: list[int]) -> list[int]:
    output = []
    index_one = 0
    index_two = 0

    # compare elements while both lists have remaining items
    while index_one < len(list1) and index_two < len(list2):
        if list1[index_one] <= list2[index_two]:
            output.append(list1[index_one])
            index_one += 1  # only advance the list we took from
        else:
            output.append(list2[index_two])
            index_two += 1

    # one list is exhausted; append remaining elements from both
    # (one slice will be empty, the other has leftovers)
    return [*output, *list1[index_one:], *list2[index_two:]]


def test_merge_sorted():
    assert merge_sorted([], []) == []
    assert merge_sorted([1], []) == [1]
    assert merge_sorted([], [1]) == [1]
    assert merge_sorted([1], [2]) == [1, 2]
    assert merge_sorted([2], [1]) == [1, 2]
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([4, 5, 6], [1, 2, 3]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([1, 1, 1], [1, 1]) == [1, 1, 1, 1, 1]


# -----------------------------------------------------------------------------
# PRACTICE: Chunk List
# -----------------------------------------------------------------------------
# Split a list into chunks of a given size.
# The last chunk may be smaller if the list doesn't divide evenly.
#
# Example:
#   chunk([1, 2, 3, 4, 5], 2) → [[1, 2], [3, 4], [5]]
#
# Hints:
# - Think about slicing with a step: list[start:end]
# - range() can take a step argument: range(start, stop, step)
# - Consider what start and end values you need for each chunk
#
# JS equivalent:
# function chunk(arr, size) {
#   const result = [];
#   for (let i = 0; i < arr.length; i += size) {
#     result.push(arr.slice(i, i + size));
#   }
#   return result;
# }


def chunk(items: list, size: int) -> list[list]:
    output = []

    # range(0, len, size) → jumps by size: 0, 2, 4... (if size=2)
    for index in range(0, len(items), size):
        # slice from index to index+size; automatically stops at end
        output.append(items[index : index + size])

    return output

    # one-liner version:
    # [items[i:i + size] for i in range(0, len(items), size)]
    #  ↑                     ↑
    #  WHAT: slice chunk     LOOP: i = 0, 2, 4... (jumping by size)


def test_chunk():
    assert chunk([], 2) == []
    assert chunk([1], 2) == [[1]]
    assert chunk([1, 2], 2) == [[1, 2]]
    assert chunk([1, 2, 3], 2) == [[1, 2], [3]]
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]
    assert chunk(["a", "b", "c", "d"], 1) == [["a"], ["b"], ["c"], ["d"]]


# -----------------------------------------------------------------------------
# PRACTICE: Most Frequent
# -----------------------------------------------------------------------------
# Find the most frequently occurring item in a list.
# If there's a tie, return any one of the tied items.
# Return None for empty list.
#
# Example:
#   most_frequent([1, 2, 2, 3]) → 2
#   most_frequent(["a", "b", "a"]) → "a"
#
# Hints:
# - First count occurrences (dict or Counter)
# - Then find the key with the highest value
# - max() can take a key function: max(items, key=some_func)
#
# JS equivalent:
# function mostFrequent(arr) {
#   if (!arr.length) return null;
#   const counts = arr.reduce((acc, x) => {
#     acc[x] = (acc[x] || 0) + 1;
#     return acc;
#   }, {});
#   return Object.entries(counts).reduce((a, b) => a[1] > b[1] ? a : b)[0];
# }


def most_frequent(items: list):  # returns item type or None
    if not items:
        return None

    count_map = dict()

    for item in items:
        count_map[item] = count_map.get(item, 0) + 1

    return max(count_map, key=lambda k: count_map[k])


def test_most_frequent():
    assert most_frequent([]) is None
    assert most_frequent([1]) == 1
    assert most_frequent([1, 1]) == 1
    assert most_frequent([1, 2, 2]) == 2
    assert most_frequent([1, 2, 2, 3, 3, 3]) == 3
    assert most_frequent(["a", "b", "a"]) == "a"
    assert most_frequent(["x", "y", "z", "x", "x"]) == "x"


# -----------------------------------------------------------------------------
# PRACTICE: Rotate List
# -----------------------------------------------------------------------------
# Rotate a list by n positions. Positive n rotates right, negative rotates left.
#
# Example:
#   rotate([1, 2, 3, 4, 5], 2)  → [4, 5, 1, 2, 3]  (right by 2)
#   rotate([1, 2, 3, 4, 5], -1) → [2, 3, 4, 5, 1]  (left by 1)
#
# Hints:
# - Slicing can split the list at a position
# - Think about where to "cut" the list based on n
# - Handle n larger than list length (use modulo)
#
# JS equivalent:
# function rotate(arr, n) {
#   const len = arr.length;
#   if (!len) return [];
#   const k = ((n % len) + len) % len;
#   return [...arr.slice(-k), ...arr.slice(0, -k)];
# }


def rotate(items: list, n: int) -> list:
    if not items:
        return []

    length = len(items)

    # normalize n: handles negatives and n > length
    # e.g., -1 % 5 = 4, 7 % 5 = 2
    rotation = n % length

    # split list at (length - rotation) and swap the pieces
    # [1,2,3,4,5] with rotation=2: split at index 3
    #   items[3:] = [4,5]    (last 'rotation' items move to front)
    #   items[:3] = [1,2,3]  (remaining items move to back)
    # result: [4,5,1,2,3]
    return [*items[length - rotation :], *items[: length - rotation]]


def test_rotate():
    assert rotate([], 5) == []
    assert rotate([1], 1) == [1]
    assert rotate([1, 2, 3], 0) == [1, 2, 3]
    assert rotate([1, 2, 3, 4, 5], 1) == [5, 1, 2, 3, 4]
    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert rotate([1, 2, 3, 4, 5], -1) == [2, 3, 4, 5, 1]
    assert rotate([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]
    assert rotate([1, 2, 3], 5) == [2, 3, 1]  # n > length
    assert rotate([1, 2, 3], -5) == [3, 1, 2]  # negative n > length
