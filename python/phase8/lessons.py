# ============================================================================
# PHASE 8: Testing (pytest advanced) - LESSONS
# ============================================================================
# Deep dive into pytest's most powerful features.
# Coming from JS/TS (Jest), you'll find many parallels — and some surprises.
#
# Concepts covered:
#   1. Fixtures (@pytest.fixture)              ← this lesson
#   2. Parametrize (@pytest.mark.parametrize)
#   3. Built-in fixtures (tmp_path, capfd)
#   4. pytest.raises (exception testing)
#   5. Markers (skip, xfail, custom)
#   6. monkeypatch (patching at runtime)
#   7. conftest.py (shared fixtures)
#   8. unittest.mock (Mock, MagicMock, patch)

import pytest


# -----------------------------------------------------------------------------
# 1. FIXTURES (@pytest.fixture)
# -----------------------------------------------------------------------------
# A fixture is a function that provides setup (and optionally teardown) for
# your tests. Any test that names a fixture as a parameter automatically
# receives its return value — pytest resolves and injects it.
#
# JS/Jest comparison:
#   beforeEach(() => { ... })  → @pytest.fixture  (default scope="function")
#   afterEach(() => { ... })   → @pytest.fixture with `yield` + teardown after
#   beforeAll(() => { ... })   → @pytest.fixture(scope="module")
#   afterAll(() => { ... })    → scope="module" with yield + teardown
#
# Key difference from Jest: Jest setup/teardown are imperative callbacks.
# pytest fixtures are declarative — tests *request* what they need by listing
# it as a parameter name. No registration, no describe block required.
#
# Basic anatomy:
#
#   @pytest.fixture
#   def my_fixture():
#       return some_value           # test receives this
#
#   def test_something(my_fixture): # ← named param = fixture injection
#       assert my_fixture == some_value
#
# Yield fixtures (setup + teardown in one function):
#
#   @pytest.fixture
#   def db():
#       conn = connect()   # setup
#       yield conn         # test gets conn here
#       conn.close()       # teardown — runs after test, even on failure
#
# Fixture scope — controls how often a fixture is created:
#   "function"  (default) — new instance per test
#   "class"               — shared within a test class
#   "module"              — shared across the entire file
#   "session"             — shared across the entire test run
#
# Fixtures can depend on other fixtures (pytest injects them automatically):
#
#   @pytest.fixture
#   def user(db):          # db is another fixture — injected by pytest
#       return db.create("ada")
#
# NOTE: In this phase, fixtures replace the demo_/test_ pattern from earlier
# phases. The fixture itself is the "demo" — it shows setup logic. The test
# function that uses it shows the concept in action.


# --- Fixture 1: Simple value fixture ---
# Returns a plain value. No teardown needed.


@pytest.fixture
def sample_list():
    # Equivalent to Jest:  let list; beforeEach(() => { list = [1,2,3,4,5] })
    return [1, 2, 3, 4, 5]


def test_fixture_injection(sample_list):
    # pytest sees `sample_list` as a param, finds the fixture, injects it.
    assert sample_list == [1, 2, 3, 4, 5]
    assert len(sample_list) == 5


# --- Fixture 2: Yield fixture (setup + teardown) ---
# `yield` splits setup (before) from teardown (after).
# Teardown runs even if the test raises an exception.


@pytest.fixture
def event_log():
    log = []
    log.append("setup")
    yield log  # test receives log here
    # teardown — runs after the test body, regardless of pass/fail
    log.clear()  # cleanup (in real code: close files, drop db tables, etc.)


def test_yield_fixture(event_log):
    # event_log is already ["setup"] when we receive it
    assert event_log == ["setup"]
    event_log.append("test ran")
    assert event_log == ["setup", "test ran"]
    # After this returns, the fixture teardown (log.clear()) fires automatically


# --- Fixture 3: Fixture depending on another fixture ---
# pytest resolves the dependency graph — you never call fixtures directly.


@pytest.fixture
def doubled_list(sample_list):  # sample_list injected here automatically
    return [x * 2 for x in sample_list]


def test_fixture_composition(doubled_list):
    assert doubled_list == [2, 4, 6, 8, 10]


