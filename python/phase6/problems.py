# ============================================================================
# PHASE 6: Error Handling & Context Managers - PROBLEMS
# ============================================================================
# Practice problems for Phase 6 concepts.
# Run tests: npm run test:py -- python/phase6/problems.py

from functools import wraps
import os
import time
from contextlib import contextmanager
from typing import Any, Callable, Optional


# -----------------------------------------------------------------------------
# PROBLEM 1: safe_divide
# -----------------------------------------------------------------------------
# Create a function `safe_divide(a, b)` that returns:
#   - The result of a / b if successful
#   - None if division by zero
#   - Raises TypeError if inputs aren't numbers
#
# Example:
#   safe_divide(10, 2) -> 5.0
#   safe_divide(10, 0) -> None
#   safe_divide("10", 2) -> TypeError
#
# JS equivalent: Manual type checking + try/catch
#
# Hints:
# - Check types first with isinstance(x, (int, float))
# - Catch ZeroDivisionError
#


def safe_divide(a, b):
    if any(not isinstance(x, (int, float)) for x in (a, b)):
        raise TypeError('argument is not a number')
    
    try:
        return a / b
    except ZeroDivisionError:
        return None


def test_safe_divide():
    # Normal division
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(7, 2) == 3.5

    # Division by zero returns None
    assert safe_divide(10, 0) is None
    assert safe_divide(0, 0) is None

    # Invalid types raise TypeError
    try:
        safe_divide("10", 2)
        assert False, "Should have raised TypeError"
    except TypeError:
        pass

    try:
        safe_divide(10, "2")
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


# -----------------------------------------------------------------------------
# PROBLEM 2: parse_int_safe
# -----------------------------------------------------------------------------
# Create a function `parse_int_safe(s, default=0)` that:
#   - Converts string to int if possible
#   - Returns default if conversion fails
#
# Example:
#   parse_int_safe("42") -> 42
#   parse_int_safe("abc") -> 0
#   parse_int_safe("abc", -1) -> -1
#
# JS equivalent: parseInt with fallback
#
# Hints:
# - int() raises ValueError for invalid strings
# - Use try/except with else clause
#


def parse_int_safe(s, default: Optional[int] = 0):
    try:
        return int(s)
    except ValueError:
        return default


def test_parse_int_safe():
    # Valid integers
    assert parse_int_safe("42") == 42
    assert parse_int_safe("-17") == -17
    assert parse_int_safe("0") == 0

    # Invalid strings return default
    assert parse_int_safe("abc") == 0
    assert parse_int_safe("12.5") == 0  # float string not valid for int()
    assert parse_int_safe("") == 0

    # Custom default
    assert parse_int_safe("abc", -1) == -1
    assert parse_int_safe("xyz", None) is None


# -----------------------------------------------------------------------------
# PROBLEM 3: retry
# -----------------------------------------------------------------------------
# Create a function `retry(func, max_attempts=3)` that:
#   - Calls func() up to max_attempts times
#   - Returns the result if successful
#   - If all attempts fail, raises the last exception
#
# Example:
#   count = 0
#   def flaky():
#       nonlocal count
#       count += 1
#       if count < 3:
#           raise ValueError("not yet")
#       return "success"
#   retry(flaky) -> "success"  (after 3 attempts)
#
# JS equivalent: async retry with catch
#
# Hints:
# - Loop max_attempts times
# - Catch Exception, store it, continue
# - After loop, raise the last exception
#


def retry(func, max_attempts=3):
    last_exception = None

    for _ in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_exception = e
    if last_exception is not None:
        raise last_exception


def test_retry():
    # Succeeds on first try
    assert retry(lambda: "ok") == "ok"

    # Succeeds on third try
    attempts = [0]

    def flaky():
        attempts[0] += 1
        if attempts[0] < 3:
            raise ValueError("not yet")
        return "success"

    assert retry(flaky) == "success"
    assert attempts[0] == 3

    # Fails all attempts
    def always_fails():
        raise RuntimeError("always fails")

    try:
        retry(always_fails, max_attempts=2)
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert str(e) == "always fails"


# -----------------------------------------------------------------------------
# PROBLEM 4: ValidatedString (custom exception)
# -----------------------------------------------------------------------------
# Create:
#   1. A custom exception `StringTooShortError` with attributes:
#      - value: the invalid string
#      - min_length: the required minimum
#   2. A function `validate_string(s, min_length=1)` that:
#      - Raises StringTooShortError if len(s) < min_length
#      - Returns s if valid
#
# Example:
#   validate_string("hello", 3) -> "hello"
#   validate_string("hi", 5) -> raises StringTooShortError
#
# Hints:
# - Custom exception inherits from Exception
# - Store attributes in __init__, call super().__init__(message)
#


