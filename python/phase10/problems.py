# ============================================================================
# PHASE 10: Pythonic Idioms & Capstone - PROBLEMS
# ============================================================================

from __future__ import annotations

from collections import Counter, defaultdict, namedtuple
import itertools
from contextlib import contextmanager


# ----------------------------------------------------------------------------
# Problem 1 — Unpack and rotate
# ----------------------------------------------------------------------------
# `rotate_left(items)` takes a non-empty list and returns a new list with
# the first element moved to the end.
#
#   rotate_left([1, 2, 3, 4])  →  [2, 3, 4, 1]
#   rotate_left([42])          →  [42]
#
# Use starred unpacking — no slicing, no indexing.
#
# JS/TS hint:
#   const [first, ...rest] = arr
#   return [...rest, first]


def rotate_left(items: list) -> list:
    first, *rest = items
    return [*rest, first]


def test_rotate_left():
    assert rotate_left([1, 2, 3, 4]) == [2, 3, 4, 1]
    assert rotate_left([42]) == [42]
    assert rotate_left(["a", "b", "c"]) == ["b", "c", "a"]


# ----------------------------------------------------------------------------
# Problem 2 — Comprehension trio
# ----------------------------------------------------------------------------
# Three small functions, each using a different comprehension type.
#
# A) `word_lengths(words: list[str]) -> dict[str, int]`
#    Returns a dict mapping each word to its length.
#    word_lengths(["hi", "hello"]) → {"hi": 2, "hello": 5}
#
# B) `unique_domains(emails: list[str]) -> set[str]`
#    Returns the set of unique domains from a list of email addresses.
#    unique_domains(["a@foo.com", "b@bar.com", "c@foo.com"]) → {"foo.com", "bar.com"}
#    Hint: split on "@" and take the second part
#
# C) `flatten(matrix: list[list[int]]) -> list[int]`
#    Flattens a 2D list into a 1D list.
#    flatten([[1, 2], [3, 4], [5]]) → [1, 2, 3, 4, 5]
#
# Each function body should be a single return statement with a comprehension.


def word_lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}


def unique_domains(emails: list[str]) -> set[str]:
    return {email.split("@")[1] for email in emails}


def flatten(matrix: list[list[int]]) -> list[int]:
    return [x for row in matrix for x in row]


def test_comprehension_trio():
    assert word_lengths(["hi", "hello", "hey"]) == {"hi": 2, "hello": 5, "hey": 3}
    assert word_lengths([]) == {}

    assert unique_domains(["a@foo.com", "b@bar.com", "c@foo.com"]) == {
        "foo.com",
        "bar.com",
    }
    assert unique_domains([]) == set()

    assert flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert flatten([[], [1], []]) == [1]
    assert flatten([]) == []


# ----------------------------------------------------------------------------
# Problem 3 — collections in practice
# ----------------------------------------------------------------------------
# Two functions using Counter and defaultdict.
#
# A) `top_words(text: str, n: int) -> list[str]`
#    Given a string of space-separated words, return the n most common words
#    as a list of just the words (not the counts), most common first.
#    top_words("the cat sat on the mat the cat", 2) → ["the", "cat"]
#    Hint: Counter has a method for this — check the lesson.
#
# B) `group_by_first_letter(words: list[str]) -> dict[str, list[str]]`
#    Groups words by their first letter. Returns a plain dict (not a defaultdict).
#    group_by_first_letter(["apple", "ant", "banana", "avocado"])
#      → {"a": ["apple", "ant", "avocado"], "b": ["banana"]}
#    Hint: use defaultdict(list) internally, convert to dict before returning.


def top_words(text: str, n: int) -> list[str]:
    return [word for word, _ in Counter(text.split()).most_common(n)]


def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:
    groups = defaultdict(list)

    for word in words:
        groups[word[0]].append(word)

    return dict(groups)


def test_collections_practice():
    assert top_words("the cat sat on the mat the cat", 2) == ["the", "cat"]
    assert top_words("a a a b b c", 1) == ["a"]
    assert top_words("x y z", 3) == ["x", "y", "z"]  # order may vary on ties

    assert group_by_first_letter(["apple", "ant", "banana", "avocado"]) == {
        "a": ["apple", "ant", "avocado"],
        "b": ["banana"],
    }
    assert group_by_first_letter([]) == {}