# --- Fixture 4: Module-scoped fixture ---
# Created once for the whole file, shared across all tests that use it.
# Equivalent to Jest's beforeAll/afterAll.


@pytest.fixture(scope="module")
def expensive_resource():
    # In real code: start a test server, load a large file, compile something.
    resource = {"initialized": True, "call_count": 0}
    yield resource
    # teardown after ALL tests in this module that use this fixture have run
    resource.clear()


def test_module_scope_a(expensive_resource):
    expensive_resource["call_count"] += 1
    assert expensive_resource["initialized"] is True


def test_module_scope_b(expensive_resource):
    # Same dict object as test_module_scope_a — not recreated between tests
    expensive_resource["call_count"] += 1
    assert expensive_resource["call_count"] == 2  # accumulated from test_a


# --- Fixture 5: Multiple fixtures in one test ---
# A test can request as many fixtures as it needs — just list them as params.


@pytest.fixture
def user():
    return {"name": "ada", "role": "admin"}


@pytest.fixture
def permissions(user):  # depends on user fixture
    return {"read": True, "write": user["role"] == "admin"}


def test_multiple_fixtures(user, permissions):
    assert user["name"] == "ada"
    assert permissions["write"] is True


# -----------------------------------------------------------------------------
# 2. PARAMETRIZE (@pytest.mark.parametrize)
# -----------------------------------------------------------------------------
# Parametrize runs the same test function multiple times with different inputs.
# Instead of writing N nearly-identical test functions, you write one and
# supply a table of (input, expected) pairs.
#
# JS/Jest comparison:
#   test.each([
#     [2, 4],
#     [3, 9],
#   ])('squares %i to %i', (n, expected) => { expect(square(n)).toBe(expected) })
#
# pytest equivalent:
#   @pytest.mark.parametrize("n, expected", [(2, 4), (3, 9)])
#   def test_square(n, expected):
#       assert square(n) == expected
#
# Anatomy:
#   @pytest.mark.parametrize("param_names", list_of_values)
#
#   - param_names: comma-separated string matching the test's extra parameters
#   - list_of_values: list of scalars (single param) or tuples (multiple params)
#
# Each tuple becomes one test case. pytest names them automatically:
#   test_square[2-4]
#   test_square[3-9]
#
# You can also stack multiple @parametrize decorators — pytest generates the
# cartesian product of all combinations (every combo of both sets).


# --- Example 1: Single parameter ---


def is_even(n):
    return n % 2 == 0


@pytest.mark.parametrize(
    "n, expected",
    [
        (2, True),
        (3, False),
        (0, True),
        (-4, True),
        (7, False),
    ],
)
def test_is_even(n, expected):
    assert is_even(n) == expected


# --- Example 2: Multiple parameters, real function under test ---


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


@pytest.mark.parametrize(
    "value, lo, hi, expected",
    [
        (5, 0, 10, 5),  # in range → unchanged
        (-1, 0, 10, 0),  # below lo → clamped to lo
        (15, 0, 10, 10),  # above hi → clamped to hi
        (0, 0, 10, 0),  # on lo boundary
        (10, 0, 10, 10),  # on hi boundary
    ],
)
def test_clamp(value, lo, hi, expected):
    assert clamp(value, lo, hi) == expected


# --- Example 3: pytest.param — custom IDs and marks per case ---
# By default pytest generates IDs like test_clamp[5-0-10-5].
# pytest.param lets you give readable IDs and even skip/xfail individual cases.


@pytest.mark.parametrize(
    "n, expected",
    [
        pytest.param(1, 1, id="one"),
        pytest.param(5, 120, id="five"),  # 5! = 120
        pytest.param(0, 1, id="zero"),
    ],
)
def test_factorial(n, expected):
    import math

    assert math.factorial(n) == expected


# --- Example 4: Stacked parametrize = cartesian product ---
# Two decorators → every combination of their values.
# 3 bases × 3 exponents = 9 test cases generated automatically.


@pytest.mark.parametrize("exp", [0, 1, 2])
@pytest.mark.parametrize("base", [2, 3, 5])
def test_power_cartesian(base, exp):
    assert base**exp == pow(base, exp)  # trivially true — shows the pattern


