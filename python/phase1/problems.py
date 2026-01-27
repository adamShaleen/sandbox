# ============================================================================
# PHASE 1: Syntax Bridge (JS → Python) - PROBLEMS
# ============================================================================
# Practice problems for Phase 1 concepts.
# Run tests: npm run test:py -- python/phase1/problems.py

# -----------------------------------------------------------------------------
# PROBLEM 1: Flick Switch
# -----------------------------------------------------------------------------
# Start with flag=True. For each word:
# - If contains 'flick', toggle flag and append new value
# - Otherwise append current flag value


def flick_switch(words: list[str]) -> list[bool]:
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
# PROBLEM 2: Word Score Calculator
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
# PROBLEM 3: Count Character Types
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
# PROBLEM 4: Group By First Letter
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


# -----------------------------------------------------------------------------
# PROBLEM 5: Find Duplicates
# -----------------------------------------------------------------------------
# Given a list, return a new list containing only the items that appear
# more than once. Result should be in order of first duplicate occurrence,
# with no duplicates in the result itself.
#
# Hints:
# - Track counts with a dict, OR use list.count()
# - Track what you've already added to avoid duplicates in result
# - `in` operator checks membership: `if item in some_list:`
#
# JS equivalent:
# function findDuplicates(items) {
#   const counts = {};
#   items.forEach(item => counts[item] = (counts[item] || 0) + 1);
#   const seen = new Set();
#   return items.filter(item => {
#     if (counts[item] > 1 && !seen.has(item)) {
#       seen.add(item);
#       return true;
#     }
#     return false;
#   });
# }


def find_duplicates(items: list) -> list:
    count_map = {}
    for item in items:
        count_map[item] = count_map.get(item, 0) + 1

    return [key for key, value in count_map.items() if value > 1]


def test_find_duplicates():
    assert find_duplicates([]) == []
    assert find_duplicates([1, 2, 3]) == []  # no duplicates
    assert find_duplicates([1, 1]) == [1]
    assert find_duplicates([1, 2, 1]) == [1]
    assert find_duplicates([1, 2, 2, 3, 1]) == [1, 2]  # order of first occurrence
    assert find_duplicates(["a", "b", "a", "c", "b"]) == ["a", "b"]
    assert find_duplicates([1, 1, 1, 1]) == [1]  # only once in result


# -----------------------------------------------------------------------------
# PROBLEM 6: Validate Brackets
# -----------------------------------------------------------------------------
# Given a string containing brackets, check if all brackets are balanced.
# Only consider: (), [], {}
# Ignore all other characters.
#
# Hints:
# - Use a list as a stack: append() to push, pop() to remove last
# - Track opening brackets, match with closing
# - Each closing bracket must match the most recent opening bracket
#
# JS equivalent:
# function validateBrackets(str) {
#   const pairs = { ')': '(', ']': '[', '}': '{' };
#   const stack = [];
#   for (const char of str) {
#     if ('([{'.includes(char)) stack.push(char);
#     else if (')]}'. includes(char)) {
#       if (stack.pop() !== pairs[char]) return false;
#     }
#   }
#   return stack.length === 0;
# }


def validate_brackets(text: str) -> bool:
    pairs = {"}": "{", ")": "(", "]": "["}
    stack = []

    for char in text:
        if char in "{([":
            stack.append(char)
        elif char in "}])":
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack


def test_validate_brackets():
    assert validate_brackets("") == True
    assert validate_brackets("()") == True
    assert validate_brackets("[]") == True
    assert validate_brackets("{}") == True
    assert validate_brackets("([])") == True
    assert validate_brackets("{[()]}") == True
    assert validate_brackets("hello (world)") == True  # ignores other chars
    assert validate_brackets("(") == False  # unclosed
    assert validate_brackets(")") == False  # no opener
    assert validate_brackets("([)]") == False  # wrong order
    assert validate_brackets("((())") == False  # missing closer
    assert validate_brackets("func(arr[0], obj{})") == True