# ----------------------------------------------------------------------------
# Problem 4 — itertools in practice
# ----------------------------------------------------------------------------
# Two functions using itertools.
#
# A) `interleave(a: list, b: list) -> list`
#    Merges two lists by alternating elements. If one is longer, append the rest.
#    interleave([1, 2, 3], ["a", "b"]) → [1, "a", 2, "b", 3]
#    interleave([1], [10, 20, 30])     → [1, 10, 20, 30]
#    Hint: zip_longest with a sentinel fillvalue, then filter it out.
#    Use a module-level sentinel object to mark "no value":
#      _MISSING = object()
#
# B) `run_length_encode(items: list) -> list[tuple]`
#    Encodes consecutive repeated elements as (count, value) tuples.
#    This is called "run-length encoding" — a basic compression technique
#    where instead of storing [1,1,1,2,2] you store [(3,1),(2,2)].
#    run_length_encode([1,1,1,2,2,3]) → [(3,1),(2,2),(1,3)]
#    run_length_encode(["a","a","b"]) → [(2,"a"),(1,"b")]
#    Hint: groupby — no sorting needed here since we want consecutive runs.

from itertools import zip_longest, chain  # noqa: E402

_MISSING = object()


def interleave(a: list, b: list) -> list:
    return [
        x
        for x in chain.from_iterable(zip_longest(a, b, fillvalue=_MISSING))
        if x is not _MISSING
    ]


def run_length_encode(items: list) -> list[tuple]:
    # 1 liner
    # return [(len(list(group)), key) for key, group in itertools.groupby(items)]
    result = []

    for key, group in itertools.groupby(items):
        result.append((len(list(group)), key))

    return result


def test_itertools_practice():
    assert interleave([1, 2, 3], ["a", "b"]) == [1, "a", 2, "b", 3]
    assert interleave([1], [10, 20, 30]) == [1, 10, 20, 30]
    assert interleave([], [1, 2]) == [1, 2]
    assert interleave([1, 2], []) == [1, 2]

    assert run_length_encode([1, 1, 1, 2, 2, 3]) == [(3, 1), (2, 2), (1, 3)]
    assert run_length_encode(["a", "a", "b"]) == [(2, "a"), (1, "b")]
    assert run_length_encode([]) == []
    assert run_length_encode([7]) == [(1, 7)]


# ----------------------------------------------------------------------------
# Problem 5 — Write a context manager
# ----------------------------------------------------------------------------
# `suppress_errors(*exc_types)` is a context manager that silently ignores
# any exceptions of the given types raised inside the `with` block.
# If no exception is raised, or a different exception type is raised, it
# behaves normally.
#
# This is actually a real tool in Python's stdlib (contextlib.suppress),
# but we'll build it ourselves to understand the pattern.
#
# Use @contextmanager. Remember:
#   - wrap the yield in try/except
#   - catch the given exception types and do nothing (pass)
#   - let anything else propagate
#
# JS/TS hint:
#   try { doWork() } catch (e) { if (!(e instanceof ExpectedError)) throw e }


@contextmanager
def suppress_errors(*exc_types):
    try:
        yield
    except exc_types:
        return


def test_suppress_errors():
    import pytest

    # suppresses the specified exception
    with suppress_errors(ValueError):
        raise ValueError("ignored")  # should NOT propagate

    # suppresses multiple types
    with suppress_errors(ValueError, KeyError):
        raise KeyError("also ignored")

    # does NOT suppress unrelated exceptions
    with pytest.raises(TypeError):
        with suppress_errors(ValueError):
            raise TypeError("this should propagate")

    # no exception — works normally
    result = []
    with suppress_errors(ValueError):
        result.append(1)
    assert result == [1]


# ----------------------------------------------------------------------------
# Problem 6 — Build a typed pipeline with dunders
# ----------------------------------------------------------------------------
# `Pipeline` is a simple data-processing container that wraps a list of items
# and lets you chain transformations.
#
# Implement the following dunders:
#   __init__(self, items)    — stores items internally
#   __len__                  — number of items
#   __iter__                 — iterate over items
#   __repr__                 — "Pipeline([...])"
#   __getitem__(self, index) — supports Pipeline[0], Pipeline[1:3], etc.
#                              Hint: just delegate to the internal list
#
# Also implement one regular method:
#   map(self, fn) -> Pipeline  — returns a NEW Pipeline with fn applied to each item
#                                (like JS Array.map — does not mutate self)
#
# JS/TS hint:
#   class Pipeline<T> {
#     constructor(private items: T[]) {}
#     map<U>(fn: (x: T) => U): Pipeline<U> { return new Pipeline(this.items.map(fn)) }
#   }


