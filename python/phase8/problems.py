# ============================================================================
# PHASE 8: Testing (pytest advanced) - PROBLEMS
# ============================================================================
# Run tests: npm run test:py:file python/phase8/problems.py

import collections

from unittest.mock import Mock

import pytest


# -----------------------------------------------------------------------------
# PROBLEM 1: fixture isolation
# -----------------------------------------------------------------------------
# Write a `stack` fixture that returns a fresh empty list.
# Then write two tests that both use it — one that appends items, one that
# checks the stack starts empty — to prove each test gets its own copy.
#
# Concept: fixtures (concept 1)
# JS hint: like beforeEach(() => { stack = [] }) — but each test is isolated
#
# Hints:
# - @pytest.fixture returns the list
# - Both test functions take `stack` as a parameter
# - If isolation is working, test order won't matter


@pytest.fixture
def stack():
    return []


def test_stack_fixture_appends(stack):
    stack.append("foo")
    assert stack == ["foo"]


def test_stack_fixture_starts_empty(stack):
    assert stack == []


# -----------------------------------------------------------------------------
# PROBLEM 2: parametrize
# -----------------------------------------------------------------------------
# Given `is_palindrome` below, write ONE parametrized test that covers:
#   "racecar" → True
#   "hello"   → False
#   ""        → True   (empty string is a palindrome)
#   "a"       → True   (single char)
#   "Racecar" → False  (case-sensitive)
#
# Concept: parametrize (concept 2)
# JS hint: test.each([[input, expected], ...])('desc', (s, expected) => { ... })
#
# Hints:
# - @pytest.mark.parametrize("s, expected", [...])
# - Each entry in the list is a (input, expected) tuple


def is_palindrome(s: str) -> bool:
    return s == s[::-1]


@pytest.mark.parametrize(
    "string,output",
    [
        ("jank", False),
        ("wow", True),
        ("fuzz", False),
        ("WANGNAW", True),
        ("", True),
        ("a", True),
    ],
)
def test_parametrize_is_palindrome(string, output):
    assert is_palindrome(string) == output


# -----------------------------------------------------------------------------
# PROBLEM 3: pytest.raises + match
# -----------------------------------------------------------------------------
# Implement `parse_percentage(value)`:
#   - Converts a string like "85%" to a float 0.85
#   - Raises ValueError("must end with %") if the string doesn't end with "%"
#   - Raises ValueError("out of range") if the number is < 0 or > 100
#
# Then write three tests:
#   1. Happy path: "85%" → 0.85
#   2. Missing "%"  → ValueError with match
#   3. Out of range → ValueError with match
#
# Concept: pytest.raises (concept 4)
# JS hint: expect(() => fn()).toThrow('message')
#
# Hints:
# - Check if value ends with "%" before converting
# - float(value[:-1]) strips the "%" and converts
# - Use pytest.raises(ValueError, match="...") for the error cases


def parse_percentage(value: str) -> float:
    if "%" not in value:
        raise ValueError("must end with %")

    percent = float(value[:-1])

    if 0 < percent > 100:
        raise ValueError("out of range")

    return percent


def test_parse_percentage_happy_path():
    assert parse_percentage("85%") == 85.0


def test_raises_parse_percentage_bad_format():
    with pytest.raises(ValueError, match="must end with %"):
        parse_percentage("25")


def test_raises_parse_percentage_out_of_range():
    with pytest.raises(ValueError, match="out of range"):
        parse_percentage("105%")


# -----------------------------------------------------------------------------
# PROBLEM 4: tmp_path
# -----------------------------------------------------------------------------
# Implement `most_frequent_word(filepath)`:
#   - Reads a text file at `filepath`
#   - Returns the single most frequent word (case-insensitive)
#   - Words are separated by whitespace
#
# Write a test using `tmp_path` that:
#   1. Creates a temp file with known content
#   2. Calls your function
#   3. Asserts the correct word is returned
#
# Concept: tmp_path (concept 3)
# JS hint: like using a temp directory from the `tmp` npm package, but built-in
#
# Hints:
# - tmp_path is a pathlib.Path — use (tmp_path / "file.txt").write_text(...)
# - str.split() splits on any whitespace
# - collections.Counter and its .most_common(1) method are your friend


