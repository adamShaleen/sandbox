# ============================================================================
# PHASE 1: Syntax Bridge (JS → Python)
# ============================================================================

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


# -----------------------------------------------------------------------------
# EXERCISE: Rewrite flick_switch with type hints
# -----------------------------------------------------------------------------


def flick_switch(words: list[str]) -> list[bool]:
    """
    Start with flag=True. For each word:
    - If contains 'flick', toggle flag and append new value
    - Otherwise append current flag value
    """
    flag = True
    output: list[bool] = []

    for word in words:
        if "flick" in word:
            flag = not flag
            output.append(flag)
        else:
            output.append(flag)

    return output


def test_flick_switch():
    assert flick_switch(["wank", "flick", "jank", "bank"]) == [
        True,
        False,
        False,
        False,
    ]
    assert flick_switch(["flick", "flick"]) == [False, True]
    assert flick_switch(["a", "b", "c"]) == [True, True, True]


# -----------------------------------------------------------------------------
# PRACTICE: Word Score Calculator
# -----------------------------------------------------------------------------
# Calculate a score for each word based on letter values (a=1, b=2, ... z=26)
# Return a dict mapping each word to its score
#
# Hints:
# - ord('a') returns 97, ord('b') returns 98, etc.
# - So letter value = ord(char) - ord('a') + 1
# - Use .lower() to handle uppercase
# - Skip non-letter characters
#
# JS equivalent you might write:
# function wordScores(words) {
#   return words.reduce((acc, char) => {
#     acc[char] = [...char.toLowerCase()]
#       .filter(c => c >= 'a' && c <= 'z')
#       .reduce((sum, c) => sum + (c.charCodeAt(0) - 96), 0);

#     return acc;
#   }, {});
# }


def word_scores(words: list[str]) -> dict[str, int]:
    output = {}

    for word in words:
        score = 0

        for char in word:
            if char.isalpha():
                score += ord(char.lower()) - ord("a") + 1

            output[word] = score

    return output


def test_word_scores():
    assert word_scores(["a"]) == {"a": 1}
    assert word_scores(["z"]) == {"z": 26}
    assert word_scores(["cab"]) == {"cab": 6}
    assert word_scores(["hello", "world"]) == {"hello": 52, "world": 72}
    assert word_scores(["ABC"]) == {"ABC": 6}  # handles uppercase
    assert word_scores(["hi!", "a1b"]) == {"hi!": 17, "a1b": 3}  # ignores non-letters
    assert word_scores([]) == {}  # empty list


# -----------------------------------------------------------------------------
# PRACTICE: Count Character Types
# -----------------------------------------------------------------------------
# Given a string, return a dict with counts of each character type:
# - "letters": count of a-z, A-Z
# - "digits": count of 0-9
# - "spaces": count of spaces
# - "other": count of everything else (punctuation, symbols)
#
# Hints:
# - char.isalpha() → True if letter
# - char.isdigit() → True if digit
# - char == " " or char.isspace() → True if space
#
# JS equivalent:
# function countCharTypes(str) {
#   return [...str].reduce((acc, c) => {
#     if (/[a-zA-Z]/.test(c)) acc.letters++;
#     else if (/[0-9]/.test(c)) acc.digits++;
#     else if (c === ' ') acc.spaces++;
#     else acc.other++;
#     return acc;
#   }, { letters: 0, digits: 0, spaces: 0, other: 0 });
# }


def count_char_types(text: str) -> dict[str, int]:
    output = {"letters": 0, "digits": 0, "spaces": 0, "other": 0}

    for char in text:
        if char.isalpha():
            output["letters"] += 1
        elif char.isdigit():
            output["digits"] += 1
        elif char.isspace():
            output["spaces"] += 1
        else:
            output["other"] += 1

    return output


def test_count_char_types():
    assert count_char_types("") == {"letters": 0, "digits": 0, "spaces": 0, "other": 0}
    assert count_char_types("abc") == {
        "letters": 3,
        "digits": 0,
        "spaces": 0,
        "other": 0,
    }
    assert count_char_types("123") == {
        "letters": 0,
        "digits": 3,
        "spaces": 0,
        "other": 0,
    }
    assert count_char_types("   ") == {
        "letters": 0,
        "digits": 0,
        "spaces": 3,
        "other": 0,
    }
    assert count_char_types("!!!") == {
        "letters": 0,
        "digits": 0,
        "spaces": 0,
        "other": 3,
    }
    assert count_char_types("Hello World!") == {
        "letters": 10,
        "digits": 0,
        "spaces": 1,
        "other": 1,
    }
    assert count_char_types("Test 123!") == {
        "letters": 4,
        "digits": 3,
        "spaces": 1,
        "other": 1,
    }


# -----------------------------------------------------------------------------
# PRACTICE: Group By First Letter
# -----------------------------------------------------------------------------
# Given a list of words, group them by their first letter (lowercase).
# Return a dict where keys are letters and values are lists of words.
#
# Hints:
# - word[0] gets first character
# - .lower() to normalize case
# - Check if key exists before appending, OR use dict.setdefault()
# - Skip empty strings
#
# JS equivalent:
# function groupByFirstLetter(words) {
#   return words.reduce((acc, word) => {
#     if (!word) return acc;
#     const key = word[0].toLowerCase();
#     acc[key] = acc[key] || [];
#     acc[key].push(word);
#     return acc;
#   }, {});
# }


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    output = {}

    for word in words:
        if word:
            first_char = word[0].lower()
            output.setdefault(first_char, []).append(word)

    return output


def test_group_by_first_letter():
    assert group_by_first_letter([]) == {}
    assert group_by_first_letter(["apple"]) == {"a": ["apple"]}
    assert group_by_first_letter(["apple", "apricot"]) == {"a": ["apple", "apricot"]}
    assert group_by_first_letter(["apple", "Banana"]) == {
        "a": ["apple"],
        "b": ["Banana"],
    }
    assert group_by_first_letter(["Apple", "APRICOT", "avocado"]) == {
        "a": ["Apple", "APRICOT", "avocado"]
    }
    assert group_by_first_letter(["", "apple", ""]) == {"a": ["apple"]}  # skips empty
    assert group_by_first_letter(["cat", "car", "dog", "deer"]) == {
        "c": ["cat", "car"],
        "d": ["dog", "deer"],
    }
