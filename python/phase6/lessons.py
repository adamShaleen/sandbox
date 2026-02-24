# ============================================================================
# PHASE 6: Error Handling & Context Managers - LESSONS
# ============================================================================
# Python's error handling and resource management patterns.
# Coming from JS/TS, you'll find similarities but also key differences.

from contextlib import contextmanager, suppress, redirect_stdout
from io import StringIO
from typing import Any


# -----------------------------------------------------------------------------
# 1. BASIC TRY/EXCEPT (vs JS try/catch)
# -----------------------------------------------------------------------------
# Python uses `except` instead of `catch`.
# Use `as e` to bind the exception to a variable (like JS `catch (e)`).
#
# Syntax:
#   try:
#       risky_code()
#   except SomeError as e:    # `as e` is optional - binds exception to `e`
#       handle_error(e)

# JS:
#   try {
#     riskyOperation();
#   } catch (error) {
#     console.error(error.message);
#   }


# Python:
def demo_basic_try():
    try:
        # This line raises ZeroDivisionError before result can be used.
        # The variable is assigned but never accessed because the exception
        # immediately jumps to the except block. This is intentional to
        # demonstrate that code after an exception doesn't run.
        result = 1 / 0  # noqa: F841 (unused variable - intentional demo)
    except ZeroDivisionError as e:
        return f"Caught: {e}"

    return "No error"


def test_basic_try():
    assert demo_basic_try() == "Caught: division by zero"


# -----------------------------------------------------------------------------
# 2. MULTIPLE EXCEPTION TYPES
# -----------------------------------------------------------------------------
# Can catch different exceptions differently.

# JS: Must check error type manually in catch block
# Python: Separate except clauses or tuple of types


def handle_multiple(value):
    try:
        if value == "key":
            d = {}
            return d["missing"]
        elif value == "index":
            lst = []
            return lst[10]
        elif value == "type":
            x: Any = "hello"
            return x + 5
        return "ok"
    except KeyError:
        return "missing key"
    except IndexError:
        return "bad index"
    except TypeError:
        return "type mismatch"


def test_multiple_exceptions():
    assert handle_multiple("key") == "missing key"
    assert handle_multiple("index") == "bad index"
    assert handle_multiple("type") == "type mismatch"
    assert handle_multiple("none") == "ok"


# Catch multiple types with tuple:
def handle_grouped(value):
    try:
        if value == "key":
            return {}["missing"]
        elif value == "index":
            return [][10]
        return "ok"
    except (KeyError, IndexError) as e:
        # type(e) returns the class of e (e.g., <class 'KeyError'>)
        # __name__ is an attribute of classes containing the class name as string
        # JS equivalent: e.constructor.name
        return f"lookup error: {type(e).__name__}"


def test_grouped_exceptions():
    assert handle_grouped("key") == "lookup error: KeyError"
    assert handle_grouped("index") == "lookup error: IndexError"


# -----------------------------------------------------------------------------
# 3. ELSE AND FINALLY
# -----------------------------------------------------------------------------
# Python has try/except/else/finally. JS only has try/catch/finally.
#
# else: runs if NO exception occurred (unique to Python)
# finally: always runs (same as JS)


def try_else_finally(should_fail):
    result = []

    try:
        if should_fail:
            raise ValueError("oops")
        result.append("try")
    except ValueError:
        result.append("except")
    else:
        # Only runs if no exception!
        result.append("else")
    finally:
        # Always runs
        result.append("finally")

    return result


def test_else_finally():
    # No exception: try -> else -> finally
    assert try_else_finally(False) == ["try", "else", "finally"]

    # Exception: try -> except -> finally (no else!)
    assert try_else_finally(True) == ["except", "finally"]


# -----------------------------------------------------------------------------
# 4. RAISING EXCEPTIONS
# -----------------------------------------------------------------------------
# Python: raise Exception("msg")
# JS: throw new Error("msg")