# -----------------------------------------------------------------------------
# 3. BUILT-IN FIXTURES (tmp_path, capsys, capfd)
# -----------------------------------------------------------------------------
# pytest ships with a set of ready-made fixtures you get for free — no import,
# no setup. Just name them as test parameters and pytest injects them.
#
# The three most useful built-ins:
#
#   tmp_path   — a fresh, empty pathlib.Path directory unique to each test.
#                Automatically cleaned up after the session.
#                JS equivalent: using os.tmpdir() + manual cleanup, or tmp-dir npm pkg.
#
#   capsys     — captures what your code prints to stdout/stderr as Python strings.
#                Call capsys.readouterr() → returns a named tuple (out, err).
#                JS equivalent: jest.spyOn(console, 'log')
#
#   capfd      — same as capsys but captures at the file-descriptor level.
#                Catches output from C extensions or subprocesses too.
#                Use capsys for pure Python; capfd when spawning subprocesses.
#
# There are others (monkeypatch, request, recwarn…) — covered in later concepts.
# These three come up constantly when testing file I/O and console output.


# --- tmp_path: safe file I/O in tests ---
# Every test that uses tmp_path gets its own isolated directory.
# No risk of tests interfering with each other or leaving temp files behind.


def write_lines(path, lines):
    """Write a list of strings to a file, one per line."""
    path.write_text("\n".join(lines))


def read_lines(path):
    """Read a file and return a list of non-empty lines."""
    return [line for line in path.read_text().splitlines() if line]


def test_tmp_path_basic(tmp_path):
    # tmp_path is a pathlib.Path pointing to a unique empty dir
    assert tmp_path.is_dir()

    f = tmp_path / "data.txt"
    write_lines(f, ["hello", "world"])

    result = read_lines(f)
    assert result == ["hello", "world"]


def test_tmp_path_isolation(tmp_path):
    # Each test gets its OWN tmp_path — completely separate from other tests.
    # Writing here doesn't affect test_tmp_path_basic's directory.
    f = tmp_path / "other.txt"
    f.write_text("isolated")
    assert f.read_text() == "isolated"


def test_tmp_path_subdirs(tmp_path):
    # You can create subdirectory trees inside tmp_path
    subdir = tmp_path / "nested" / "deep"
    subdir.mkdir(parents=True)

    f = subdir / "file.txt"
    f.write_text("deep content")

    assert f.read_text() == "deep content"
    assert f.parent == subdir


# --- capsys: capture stdout/stderr ---
# capsys.readouterr() returns a namedtuple with .out and .err strings.
# Calling it also resets the capture buffer — so you can call it multiple times.


def greet(name):
    print(f"Hello, {name}!")  # stdout
    import sys

    print("debug info", file=sys.stderr)  # stderr


def test_capsys_stdout(capsys):
    greet("ada")
    captured = capsys.readouterr()  # drain the buffer
    assert captured.out == "Hello, ada!\n"
    assert captured.err == "debug info\n"


def test_capsys_multiple_reads(capsys):
    # readouterr() resets the buffer each time — useful for multi-step tests
    print("first")
    first = capsys.readouterr()
    assert first.out == "first\n"

    print("second")
    second = capsys.readouterr()
    assert second.out == "second\n"  # "first" is gone — buffer was reset


def test_capsys_no_output(capsys):
    # If nothing was printed, out and err are empty strings
    _ = 1 + 1  # no side effects
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


# --- capfd: file-descriptor level capture ---
# Same API as capsys (.readouterr()), but intercepts at the OS fd level.
# Needed when code calls C libraries or subprocesses that bypass sys.stdout.

import subprocess  # noqa: E402


def test_capfd_subprocess(capfd):
    # subprocess output bypasses Python's sys.stdout — capsys would miss it.
    # capfd captures at the fd level, so it catches subprocess output too.
    subprocess.run(["echo", "from subprocess"], check=True)
    captured = capfd.readouterr()
    assert "from subprocess" in captured.out