class Pipeline:
    def __init__(self, items):
        self._items = items

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Pipeline({self._items})"

    def __getitem__(self, index):
        return self._items[index]

    def map(self, fn) -> Pipeline:
        items = [fn(item) for item in self._items]
        return Pipeline(items)


def test_pipeline():
    p = Pipeline([1, 2, 3, 4, 5])

    assert len(p) == 5
    assert list(p) == [1, 2, 3, 4, 5]
    assert repr(p) == "Pipeline([1, 2, 3, 4, 5])"
    assert p[0] == 1
    assert p[1:3] == [2, 3]

    doubled = p.map(lambda x: x * 2)
    assert isinstance(doubled, Pipeline)
    assert list(doubled) == [2, 4, 6, 8, 10]

    # chaining
    result = p.map(lambda x: x * 2).map(lambda x: x + 1)
    assert list(result) == [3, 5, 7, 9, 11]

    # original unchanged
    assert list(p) == [1, 2, 3, 4, 5]


# ============================================================================
# CAPSTONE — Game Leaderboard
# ============================================================================
# Build a small leaderboard system that brings together the phase concepts.
#
# --- Step 1: Define a namedtuple ---
# `Result` with fields: player (str), score (int), level (str)
# level is one of "easy", "medium", "hard"
#
# --- Step 2: Build a `Leaderboard` class ---
# __init__(self, results: list[Result])
# __len__                → total number of results
# __iter__               → iterate over results
# __contains__(player)   → True if player name appears anywhere in results
# __repr__               → "Leaderboard(<n> results)"
#
# Three methods (each should be a comprehension or use a collections type):
#
# top_players(n: int) -> list[str]
#   Returns the n players with the highest TOTAL score across all their results.
#   Return just the names, most points first.
#   Hint: Counter + most_common
#
# by_level() -> dict[str, list[Result]]
#   Groups results by level ("easy", "medium", "hard").
#   Returns a plain dict (not defaultdict).
#   Hint: defaultdict(list) internally
#
# best_per_player() -> dict[str, int]
#   Returns each player's single highest score.
#   Hint: dict comprehension — for each player, max of their scores


Result = namedtuple("Result", ["player", "score", "level"])


class Leaderboard:
    def __init__(self, results: list[Result]) -> None:
        self.results = results

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(self.results)

    def __contains__(self, player):
        return any(result.player == player for result in self.results)

    def __repr__(self) -> str:
        return f"Leaderboard({len(self.results)} results)"

    def top_players(self, n: int) -> list[str]:
        totals_by_player = Counter()

        for player, score, _ in self.results:
            totals_by_player[player] += score

        return [player for player, _ in totals_by_player.most_common(n)]

    def by_level(self) -> dict[str, list[Result]]:
        level_to_results = defaultdict(list)

        for result in self.results:
            level_to_results[result.level].append(result)

        return dict(level_to_results)

    def best_per_player(self) -> dict[str, int]:
        player_to_scores = defaultdict(list)

        for player, score, _ in self.results:
            player_to_scores[player].append(score)

        return {player: max(scores) for player, scores in player_to_scores.items()}


def test_capstone():
    results = [
        Result("adam", 120, "hard"),
        Result("bob", 80, "easy"),
        Result("adam", 95, "medium"),
        Result("carol", 110, "hard"),
        Result("bob", 60, "easy"),
        Result("carol", 70, "medium"),
    ]
    lb = Leaderboard(results)

    # dunders
    assert len(lb) == 6
    assert list(lb) == results
    assert "adam" in lb
    assert "dave" not in lb
    assert repr(lb) == "Leaderboard(6 results)"

    # top_players — adam: 215, carol: 180, bob: 140
    assert lb.top_players(2) == ["adam", "carol"]
    assert lb.top_players(1) == ["adam"]

    # by_level
    by_level = lb.by_level()
    assert set(by_level.keys()) == {"hard", "easy", "medium"}
    assert len(by_level["hard"]) == 2
    assert len(by_level["easy"]) == 2

    # best_per_player
    best = lb.best_per_player()
    assert best == {"adam": 120, "bob": 80, "carol": 110}