def validate_age(age):
    # isinstance(obj, type) checks if obj is an instance of type
    # JS equivalent: typeof age !== 'number' (but Python has int vs float)
    # Can also check multiple types: isinstance(age, (int, float))
    if not isinstance(age, int):
        raise TypeError("age must be an integer")
    if age < 0:
        raise ValueError("age cannot be negative")
    if age > 150:
        raise ValueError("age seems unrealistic")
    return True


def test_raise():
    assert validate_age(25) is True

    try:
        validate_age(-5)
    except ValueError as e:
        assert str(e) == "age cannot be negative"

    try:
        validate_age("twenty")
    except TypeError as e:
        assert str(e) == "age must be an integer"


# Re-raising: use bare `raise` to re-raise current exception
def log_and_reraise(func):
    try:
        return func()
    except Exception as e:
        print(f"Logging error: {e}")
        raise  # Re-raises the same exception with original traceback


# -----------------------------------------------------------------------------
# 5. EXCEPTION HIERARCHY
# -----------------------------------------------------------------------------
# Python exceptions form a hierarchy. Catching a parent catches children too.
#
# BaseException
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   └── Exception  <-- catch this for "normal" errors
#         ├── ValueError
#         ├── TypeError
#         ├── LookupError
#         │     ├── KeyError
#         │     └── IndexError
#         ├── OSError
#         │     ├── FileNotFoundError
#         │     └── PermissionError
#         └── ... many more


def test_hierarchy():
    # KeyError is a LookupError
    try:
        {}["missing"]
    except LookupError:
        pass  # Catches KeyError

    # IndexError is also a LookupError
    try:
        [][0]
    except LookupError:
        pass  # Catches IndexError


# Avoid bare except or catching Exception too broadly:
# BAD:  except:  (catches everything including KeyboardInterrupt)
# BAD:  except Exception:  (too broad, hides bugs)
# GOOD: except SpecificError:  (catch what you expect)


# -----------------------------------------------------------------------------
# 6. CUSTOM EXCEPTIONS
# -----------------------------------------------------------------------------
# Create custom exceptions by inheriting from Exception.

# JS:
#   class ValidationError extends Error {
#     constructor(message) {
#       super(message);
#       this.name = 'ValidationError';
#     }
#   }


# Python:
class ValidationError(Exception):
    """Raised when validation fails."""

    # `pass` is required when a class/function body is empty.
    # This creates a new exception type with no extra behavior.
    # It inherits everything from Exception - we just want a distinct type.
    pass


class InvalidEmailError(ValidationError):
    """Raised for invalid email addresses."""

    def __init__(self, email, message="Invalid email format"):
        # Store custom attributes on the exception instance
        self.email = email
        self.message = message
        # super().__init__() calls the parent class's __init__
        # For exceptions, pass the error message to make str(e) work properly
        # JS equivalent: super(message) in constructor
        super().__init__(f"{message}: {email}")


def validate_email(email):
    if "@" not in email:
        raise InvalidEmailError(email)
    return True


def test_custom_exceptions():
    assert validate_email("user@example.com") is True

    try:
        validate_email("invalid-email")
    except InvalidEmailError as e:
        assert e.email == "invalid-email"
        assert "Invalid email format" in str(e)


# -----------------------------------------------------------------------------
# 7. CONTEXT MANAGERS (with statement)
# -----------------------------------------------------------------------------
# Context managers handle setup/teardown automatically.
# Most common use: file handling.

# JS (no built-in equivalent, must manually close):
#   const file = fs.openSync('file.txt', 'r');
#   try {
#     // use file
#   } finally {
#     fs.closeSync(file);
#   }


# Python (with statement handles cleanup):
def demo_file_context():
    # File is automatically closed when block exits, even if an exception occurs!
    #
    # __file__ is a magic variable containing the current file's path.
    # (Similar to __filename in Node.js, but built into Python)
    #
    # The `as f` binds the opened file object to variable `f`.
    # When the `with` block exits, Python automatically calls f.close().
    with open(__file__) as f:
        first_line = f.readline()
    # f is now closed - accessing f.read() here would fail
    return first_line