# -----------------------------------------------------------------------------
# 4. EXCEPTION TESTING (pytest.raises)
# -----------------------------------------------------------------------------
# pytest.raises is a context manager that asserts a specific exception is raised.
# If the exception is NOT raised, the test fails.
#
# JS/Jest comparison:
#   expect(() => fn()).toThrow(Error)
#   expect(() => fn()).toThrow('message substring')
#
# Python equivalent:
#   with pytest.raises(ValueError):
#       fn()
#
# You can also capture the exception info to inspect message, type, etc.:
#   with pytest.raises(ValueError) as exc_info:
#       fn()
#   assert "too small" in str(exc_info.value)
#
# exc_info attributes:
#   exc_info.type     — the exception class (e.g. ValueError)
#   exc_info.value    — the exception instance (call str() to get message)
#   exc_info.tb       — the traceback object
#
# match= shortcut: pass a regex string to assert the message in one step:
#   with pytest.raises(ValueError, match="too small"):
#       fn()
#
# pytest.raises vs bare try/except in tests:
#   try/except can silently pass if the wrong exception fires.
#   pytest.raises is explicit — wrong exception type = test failure, not a catch.


def parse_age(value):
    """Parse a positive integer age from a string."""
    n = int(value)  # raises ValueError if not numeric
    if n < 0:
        raise ValueError(f"Age cannot be negative: {n}")
    if n > 150:
        raise ValueError(f"Age unreasonably large: {n}")
    return n


# --- Basic: assert an exception is raised ---


def test_raises_basic():
    with pytest.raises(ValueError):
        parse_age("not_a_number")


# --- Capture exc_info to inspect the message ---


def test_raises_inspect_message():
    with pytest.raises(ValueError) as exc_info:
        parse_age("-5")

    assert exc_info.type is ValueError
    assert "negative" in str(exc_info.value)


# --- match= shortcut: regex against the exception message ---


def test_raises_match():
    with pytest.raises(ValueError, match="unreasonably large"):
        parse_age("999")


# --- Wrong exception type fails the test ---
# (This test shows that pytest.raises is strict about exception type.)


def test_raises_type_error():
    # int("abc") raises ValueError, NOT TypeError.
    # If we ask for TypeError, the test would fail — showing pytest.raises is exact.
    # Here we correctly ask for ValueError:
    with pytest.raises(ValueError):
        int("abc")


# --- pytest.raises with parametrize: table of bad inputs ---


@pytest.mark.parametrize(
    "bad_input, expected_match",
    [
        ("abc", "invalid literal"),  # int() failure message
        ("-1", "negative"),
        ("200", "unreasonably large"),
    ],
)
def test_raises_parametrized(bad_input, expected_match):
    with pytest.raises(ValueError, match=expected_match):
        parse_age(bad_input)


# --- Assert NO exception is raised (the positive case) ---
# There's no pytest.not_raises — just call the function normally.
# If it raises, the test fails automatically.


def test_no_exception_raised():
    result = parse_age("25")
    assert result == 25


# -----------------------------------------------------------------------------
# 5. MARKERS (skip, xfail, custom)
# -----------------------------------------------------------------------------
# Markers are decorators that attach metadata to test functions.
# pytest has several built-in markers and lets you define your own.
#
# Built-in markers covered here:
#   @pytest.mark.skip        — unconditionally skip a test
#   @pytest.mark.skipif      — skip based on a condition
#   @pytest.mark.xfail       — expect the test to fail (known broken)
#
# JS/Jest comparison:
#   @pytest.mark.skip    ↔  test.skip(...)  or  xit(...)
#   @pytest.mark.skipif  ↔  no direct equivalent (manual if in beforeAll)
#   @pytest.mark.xfail   ↔  no direct equivalent in Jest
#
# Why xfail matters:
#   A test marked xfail that FAILS  → reported as "xfail" (expected) — green
#   A test marked xfail that PASSES → reported as "xpass" (unexpected pass)
#   This lets you document known bugs without hiding them from the suite.
#
# Custom markers:
#   Define your own with @pytest.mark.<name> and register them in pytest.ini
#   to avoid warnings. Use -m "slow" on the CLI to run only marked tests.
#
# CLI filtering:
#   pytest -m "slow"           # run only tests marked slow
#   pytest -m "not slow"       # skip tests marked slow
#   pytest -m "slow and db"    # boolean expressions work


# --- skip: unconditionally skip ---


@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    assert False  # body never runs — shown as 's' in output


