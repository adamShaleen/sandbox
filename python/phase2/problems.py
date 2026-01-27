# ============================================================================
# PHASE 2: Collections & Comprehensions - PROBLEMS
# ============================================================================
# Practice problems for Phase 2 concepts.
# Run tests: npm run test:py -- python/phase2/problems.py

# -----------------------------------------------------------------------------
# PROBLEM 1: Matrix Transpose
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
# PROBLEM 2: Flatten and Filter
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
# PROBLEM 3: Invert Dict
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
# PROBLEM 4: Merge Sorted Lists
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
# PROBLEM 5: Chunk List
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
# PROBLEM 6: Most Frequent
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
# PROBLEM 7: Rotate List
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


# -----------------------------------------------------------------------------
# PROBLEM 8: Group By
# -----------------------------------------------------------------------------
# Group items by the result of a key function.
# Returns a dict where keys are the function results and values are lists of items.
#
# Example:
#   group_by(["apple", "banana", "apricot", "blueberry"], lambda x: x[0])
#   → {"a": ["apple", "apricot"], "b": ["banana", "blueberry"]}
#
#   group_by([1, 2, 3, 4, 5, 6], lambda x: x % 2)
#   → {1: [1, 3, 5], 0: [2, 4, 6]}
#
# Hints:
# - Similar pattern to invert_dict - you're building a dict with lists
# - Apply the key function to each item to get the grouping key
# - setdefault() is your friend here
#
# JS equivalent:
# function groupBy(arr, keyFn) {
#   return arr.reduce((acc, item) => {
#     const key = keyFn(item);
#     acc[key] = acc[key] || [];
#     acc[key].push(item);
#     return acc;
#   }, {});
# }


def group_by(items: list, key_fn) -> dict:
    # Example: items = ["apple", "banana", "apricot"], key_fn = lambda x: x[0]

    output = {}

    for item in items:
        # Step 1: apply key function to get grouping key
        # key_fn("apple") → "a", key_fn("banana") → "b"
        key = key_fn(item)

        # Step 2: add item to the list for this key
        # setdefault: if key missing, create empty list; return the list
        # append: add item to that list
        # "a" → ["apple"], then "a" → ["apple", "apricot"]
        output.setdefault(key, []).append(item)

    # Result: {"a": ["apple", "apricot"], "b": ["banana"]}
    return output


def test_group_by():
    assert group_by([], lambda x: x) == {}
    assert group_by([1], lambda x: x) == {1: [1]}
    assert group_by([1, 2, 3, 4, 5, 6], lambda x: x % 2) == {1: [1, 3, 5], 0: [2, 4, 6]}
    assert group_by(["apple", "banana", "apricot", "blueberry"], lambda x: x[0]) == {
        "a": ["apple", "apricot"],
        "b": ["banana", "blueberry"],
    }
    assert group_by([1, 2, 3, 4, 5], lambda x: "even" if x % 2 == 0 else "odd") == {
        "odd": [1, 3, 5],
        "even": [2, 4],
    }
    assert group_by(["cat", "dog", "elephant", "ant"], len) == {
        3: ["cat", "dog", "ant"],
        8: ["elephant"],
    }


# -----------------------------------------------------------------------------
# PROBLEM 9: Two Sum
# -----------------------------------------------------------------------------
# Given a list of numbers and a target, return True if any two distinct
# numbers in the list add up to the target.
#
# Example:
#   two_sum([1, 2, 3, 4], 5) → True   (1+4 or 2+3)
#   two_sum([1, 2, 3, 4], 10) → False (no pair sums to 10)
#
# Hints:
# - Naive approach: nested loops O(n²) - works but slow
# - Better: use a set to track numbers you've seen
# - For each number, check if (target - number) is in the set
# - Sets have O(1) lookup with `in` operator
#
# JS equivalent:
# function twoSum(nums, target) {
#   const seen = new Set();
#   for (const n of nums) {
#     if (seen.has(target - n)) return true;
#     seen.add(n);
#   }
#   return false;
# }