def test_file_context():
    line = demo_file_context()
    # First line is the === delimiter, just check it read something
    assert "====" in line or "PHASE" in line


# Multiple context managers:
def demo_multiple_contexts(path1, path2):
    with open(path1) as f1, open(path2) as f2:
        return f1.readline(), f2.readline()


# -----------------------------------------------------------------------------
# 8. CREATING CONTEXT MANAGERS (class-based)
# -----------------------------------------------------------------------------
# To create a class-based context manager, implement two "dunder" methods:
#
#   __enter__(self) - Called when entering the `with` block
#       - Perform setup (open files, acquire locks, start timers, etc.)
#       - Return value becomes the `as` variable (e.g., `with Foo() as x:`)
#       - Often returns `self`, but can return anything
#
#   __exit__(self, exc_type, exc_val, exc_tb) - Called when exiting the block
#       - REQUIRED SIGNATURE: Python always passes these 3 arguments!
#       - exc_type: The exception class (e.g., ValueError), or None if no error
#       - exc_val: The exception instance, or None
#       - exc_tb: The traceback object, or None
#       - Return True to suppress the exception, False (or None) to propagate
#       - Even if you don't use these params, you must accept them!
#
# Convention: Prefix unused params with underscore to indicate intentionally unused


class Timer:
    """Context manager that tracks elapsed time."""

    def __init__(self):
        self.elapsed = 0.0

    def __enter__(self):
        import time

        self.start = time.time()
        return self  # This is what `as` binds to

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        # These 3 params are REQUIRED by Python's context manager protocol.
        # We prefix with _ to indicate we're not using them here.
        # We just want to record elapsed time regardless of success/failure.
        import time

        self.elapsed = time.time() - self.start
        return False  # Don't suppress exceptions (let them propagate)


def test_timer_context():
    import time

    with Timer() as t:
        time.sleep(0.01)

    assert t.elapsed >= 0.01


# __exit__ receives exception info if one occurred:
#   exc_type: exception class (or None)
#   exc_val: exception instance (or None)
#   exc_tb: traceback (or None)
#
# Return True to suppress the exception, False to propagate it.


class SuppressError:
    """Context manager that suppresses a specific exception type."""

    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        # exc_type: We check this to see if an exception occurred and what type
        # _exc_val, _exc_tb: Required params but unused here (prefixed with _)
        #
        # Return True to suppress the exception (caller won't see it)
        # Return False to propagate (exception continues up the stack)
        if exc_type is None:
            return False  # No exception occurred, nothing to suppress

        # issubclass(A, B) checks if class A inherits from class B
        # e.g., issubclass(KeyError, LookupError) is True
        # Works with tuples: issubclass(KeyError, (ValueError, LookupError))
        return issubclass(exc_type, self.exceptions)


def test_suppress():
    with SuppressError(ValueError):
        raise ValueError("ignored")
    # No exception raised to caller

    # Other exceptions still propagate
    try:
        with SuppressError(ValueError):
            raise TypeError("not suppressed")
    except TypeError:
        pass  # This exception propagates


# -----------------------------------------------------------------------------
# 9. CREATING CONTEXT MANAGERS (generator-based with contextlib)
# -----------------------------------------------------------------------------
# Writing __enter__ and __exit__ can be verbose. The @contextmanager decorator
# lets you write a context manager as a generator function instead.
#
# How it works:
#   1. Code BEFORE `yield` runs on enter (like __enter__)
#   2. The yielded value becomes the `as` variable
#   3. Code AFTER `yield` runs on exit (like __exit__)
#   4. Wrap yield in try/finally to ensure cleanup runs even on exception