# --- skipif: condition-based skip ---

import sys  # noqa: E402


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX only")
def test_posix_paths():
    from pathlib import PurePosixPath

    p = PurePosixPath("/usr/local/bin")
    assert p.parts == ("/", "usr", "local", "bin")


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python 3.10+")
def test_requires_310():
    # typing.TypeAlias was added in 3.10 — raises AttributeError on 3.9
    # skipif prevents this test from running on 3.9 entirely
    import typing

    assert hasattr(typing, "TypeAlias")


# --- xfail: expected failure ---


@pytest.mark.xfail(reason="bug #42: division rounds incorrectly")
def test_known_bug():
    # This test currently passes, so it will be reported as XPASS.
    # Change assert to `assert 1 / 3 == 0.333` to see true xfail behaviour.
    assert round(1 / 3, 3) == 0.333


@pytest.mark.xfail(strict=True, reason="must stay broken until bug is fixed")
def test_strict_xfail():
    # strict=True: if this unexpectedly PASSES, the test is marked as FAILED.
    # Use this to enforce that a known bug hasn't been silently "fixed" in a
    # way that masks the real issue.
    assert 0.1 + 0.2 == 0.3  # classic float precision bug — always fails


# --- Custom markers ---
# Register markers in pytest.ini to avoid "Unknown mark" warnings.
# This repo's pytest.ini is checked next — for now we define and use them.


@pytest.mark.slow
def test_marked_slow():
    # Run only via: pytest -m slow
    assert sum(range(1000)) == 499500


@pytest.mark.parametrize("n", [1, 2, 3])
@pytest.mark.slow
def test_slow_parametrized(n):
    # Markers and parametrize compose freely
    assert n > 0


# -----------------------------------------------------------------------------
# 6. MONKEYPATCH
# -----------------------------------------------------------------------------
# monkeypatch is a built-in fixture that temporarily replaces attributes,
# environment variables, dict entries, and more — for the duration of one test.
# Everything is automatically restored after the test, even on failure.
#
# JS/Jest comparison:
#   jest.spyOn(obj, 'method').mockImplementation(fn)  → monkeypatch.setattr
#   process.env.FOO = 'bar' + afterEach restore        → monkeypatch.setenv
#   jest.restoreAllMocks()                             → automatic (no call needed)
#
# Key methods:
#   monkeypatch.setattr(obj, "attr", value)   — replace any attribute
#   monkeypatch.setattr("module.path.name", value)  — dotted string form
#   monkeypatch.setenv("VAR", "value")        — set env var
#   monkeypatch.delenv("VAR", raising=False)  — delete env var
#   monkeypatch.setitem(dict, "key", value)   — patch a dict entry
#   monkeypatch.delitem(dict, "key")          — remove a dict entry
#   monkeypatch.chdir(path)                   — change working directory
#
# When to use monkeypatch vs unittest.mock (concept 8):
#   monkeypatch — simple attribute/value swaps, env vars, dicts
#   unittest.mock — when you need call tracking, return values, side effects


import os  # noqa: E402


# --- setattr: replace a function on a module ---
# The classic use case: patch out I/O so tests run offline/fast.


def get_username():
    """Reads the OS login name — real I/O we don't want in tests."""
    return os.getlogin()


def test_setattr_module_function(monkeypatch):
    # Replace os.getlogin with a lambda for this test only
    monkeypatch.setattr(os, "getlogin", lambda: "test_user")
    assert get_username() == "test_user"
    # After the test, os.getlogin is restored to the real implementation


# --- setattr with dotted string form ---
# Useful when you can't easily import the object directly.


def test_setattr_dotted(monkeypatch):
    monkeypatch.setattr("os.sep", "!")  # replace path separator
    assert os.sep == "!"


# os.sep is back to "/" here


# --- setenv / delenv: patch environment variables ---


def get_api_url():
    """Read config from env — common real-world pattern."""
    return os.environ.get("API_URL", "http://localhost")


def test_setenv(monkeypatch):
    monkeypatch.setenv("API_URL", "http://staging.example.com")
    assert get_api_url() == "http://staging.example.com"


def test_delenv_missing_key(monkeypatch):
    # raising=False: don't error if the key doesn't exist
    monkeypatch.delenv("API_URL", raising=False)
    assert get_api_url() == "http://localhost"  # falls back to default