class StringTooShortError(Exception):
    def __init__(self, value: str, min_length: int):
        super().__init__(f"String '{value}' too short (min: {min_length})")
        self.value = value
        self.min_length = min_length

def validate_string(s, min_length=1):
    if len(s) < min_length:
        raise StringTooShortError(s, min_length)

    return s

def test_validated_string():
    # Valid strings
    assert validate_string("hello", 3) == "hello"
    assert validate_string("a", 1) == "a"
    assert validate_string("test") == "test"

    # Too short
    try:
        validate_string("hi", 5)
        assert False, "Should have raised StringTooShortError"
    except StringTooShortError as e:
        assert e.value == "hi"
        assert e.min_length == 5

    # Empty string
    try:
        validate_string("", 1)
    except StringTooShortError as e:
        assert e.value == ""
        assert e.min_length == 1


# -----------------------------------------------------------------------------
# PROBLEM 5: Indenter (context manager class)
# -----------------------------------------------------------------------------
# Create a context manager class `Indenter` that tracks indentation level.
#   - Each nested `with` increases indent by a configurable amount
#   - Has a `print(text)` method that prints with current indentation
#   - Supports reuse (indent level resets between uses)
#
# Example:
#   ind = Indenter(indent="  ")
#   with ind:
#       ind.print("level 1")      # "  level 1"
#       with ind:
#           ind.print("level 2")  # "    level 2"
#       ind.print("back to 1")    # "  level 1"
#
# Hints:
# - __enter__ increments level, returns self
# - __exit__ decrements level
# - print method uses level * indent as prefix
#


class Indenter:
    def __init__(self, indent: str, level = 0):
        self.indent = indent  
        self.level = level

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.level -= 1

    def print(self, text):
        print(self.indent * self.level + text)

def test_indenter(capsys):
    ind = Indenter(indent="  ")

    ind.print("level 0")
    with ind:
        ind.print("level 1")
        with ind:
            ind.print("level 2")
        ind.print("back to 1")
    ind.print("back to 0")

    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert lines[0] == "level 0"
    assert lines[1] == "  level 1"
    assert lines[2] == "    level 2"
    assert lines[3] == "  back to 1"
    assert lines[4] == "back to 0"


# -----------------------------------------------------------------------------
# PROBLEM 6: temp_setattr (context manager function)
# -----------------------------------------------------------------------------
# Create a context manager function `temp_setattr(obj, name, value)` that:
#   - Temporarily sets obj.name = value
#   - Restores the original value (or deletes if it didn't exist) on exit
#
# Example:
#   class Config:
#       debug = False
#
#   with temp_setattr(Config, 'debug', True):
#       print(Config.debug)  # True
#   print(Config.debug)  # False
#
# Hints:
# - Use @contextmanager from contextlib
# - Use hasattr to check if attribute exists
# - Use getattr/setattr/delattr
#

@contextmanager
def temp_setattr(obj, name, value):
    has_attribute = hasattr(obj, name) 
    
    if has_attribute:
        original_value = getattr(obj, name)
    
    setattr(obj, name, value)

    try:
        yield
    finally:
        if has_attribute:
            setattr(obj, name, original_value)
        else:
            delattr(obj, name)


def test_temp_setattr():
    class Config:
        debug = False
        log_level = "INFO"

    # Temporarily change existing attr
    assert Config.debug is False
    with temp_setattr(Config, "debug", True):
        assert Config.debug is True
    assert Config.debug is False

    # Temporarily add new attr
    assert not hasattr(Config, "new_attr")
    with temp_setattr(Config, "new_attr", "temp"):
        assert getattr(Config, "new_attr") == "temp"
    assert not hasattr(Config, "new_attr")


# -----------------------------------------------------------------------------
# PROBLEM 7: FileWriterContext
# -----------------------------------------------------------------------------
# Create a context manager class `FileWriter` that:
#   - Opens a file for writing on enter
#   - Provides a write(text) method
#   - Closes the file on exit
#   - If an exception occurs, deletes the partial file
#
# Example:
#   with FileWriter("out.txt") as fw:
#       fw.write("line 1\n")
#       fw.write("line 2\n")
#   # File contains both lines
#
#   with FileWriter("out.txt") as fw:
#       fw.write("partial")
#       raise ValueError("oops")
#   # File is deleted, not left with partial content
#
# Hints:
# - Store filepath, open in __enter__
# - In __exit__, close file, check if exception occurred
# - Use os.remove() to delete file on error
#

class FileWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'w')
        return self

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        self.file.close()
        if exc_type is not None:
            os.remove(self.file_path)

    def write(self, text: str):
        self.file.write(text)

def test_file_writer(tmp_path):
    filepath = tmp_path / "test.txt"

    # Normal usage
    with FileWriter(str(filepath)) as fw:
        fw.write("hello\n")
        fw.write("world\n")

    assert filepath.read_text() == "hello\nworld\n"

    # Exception causes file deletion
    filepath2 = tmp_path / "test2.txt"
    try:
        with FileWriter(str(filepath2)) as fw:
            fw.write("partial")
            raise ValueError("oops")
    except ValueError:
        pass

    assert not filepath2.exists()


# -----------------------------------------------------------------------------
# PROBLEM 8: collect_errors
# -----------------------------------------------------------------------------
# Create a context manager `collect_errors(*exception_types)` that:
#   - Collects all specified exceptions instead of raising them
#   - Stores them in a .errors list
#   - Allows code to continue after each caught exception
#
# Wait - this is tricky! A context manager can only suppress exceptions
# at the END of the block, not during. So we need a different approach:
#
# Create a function `collect_errors(func, *exception_types)` that:
#   - Calls func()
#   - If it raises one of exception_types, stores it and returns None
#   - Otherwise returns the result
#   - Has a .errors attribute that accumulates caught exceptions
#
# Example:
#   collector = ErrorCollector(ValueError, TypeError)
#   collector.call(lambda: int("abc"))  # Catches ValueError
#   collector.call(lambda: 1 + "a")     # Catches TypeError
#   collector.call(lambda: 1 / 0)       # Raises ZeroDivisionError!
#   len(collector.errors)  # 2
#


class ErrorCollector:
    def __init__(self, *exception_types) -> None:
        self.exception_types = exception_types
        self.errors = []

    def collect_errors(self, function):
        try:
            return function()
        except Exception as e:
            if isinstance(e, self.exception_types):
                self.errors.append(e)
                return None
            raise

def test_error_collector():
    collector = ErrorCollector(ValueError, TypeError)

    # Catches ValueError
    result = collector.collect_errors(lambda: int("abc"))
    assert result is None
    assert len(collector.errors) == 1
    assert isinstance(collector.errors[0], ValueError)

    # Catches TypeError
    bad: Any = "a"
    result = collector.collect_errors(lambda: bad + 1)
    assert result is None
    assert len(collector.errors) == 2

    # Returns result on success
    result = collector.collect_errors(lambda: 42)
    assert result == 42
    assert len(collector.errors) == 2  # No new errors

    # Doesn't catch other exceptions
    try:
        collector.collect_errors(lambda: 1 / 0)
        assert False, "Should have raised ZeroDivisionError"
    except ZeroDivisionError:
        pass


# -----------------------------------------------------------------------------
# PROBLEM 9: ensure_cleanup (decorator)
# -----------------------------------------------------------------------------
# Create a decorator `ensure_cleanup(cleanup_func)` that:
#   - Calls cleanup_func after the decorated function, even if it raises
#   - Similar to finally block behavior
#
# Example:
#   resources = []
#
#   def release():
#       resources.append("released")
#
#   @ensure_cleanup(release)
#   def use_resource():
#       resources.append("using")
#       raise ValueError("oops")
#
#   use_resource()  # raises ValueError
#   # resources == ["using", "released"]
#
# Hints:
# - Decorator takes cleanup_func, returns decorator
# - Use try/finally in the wrapper
# - Use functools.wraps to preserve function metadata
#