def two_sum(nums: list[int], target: int) -> bool:
    # Example: nums = [1, 2, 3, 4], target = 5

    # Track numbers we've already visited
    # Set gives O(1) lookup vs O(n) for list
    seen = set()

    for num in nums:
        # Check if complement exists in seen numbers
        # If target=5 and num=3, we need 2. Have we seen 2?
        if (target - num) in seen:
            return True

        # Haven't found a pair yet; add this number to seen
        # Order matters: check first, add second (avoids using same element twice)
        seen.add(num)

    # Checked all numbers, no pair found
    return False


def test_two_sum():
    assert two_sum([], 5) is False
    assert two_sum([5], 5) is False  # need TWO numbers
    assert two_sum([1, 4], 5) is True
    assert two_sum([1, 2, 3, 4], 5) is True
    assert two_sum([1, 2, 3, 4], 10) is False
    assert two_sum([3, 3], 6) is True  # same value twice
    assert two_sum([1, 5, 3, 7, 9], 12) is True  # 5+7 or 3+9
    assert two_sum([-1, 2, 3, -2], 1) is True  # -1+2 or 3+-2
    assert two_sum([0, 0], 0) is True


# -----------------------------------------------------------------------------
# PROBLEM 10: Partition
# -----------------------------------------------------------------------------
# Split a list into two lists based on a predicate function.
# Returns a tuple: (items where predicate is True, items where predicate is False)
#
# Example:
#   partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
#   → ([2, 4], [1, 3, 5])
#
#   partition(["apple", "banana", "apricot"], lambda x: x.startswith("a"))
#   → (["apple", "apricot"], ["banana"])
#
# Hints:
# - Like filter(), but you keep BOTH sides
# - Build two lists, check predicate for each item
# - Return as a tuple (truthy_list, falsy_list)
#
# JS equivalent:
# function partition(arr, predFn) {
#   const truthy = [], falsy = [];
#   for (const item of arr) {
#     (predFn(item) ? truthy : falsy).push(item);
#   }
#   return [truthy, falsy];
# }


def partition(items: list, pred_fn) -> tuple[list, list]:
    # Example: items = [1, 2, 3, 4, 5], pred_fn = lambda x: x % 2 == 0

    # Two buckets: one for items that pass, one for items that fail
    truthy = []
    falsy = []

    for item in items:
        # Apply predicate to decide which bucket
        # pred_fn(2) → True → truthy; pred_fn(3) → False → falsy
        if pred_fn(item):
            truthy.append(item)
        else:
            falsy.append(item)

    # Return as tuple: (passing_items, failing_items)
    # Result: ([2, 4], [1, 3, 5])
    return truthy, falsy


def test_partition():
    assert partition([], lambda x: x) == ([], [])
    assert partition([1], lambda x: x > 0) == ([1], [])
    assert partition([1], lambda x: x < 0) == ([], [1])
    assert partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0) == ([2, 4], [1, 3, 5])
    assert partition([1, 2, 3, 4, 5], lambda x: x > 3) == ([4, 5], [1, 2, 3])
    assert partition(["apple", "banana", "apricot"], lambda x: x.startswith("a")) == (
        ["apple", "apricot"],
        ["banana"],
    )
    assert partition([0, "", None, 1, "hi"], bool) == ([1, "hi"], [0, "", None])


# -----------------------------------------------------------------------------
# PROBLEM 11: Anagram Groups
# -----------------------------------------------------------------------------
# Group words that are anagrams of each other.
# Two words are anagrams if they contain the same letters in different order.
# Return a list of groups (each group is a list of anagram words).
# Order of groups and words within groups doesn't matter.
#
# Example:
#   anagram_groups(["eat", "tea", "tan", "ate", "nat", "bat"])
#   → [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
#
# Hints:
# - Anagrams have the same letters when sorted: sorted("eat") == sorted("tea")
# - sorted() on a string returns a list of chars: sorted("cat") → ['a', 'c', 't']
# - Use "".join() to turn list back to string: "".join(['a', 'c', 't']) → "act"
# - This is a group_by problem: group by the sorted letters
#
# JS equivalent:
# function anagramGroups(words) {
#   const groups = {};
#   for (const word of words) {
#     const key = [...word].sort().join('');
#     groups[key] = groups[key] || [];
#     groups[key].push(word);
#   }
#   return Object.values(groups);
# }