def most_frequent_word(filepath) -> str:
    content_split = filepath.read_text().lower().split()
    return collections.Counter(content_split).most_common(1)[0][0]


def test_wank(tmp_path):
    mock_file = tmp_path / "mock.txt"
    mock_file.write_text("wank wank bank")
    assert most_frequent_word(mock_file) == "wank"


# -----------------------------------------------------------------------------
# PROBLEM 5: capsys
# -----------------------------------------------------------------------------
# Given `print_receipt` below, write a test using `capsys` that asserts:
#   - Each item name and price appears in the output
#   - A "Total:" line appears with the correct sum
#
# Concept: capsys (concept 3)
# JS hint: like jest.spyOn(console, 'log') but simpler
#
# Hints:
# - capsys.readouterr().out gives you the full stdout as a string
# - Use `in` to check substrings rather than matching the whole output


def print_receipt(items: dict):
    for name, price in items.items():
        print(f"{name}: ${price:.2f}")
    total = sum(items.values())
    print(f"Total: ${total:.2f}")


def test_print_receipt(capsys):
    print_receipt({"booze": 10.25, "chips": 4.50})
    captured = capsys.readouterr()
    assert "booze" in captured.out
    assert "chips" in captured.out
    assert "Total: $14.75" in captured.out


# -----------------------------------------------------------------------------
# PROBLEM 6: monkeypatch
# -----------------------------------------------------------------------------
# Implement `current_user_greeting()`:
#   - Reads the env var "APP_USER", falls back to "stranger" if not set
#   - Returns f"Hello, {name}!"
#
# Write TWO tests using monkeypatch:
#   1. env var is set → greeting uses it
#   2. env var is absent → greeting uses "stranger"
#
# Concept: monkeypatch (concept 6)
# JS hint: like setting process.env.APP_USER in beforeEach + cleanup in afterEach
#
# Hints:
# - import os and use os.environ.get("APP_USER", "stranger")
# - monkeypatch.setenv("APP_USER", "ada")

import os  # noqa: E402


def current_user_greeting() -> str:
    user = os.environ.get("APP_USER", "stranger")
    return f"Hello, {user}!"


def test_current_user_greeting_env_set(monkeypatch):
    monkeypatch.setenv("APP_USER", "Wayne Dick")
    assert current_user_greeting() == "Hello, Wayne Dick!"


def test_current_user_greeting_env_not_set():
    assert current_user_greeting() == "Hello, stranger!"


# -----------------------------------------------------------------------------
# PROBLEM 7: fixture composition
# -----------------------------------------------------------------------------
# Using `base_user` from conftest.py, write a `premium_user` fixture that
# adds a "tier": "premium" key and returns the new dict.
#
# Then write a test that asserts:
#   - premium_user["name"] == "ada"         (base fields still present)
#   - premium_user["tier"] == "premium"     (new field added)
#
# Concept: fixture composition + conftest (concepts 1, 7)
# JS hint: like spreading a base object: { ...baseUser, tier: "premium" }
#
# Hints:
# - Your fixture takes `base_user` as a parameter (injected from conftest.py)
# - Fixtures must return a value — that's what the test receives
# - {**base_user, "tier": "premium"} builds a new dict without mutating the original
# - Dict values are accessed with ["key"], not .key


@pytest.fixture
def premium_user(base_user):
    return {**base_user, "tier": "premium"}


def test_premium_user(premium_user):
    assert premium_user["name"] == "ada"
    assert premium_user["tier"] == "premium"


# -----------------------------------------------------------------------------
# PROBLEM 8: unittest.mock
# -----------------------------------------------------------------------------
# Given the classes below, write TWO tests for `process_order`:
#
#   Test 1 — success path:
#     - Create a Mock() for the gateway
#     - Call process_order with it and an amount
#     - Assert gateway.charge was called with the correct amount
#     - Assert process_order returned True
#
#   Test 2 — failure path:
#     - Set gateway.charge to raise RuntimeError via side_effect
#     - Assert process_order returned False
#
# Concept: unittest.mock (concept 8)
# JS hint: like jest.fn() for the gateway, checking mockFn.mock.calls
#
# Hints:
# - from unittest.mock import Mock  (already imported at the top)
# - gateway = Mock()  creates a mock object — all its attributes are also mocks
# - gateway.charge.assert_called_once_with(amount) checks the call
# - gateway.charge.side_effect = RuntimeError("declined") makes it raise