# --- setitem: patch a dictionary ---
# Useful for config dicts, registries, or caches your code reads from.

CONFIG = {"debug": False, "timeout": 30}


def is_debug():
    return CONFIG["debug"]


def test_setitem(monkeypatch):
    monkeypatch.setitem(CONFIG, "debug", True)
    assert is_debug() is True


# CONFIG["debug"] is False again here


# --- Combining monkeypatch with tmp_path ---
# monkeypatch.chdir() + tmp_path: move into a clean dir for the test,
# so code that uses relative paths or cwd() behaves predictably.


def write_report():
    """Writes a file relative to cwd — sensitive to current directory."""
    from pathlib import Path

    Path("report.txt").write_text("done")


def test_chdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # cwd is now the isolated temp dir
    write_report()
    assert (tmp_path / "report.txt").read_text() == "done"


# -----------------------------------------------------------------------------
# 7. conftest.py
# -----------------------------------------------------------------------------
# conftest.py is a special file pytest discovers automatically.
# Fixtures defined in it are available to every test in the same directory
# and all subdirectories — no import statement needed.
#
# JS comparison:
#   No direct equivalent. Closest analogy: a shared __mocks__ directory or
#   a Jest globalSetup file, but conftest.py is more granular and composable.
#
# How pytest finds conftest.py files:
#   pytest walks up from the test file toward the rootdir, collecting every
#   conftest.py it finds. Fixtures from parent conftest files are available
#   to child directories — scope is hierarchical.
#
#   rootdir/
#     conftest.py          ← fixtures available to ALL tests
#     python/
#       conftest.py        ← fixtures available to all python/ tests
#       phase8/
#         conftest.py      ← fixtures available to phase8/ tests only  ← ours
#         lessons.py
#         problems.py
#
# Key rules:
#   - No import needed — pytest injects conftest fixtures by name, same as
#     fixtures defined in the test file itself.
#   - If a fixture name collides, the closest conftest.py wins (most specific).
#   - conftest.py can also define hooks (pytest_configure, pytest_collection_
#     modifyitems, etc.) for advanced plugin-like behaviour.
#
# What lives in conftest.py vs inline in the test file:
#   conftest.py  → fixtures reused across multiple files (db connections,
#                  shared test data, expensive setup)
#   inline       → fixtures used by only one file


# --- Using fixtures from conftest.py — no import, just name them as params ---
# `base_user` and `admin_user` are defined in python/phase8/conftest.py


def test_conftest_base_user(base_user):
    # base_user comes from conftest.py — pytest found and injected it
    assert base_user["name"] == "ada"
    assert base_user["active"] is True


def test_conftest_admin_user(admin_user):
    assert admin_user["role"] == "admin"


# --- conftest fixture + local fixture composition ---
# A local fixture can depend on a conftest fixture.


@pytest.fixture
def display_name(base_user):  # base_user from conftest.py
    return base_user["name"].upper()


def test_local_uses_conftest(display_name):
    assert display_name == "ADA"


# --- Module-scoped conftest fixture shared across tests in this file ---
# shared_counter is scope="module" in conftest.py — one instance per file.


def test_shared_counter_a(shared_counter):
    shared_counter["value"] += 1
    assert shared_counter["value"] == 1


def test_shared_counter_b(shared_counter):
    # Same dict — not recreated between tests in this module
    shared_counter["value"] += 1
    assert shared_counter["value"] == 2


# --- Fixture override: local fixture shadows conftest fixture by name ---
# If you redefine a fixture with the same name in a test file, the local
# version wins for ALL tests in that file — pytest collects fixtures at
# module level, so placement inside the file doesn't matter.
#
# Because of this whole-file effect, overrides are best done intentionally:
# define the override at the TOP of the file so the shadowing is obvious.
#
# Here we demo the concept with a separate name to avoid clobbering the
# conftest fixtures used in the tests above.


@pytest.fixture
def privileged_user(admin_user):  # admin_user from conftest — still reachable
    # Extends the conftest fixture rather than replacing it outright
    return {**admin_user, "sudo": True}