def anagram_groups(words: list[str]) -> list[list[str]]:
    # Example: words = ["eat", "tea", "tan", "ate", "nat", "bat"]

    # Group words by their sorted letters (anagram signature)
    grouping_dict = {}

    for word in words:
        # sorted("eat") → ['a', 'e', 't'], join → "aet"
        # "eat", "tea", "ate" all become "aet" → same group
        sorted_word = "".join(sorted(word))

        # Same setdefault pattern: group words by their signature
        # {"aet": ["eat", "tea", "ate"], "ant": ["tan", "nat"], "abt": ["bat"]}
        grouping_dict.setdefault(sorted_word, []).append(word)

    # Return just the groups (values), not the keys
    # [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    return list(grouping_dict.values())


def test_anagram_groups():
    assert anagram_groups([]) == []
    assert anagram_groups(["cat"]) == [["cat"]]
    assert anagram_groups(["cat", "dog"]) == [["cat"], ["dog"]]
    assert sorted([sorted(g) for g in anagram_groups(["eat", "tea"])]) == [
        ["eat", "tea"]
    ]
    assert sorted([sorted(g) for g in anagram_groups(["eat", "tea", "ate"])]) == [
        ["ate", "eat", "tea"]
    ]
    result = anagram_groups(["eat", "tea", "tan", "ate", "nat", "bat"])
    # Check we have 3 groups with correct sizes
    assert len(result) == 3
    sizes = sorted([len(g) for g in result])
    assert sizes == [1, 2, 3]  # bat=1, tan/nat=2, eat/tea/ate=3


# -----------------------------------------------------------------------------
# PROBLEM 12: Run-Length Encoding
# -----------------------------------------------------------------------------
# Compress a list by counting consecutive repeated items.
# Return a list of tuples: (item, count)
#
# Example:
#   run_length_encode("aaabbc") → [("a", 3), ("b", 2), ("c", 1)]
#   run_length_encode([1, 1, 2, 2, 2, 3]) → [(1, 2), (2, 3), (3, 1)]
#
# Hints:
# - Track the current item and its count
# - When item changes, save the (item, count) tuple and reset
# - Don't forget the last group after the loop ends
# - Handle empty input
#
# JS equivalent:
# function runLengthEncode(items) {
#   if (!items.length) return [];
#   const result = [];
#   let current = items[0], count = 1;
#   for (let i = 1; i < items.length; i++) {
#     if (items[i] === current) count++;
#     else { result.push([current, count]); current = items[i]; count = 1; }
#   }
#   result.push([current, count]);
#   return result;
# }


def run_length_encode(items) -> list[tuple]:
    # Example: items = "aabbbaa"

    if not items:
        return []

    output = []
    current_item = items[0]  # start tracking first item
    count = 0  # will be incremented on first iteration

    for item in items:
        if current_item == item:
            # same item as we're tracking, increment count
            # 'a' == 'a' → count becomes 1, then 2
            count += 1
        else:
            # item changed! save the completed group, start new one
            # 'a' != 'b' → save ('a', 2), start counting 'b'
            output.append((current_item, count))
            count = 1  # new item already seen once
            current_item = item

    # don't forget the last group (loop ends without saving it)
    # after loop: current_item='a', count=2 → append ('a', 2)
    output.append((current_item, count))

    # Result: [('a', 2), ('b', 3), ('a', 2)]
    return output


def test_run_length_encode():
    assert run_length_encode("") == []
    assert run_length_encode([]) == []
    assert run_length_encode("a") == [("a", 1)]
    assert run_length_encode("aaa") == [("a", 3)]
    assert run_length_encode("abc") == [("a", 1), ("b", 1), ("c", 1)]
    assert run_length_encode("aaabbc") == [("a", 3), ("b", 2), ("c", 1)]
    assert run_length_encode("aabbbaa") == [("a", 2), ("b", 3), ("a", 2)]
    assert run_length_encode([1, 1, 2, 2, 2, 3]) == [(1, 2), (2, 3), (3, 1)]
    assert run_length_encode([True, True, False]) == [(True, 2), (False, 1)]