@contextmanager
def temp_change(obj, attr, value):
    """Temporarily change an attribute, restore on exit."""
    # --- SETUP (runs when entering `with` block) ---
    original = getattr(obj, attr)  # getattr(obj, "foo") is like obj.foo
    setattr(obj, attr, value)  # setattr(obj, "foo", x) is like obj.foo = x

    try:
        yield original  # Pause here; value is bound to `as` variable
        # --- The `with` block body runs while we're paused at yield ---
    finally:
        # --- TEARDOWN (always runs, even if exception in the block) ---
        setattr(obj, attr, original)


class Config:
    debug = False


def test_temp_change():
    config = Config()
    assert config.debug is False

    with temp_change(config, "debug", True) as original:
        assert config.debug is True
        assert original is False

    assert config.debug is False  # Restored!


# Pattern for @contextmanager:
#   @contextmanager
#   def my_context():
#       # setup code
#       try:
#           yield value  # value is bound to `as`
#       finally:
#           # teardown code (always runs)


# -----------------------------------------------------------------------------
# 10. USEFUL CONTEXTLIB UTILITIES
# -----------------------------------------------------------------------------


def test_suppress_builtin():
    # suppress() is a built-in version of our SuppressError
    with suppress(FileNotFoundError):
        open("nonexistent_file.txt")
    # No exception raised


def test_redirect_stdout():
    # Capture stdout
    f = StringIO()
    with redirect_stdout(f):
        print("captured")

    assert f.getvalue() == "captured\n"


# Other useful contextlib tools:
# - closing(thing): calls thing.close() on exit
# - nullcontext(): do-nothing context manager
# - ExitStack(): manage multiple dynamic context managers


# -----------------------------------------------------------------------------
# 11. EXCEPTION CHAINING
# -----------------------------------------------------------------------------
# Python tracks exception causes with `raise ... from ...`
#
# When you catch one exception and raise another, you can link them:
#   raise NewError("message") from original_error
#
# This sets the __cause__ attribute on the new exception, creating a chain.
# Tracebacks will show "The above exception was the direct cause of..."
#
# JS has no built-in equivalent (you'd manually set error.cause property).


class DatabaseError(Exception):
    pass


def fetch_user(user_id):
    try:
        # Simulate a KeyError from missing data
        users = {}
        return users[user_id]
    except KeyError as e:
        # Chain: DatabaseError's __cause__ will be the KeyError
        # Traceback shows both exceptions and their relationship
        raise DatabaseError(f"User {user_id} not found") from e


def test_exception_chaining():
    try:
        fetch_user(123)
    except DatabaseError as e:
        assert "User 123 not found" in str(e)
        assert isinstance(e.__cause__, KeyError)


# `raise ... from None` suppresses the chain:
def fetch_user_clean(user_id):
    try:
        users = {}
        return users[user_id]
    except KeyError:
        raise DatabaseError(f"User {user_id} not found") from None


def test_suppressed_chain():
    try:
        fetch_user_clean(123)
    except DatabaseError as e:
        assert e.__cause__ is None  # Chain suppressed


# -----------------------------------------------------------------------------
# 12. COMMON PATTERNS
# -----------------------------------------------------------------------------


# Pattern: EAFP (Easier to Ask Forgiveness than Permission)
# Python prefers try/except over checking first.

# JS style (LBYL - Look Before You Leap):
#   if (obj.hasOwnProperty('key')) {
#     value = obj.key;
#   }


# Python style (EAFP):
def get_value_eafp(d, key, default=None):
    try:
        return d[key]
    except KeyError:
        return default


# Pattern: Ensure cleanup with context manager
@contextmanager
def acquire_lock(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release()


# Pattern: Transaction-like behavior
@contextmanager
def transaction(connection):
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise


# -----------------------------------------------------------------------------
# SUMMARY
# -----------------------------------------------------------------------------
# - try/except/else/finally: else is unique to Python
# - Catch specific exceptions, avoid bare except
# - Custom exceptions: inherit from Exception
# - Context managers: with statement for resource management
# - Class-based: __enter__ and __exit__
# - Generator-based: @contextmanager decorator
# - Exception chaining: raise ... from ...
# - EAFP: prefer try/except over pre-checking