def test_fixture_extension(privileged_user):
    assert privileged_user["role"] == "admin"
    assert privileged_user["sudo"] is True


# -----------------------------------------------------------------------------
# 8. unittest.mock (Mock, MagicMock, patch)
# -----------------------------------------------------------------------------
# unittest.mock lets you replace objects with fakes that record how they were
# called, return controlled values, and raise controlled exceptions.
#
# JS/Jest comparison:
#   jest.fn()                          → Mock() / MagicMock()
#   mockFn.mockReturnValue(x)          → mock.return_value = x
#   mockFn.mockRejectedValue(err)      → mock.side_effect = SomeError(...)
#   expect(fn).toHaveBeenCalledWith(x) → mock.assert_called_once_with(x)
#   jest.spyOn(obj, 'method')          → patch.object(obj, 'method')
#   jest.mock('module')                → patch('module.Thing')
#
# Mock vs MagicMock:
#   Mock        — basic mock, no magic methods (__len__, __iter__, etc.)
#   MagicMock   — Mock + all magic methods pre-configured. Use this by default.
#
# Three ways to apply patch:
#   1. patch() as a context manager  — with patch(...) as mock:
#   2. patch() as a decorator        — @patch('module.name')
#   3. patch.object()                — patch one attribute on a specific object
#
# Critical rule — patch where it's USED, not where it's DEFINED:
#   If your code does `import os` then calls `os.getlogin()`,
#   patch 'os.getlogin' (where it lives).
#   If your code does `from os import getlogin` then calls `getlogin()`,
#   patch 'your_module.getlogin' (where it was imported into).

from unittest.mock import Mock, MagicMock, patch, call  # noqa: E402


# --- Mock basics: return_value, call tracking ---


def test_mock_return_value():
    m = Mock(return_value=42)
    assert m() == 42
    assert m.called is True
    assert m.call_count == 1


def test_mock_call_args():
    m = Mock()
    m("hello", key="world")
    m.assert_called_once_with("hello", key="world")


def test_mock_multiple_calls():
    m = Mock()
    m(1)
    m(2)
    m(3)
    assert m.call_count == 3
    # call() objects let you assert the full call history
    assert m.call_args_list == [call(1), call(2), call(3)]


# --- side_effect: raise exceptions or return a sequence ---


def test_mock_side_effect_exception():
    m = Mock(side_effect=ValueError("boom"))
    with pytest.raises(ValueError, match="boom"):
        m()


def test_mock_side_effect_sequence():
    # Each call pops the next value from the list
    m = Mock(side_effect=[10, 20, 30])
    assert m() == 10
    assert m() == 20
    assert m() == 30


# --- patch() as context manager — replaces for the duration of the `with` block ---


def fetch_status():
    """Real code that calls os.getlogin — we want to test without the OS."""
    return f"logged in as {os.getlogin()}"


def test_patch_context_manager():
    with patch("os.getlogin", return_value="mock_user"):
        result = fetch_status()
    assert result == "logged in as mock_user"
    # os.getlogin is restored here — outside the with block


# --- patch() as decorator — cleaner for whole-test patches ---


@patch("os.getlogin", return_value="decorator_user")
def test_patch_decorator(mock_getlogin):
    # mock_getlogin is injected as the last parameter (before fixtures)
    result = fetch_status()
    assert result == "logged in as decorator_user"
    mock_getlogin.assert_called_once()


# --- patch.object() — patch one attribute on an object you already have ---


class EmailService:
    def send(self, to, subject):
        raise RuntimeError("would send real email in prod")


def notify_user(service, email):
    service.send(email, "Welcome!")
    return True


def test_patch_object():
    svc = EmailService()
    with patch.object(svc, "send") as mock_send:
        result = notify_user(svc, "ada@example.com")
    assert result is True
    mock_send.assert_called_once_with("ada@example.com", "Welcome!")


# --- MagicMock: magic methods work out of the box ---


def test_magic_mock_len():
    m = MagicMock()
    m.__len__.return_value = 5
    assert len(m) == 5  # works — Mock() would raise TypeError here


def test_magic_mock_iteration():
    m = MagicMock()
    m.__iter__.return_value = iter([1, 2, 3])
    assert list(m) == [1, 2, 3]