def ensure_cleanup(cleanup_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                cleanup_func()
        return wrapper
    return decorator

def test_ensure_cleanup():
    log = []

    def cleanup():
        log.append("cleanup")

    @ensure_cleanup(cleanup)
    def success():
        log.append("success")
        return "result"

    @ensure_cleanup(cleanup)
    def failure():
        log.append("failure")
        raise ValueError("oops")

    # Cleanup runs after success
    result = success()
    assert result == "result"
    assert log == ["success", "cleanup"]

    log.clear()

    # Cleanup runs after failure
    try:
        failure()
    except ValueError:
        pass
    assert log == ["failure", "cleanup"]


# -----------------------------------------------------------------------------
# PROBLEM 10: ChainedError
# -----------------------------------------------------------------------------
# Create a function `fetch_config(key)` that:
#   - Looks up key in a CONFIG dict
#   - If KeyError, raises ConfigError with the original as cause
#   - ConfigError should have a `key` attribute
#
# This practices exception chaining with `raise ... from ...`
#


class ConfigError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Config key not found: {key}")  
        self.key = key

CONFIG = {"database_url": "postgres://localhost", "api_key": "secret123"}


def fetch_config(key):
    try:
        return CONFIG[key]
    
    except KeyError as e:
        raise ConfigError(key) from e


def test_chained_error():
    # Success case
    assert fetch_config("database_url") == "postgres://localhost"

    # Missing key raises ConfigError
    try:
        fetch_config("missing_key")
        assert False, "Should have raised ConfigError"
    except ConfigError as e:
        assert e.key == "missing_key"
        assert isinstance(e.__cause__, KeyError)


# -----------------------------------------------------------------------------
# PROBLEM 11: timed_block (practical)
# -----------------------------------------------------------------------------
# Create a context manager `timed_block(label)` that:
#   - Prints "{label}: started" on enter
#   - Prints "{label}: finished in {seconds:.3f}s" on exit
#   - If exception, prints "{label}: failed in {seconds:.3f}s" then re-raises
#
# Example:
#   with timed_block("fetch"):
#       time.sleep(0.1)
#   # Prints: "fetch: started"
#   # Prints: "fetch: finished in 0.100s"
#
# Hints:
# - Use @contextmanager
# - time.time() for timing
# - try/except/else around yield
#

@contextmanager
def timed_block(label):
    start_time = time.time()
    print(f"{label}: started")

    try:
        yield  # Pause here; the `with` block body runs while paused
    except Exception:
        # Only runs if the `with` block raised an exception
        failed_time = time.time() - start_time
        print(f"{label}: failed in {failed_time:.3f}s")
        raise  # Re-raise so the caller still sees the exception
    else:
        # Only runs if NO exception occurred (skipped if except ran)
        finish_time = time.time() - start_time
        print(f"{label}: finished in {finish_time:.3f}s")

def test_timed_block(capsys):
    # Successful block
    with timed_block("test"):
        time.sleep(0.01)

    output = capsys.readouterr().out
    assert "test: started" in output
    assert "test: finished in 0.0" in output

    # Failed block
    try:
        with timed_block("failing"):
            time.sleep(0.01)
            raise ValueError("oops")
    except ValueError:
        pass

    output = capsys.readouterr().out
    assert "failing: started" in output
    assert "failing: failed in 0.0" in output


# -----------------------------------------------------------------------------
# PROBLEM 12: ResourcePool (advanced)
# -----------------------------------------------------------------------------
# Create a context manager class `ResourcePool` that:
#   - Manages a pool of reusable resources
#   - acquire() returns a resource from the pool (or creates one)
#   - release(resource) returns it to the pool
#   - Can be used as context manager to auto-release
#   - Has max_size limit for pool
#
# Example:
#   pool = ResourcePool(create_func=lambda: Connection(), max_size=5)
#
#   with pool.acquire() as conn:
#       conn.execute("SELECT 1")
#   # conn automatically returned to pool
#
#   # Or manual:
#   conn = pool.get()
#   try:
#       conn.execute("SELECT 1")
#   finally:
#       pool.release(conn)
#
# Hints:
# - Store available resources in a list
# - acquire() pops from list or calls create_func
# - release() appends back (if under max_size)
# - acquire() should return a context manager that calls release on exit
#


class ResourcePool:
    def __init__(self, create_func: Callable, max_size = 5) -> None:
        self._resources = []
        self.create_func = create_func
        self.max_size = max_size

    @contextmanager
    def acquire(self):
        try:    
            if self._resources:
                resource = self._resources.pop()
            else:
                resource = self.create_func()
        
            yield resource
        finally:
            self.release(resource)

    def release(self, resource: str):
        if len(self._resources) < self.max_size:
            self._resources.append(resource)

def test_resource_pool():
    created = [0]

    def create():
        created[0] += 1
        return f"resource-{created[0]}"

    pool = ResourcePool(create_func=create, max_size=2)

    # First acquire creates a new resource
    with pool.acquire() as r1:
        assert r1 == "resource-1"
        assert created[0] == 1

    # Second acquire reuses the released resource
    with pool.acquire() as r2:
        assert r2 == "resource-1"  # Reused!
        assert created[0] == 1  # No new creation

    # Concurrent acquires
    with pool.acquire() as r1:
        with pool.acquire() as r2:
            assert r1 == "resource-1"
            assert r2 == "resource-2"  # New one created
            assert created[0] == 2