class PaymentGateway:
    def charge(self, amount: float) -> bool:
        raise NotImplementedError("real gateway not available in tests")


def process_order(gateway: PaymentGateway, amount: float) -> bool:
    try:
        gateway.charge(amount)
        return True
    except RuntimeError:
        return False


def test_process_order_happy_path():
    payment_gateway = Mock()
    result = process_order(payment_gateway, 100.25)
    assert result
    payment_gateway.charge.assert_called_once_with(100.25)


def test_processs_order_sad_path():
    payment_gateway = Mock()
    payment_gateway.charge.side_effect = RuntimeError("declined")

    assert not process_order(payment_gateway, 100.25)


# -----------------------------------------------------------------------------
# PROBLEM 9: parametrize + raises combo
# -----------------------------------------------------------------------------
# Implement `hex_to_rgb(hex_str)`:
#   - Converts "#ff8800" → (255, 136, 0)
#   - Raises ValueError("invalid hex color") for anything that doesn't match
#
# Write ONE parametrized test that covers both valid and invalid inputs.
# Use an extra `valid` boolean column to branch between the two cases:
#   - valid=True  → assert the return value equals the expected tuple
#   - valid=False → use pytest.raises(ValueError) inside the test body
#
# Concept: parametrize + pytest.raises (concepts 2, 4)
#
# Hints:
# - Valid format: starts with "#", exactly 7 chars, rest are hex digits
# - int("ff", 16) converts a two-char hex string to an int
# - Slice the string: hex_str[1:3], hex_str[3:5], hex_str[5:7] for R, G, B
# - str.isidentifier() won't help here — use a try/except or re.match
# - Parametrize table column: "hex_str, expected, valid"
# - For invalid cases, set expected to None (it won't be used)


def hex_to_rgb(hex_str: str) -> tuple:
    if hex_str[0] != "#" or len(hex_str) != 7:
        raise ValueError("invalid hex color")

    r = hex_str[1:3]
    g = hex_str[3:5]
    b = hex_str[5:7]

    return (int(r, 16), int(g, 16), int(b, 16))


@pytest.mark.parametrize(
    "hex_str, expected, valid",
    [
        pytest.param("#ff8800", (255, 136, 0), True, id="orange"),
        pytest.param("ff8800", None, False, id="missing #"),
        pytest.param("#ff8", None, False, id="too short"),
        pytest.param("#gggggg", None, False, id="invalid hex"),
    ],
)
def test_hex_to_rgb(hex_str, expected, valid):
    if valid:
        assert hex_to_rgb(hex_str) == expected
    else:
        with pytest.raises(ValueError):
            hex_to_rgb(hex_str)


# -----------------------------------------------------------------------------
# PROBLEM 10: yield fixture
# -----------------------------------------------------------------------------
# Write an `audit_log` yield fixture that:
#   - Setup: creates an empty list, appends "session started", then yields it
#   - Teardown (after yield): appends "session ended"
#
# Write TWO tests:
#
#   Test 1: receives the log, appends "user action", asserts the log is
#           ["session started", "user action"]
#           (teardown fires after this assert, so "session ended" won't appear)
#
#   Test 2: proves the log is FRESH each time — assert it only contains
#           "session started" with no leftover entries from test 1
#
# Concept: yield fixtures (concept 1)
# JS hint: like beforeEach + afterEach in one function, scoped per test
#
# Hints:
# - The fixture must return a value via yield, not return
# - Anything after yield runs as teardown, automatically, after each test
# - Each test gets a completely new list — fixture scope is "function" by default


@pytest.fixture
def audit_log():
    log = []
    log.append("session started")
    yield log
    log.append("session ended")


def test_audit_log_1(audit_log):
    audit_log.append("user action")
    assert audit_log == ["session started", "user action"]


def test_audit_log_2(audit_log):
    assert audit_log == ["session started"]
