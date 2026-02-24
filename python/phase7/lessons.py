# ============================================================================
# PHASE 7: Modules & Packaging - LESSONS
# ============================================================================
# How Python organizes, imports, and distributes code.
# Coming from JS/TS, you'll find some parallels to ESModules and npm.

# Concepts covered:
#   1. Import basics (import, from, as)
#   2. Module search path (sys.path)
#   3. Packages & __init__.py
#   4. Relative vs absolute imports
#   5. __name__ == "__main__"
#   6. The standard library tour
#   7. Third-party packages & pip
#   8. Virtual environments
#   9. pyproject.toml / setup.py basics


# -----------------------------------------------------------------------------
# 1. IMPORT BASICS
# -----------------------------------------------------------------------------
# Python has three import styles. All load a module and bind names in the
# current namespace.
#
# JS/TS comparison:
#   import math from 'math'               → import math
#   import { sqrt } from 'math'           → from math import sqrt
#   import { sqrt as squareRoot } from …  → from math import sqrt as squareRoot
#   import * as math from 'math'          → import math  (same as first)
#
# Key difference: `import math` gives you the module object; you access things
# via `math.sqrt`. `from math import sqrt` pulls `sqrt` directly into scope.

import math  # whole module — access via math.xxx
from math import sqrt  # named import — sqrt is now a local name
from math import pi as PI  # aliased import — PI is now a local name


def demo_import_styles():
    a = math.sqrt(16)  # via module
    b = sqrt(16)  # via named import (same function)
    c = PI  # aliased constant
    return a, b, c


def test_import_styles():
    a, b, c = demo_import_styles()
    assert a == 4.0
    assert b == 4.0
    assert abs(c - 3.14159) < 0.001


# -----------------------------------------------------------------------------
# 2. MODULE SEARCH PATH (sys.path)
# -----------------------------------------------------------------------------
# When you write `import foo`, Python searches a list of directories in order.
# That list is `sys.path`. Think of it like NODE_PATH in Node, but simpler.
#
# Default sys.path order:
#   1. The directory of the script being run (or "" for the REPL/current dir)
#   2. PYTHONPATH env variable directories (if set)
#   3. Standard library directories
#   4. site-packages (where pip installs third-party packages)
#
# You can inspect it at runtime:
#   import sys
#   print(sys.path)
#
# JS comparison:
#   Node resolves: ./node_modules → ../node_modules → ... → global
#   Python resolves: script dir → PYTHONPATH → stdlib → site-packages
#
# You can mutate sys.path at runtime (useful for scripts, bad for libraries):
#   sys.path.insert(0, '/some/other/dir')
#
# First match wins — if two directories both have a `foo.py`, the one earlier
# in sys.path is used. This is how local files can shadow stdlib modules
# (e.g., naming your file `math.py` would break `import math`).

import sys  # noqa: E402


def demo_sys_path():
    # sys.path is just a list of strings
    return isinstance(sys.path, list) and all(isinstance(p, str) for p in sys.path)


def test_sys_path():
    assert demo_sys_path() is True


def demo_first_match_wins():
    # `math` is already imported above — Python caches modules in sys.modules.
    # Re-importing returns the cached version, not a fresh search.
    import math as m1
    import math as m2

    return m1 is m2  # same object — cached in sys.modules


def test_first_match_wins():
    assert demo_first_match_wins() is True


# -----------------------------------------------------------------------------
# 3. PACKAGES & __init__.py
# -----------------------------------------------------------------------------
# A *module* is a single .py file.
# A *package* is a directory containing an __init__.py file.
#
# Directory structure example:
#
#   mypackage/
#     __init__.py        ← makes this directory a package
#     utils.py           ← mypackage.utils
#     math/
#       __init__.py      ← makes this a sub-package
#       vector.py        ← mypackage.math.vector
#
# JS comparison:
#   A JS package is a directory with package.json.
#   __init__.py is roughly like index.js — it runs when you
#   `import mypackage` (the directory itself, not a specific file).
#
# __init__.py can be:
#   - Empty  (just marks the directory as a package — what we do in this repo)
#   - Used to re-export things for a cleaner public API
#
# Re-export pattern (common in libraries):
#
#   # mypackage/__init__.py
#   from mypackage.utils import helper
#
#   # Now users write:        from mypackage import helper
#   # Instead of the full:   from mypackage.utils import helper
#
# Since Python 3.3+, "namespace packages" exist (no __init__.py needed),
# but explicit __init__.py is still the standard for regular packages.

import importlib  # noqa: E402


def demo_package_is_module():
    # A package is itself a module — importlib is a stdlib package.
    # Packages have a __path__ attribute; plain modules do not.
    pkg = importlib.import_module("importlib")
    return hasattr(pkg, "__path__")  # True for packages, False for plain modules


def test_package_is_module():
    assert demo_package_is_module() is True


def demo_init_controls_api():
    # os/__init__.py exposes os.path automatically.
    # That sub-module is available without a separate `import os.path`.
    import os  # noqa: E402

    return callable(os.path.join)


def test_init_controls_api():
    assert demo_init_controls_api() is True


# -----------------------------------------------------------------------------
# 4. RELATIVE vs ABSOLUTE IMPORTS
# -----------------------------------------------------------------------------
# Inside a package, you can import siblings two ways:
#
#   Absolute: from phase7.lessons import something   ← full dotted path from root
#   Relative: from .lessons import something         ← relative to current package
#             from ..phase6.lessons import something ← go up one level, then down
#
# JS comparison:
#   Absolute: import { thing } from 'mypackage/utils'   (bare specifier)
#   Relative: import { thing } from './utils'
#             import { thing } from '../phase6/lessons'
#
# The leading dots in relative imports:
#   .foo   → same package (sibling module)
#   ..foo  → parent package
#   ...foo → grandparent package
#
# When to use which:
#   - Absolute: in scripts, tests, or when crossing package boundaries.
#     More explicit and easier to grep.
#   - Relative: inside a library/package, keeps internals self-contained.
#     If you rename the package, relative imports don't break.
#
# This repo uses absolute imports in lessons/problems because pytest runs
# from the repo root and the phase folders are top-level packages.
#
# One hard rule: relative imports only work inside packages. A plain script
# (run directly with `python script.py`) has __name__ == "__main__" and
# __package__ == None, so relative imports will raise ImportError.


def demo_absolute_import():
    # Absolute import — works from anywhere as long as the package is on sys.path
    from math import factorial  # noqa: E402

    return factorial(5)


def test_absolute_import():
    assert demo_absolute_import() == 120


def demo_relative_would_work_inside_package():
    # We can't easily demo a relative import in this file without a second module,
    # but we can show what __package__ looks like — it tells Python the anchor
    # for resolving dots in relative imports.
    #
    # When run via pytest from the repo root, __package__ for this file is "phase7".
    # A relative import like `from .problems import foo` would resolve to phase7.problems.
    return __package__  # "phase7" when imported as a package module


def test_package_anchor():
    # __package__ is "python.phase7" in this repo because pytest treats
    # python/ as the top-level package and phase7 as a sub-package within it.
    # A relative import like `from .problems import foo` resolves to python.phase7.problems.
    assert demo_relative_would_work_inside_package() == "python.phase7"


# -----------------------------------------------------------------------------
# 5. __name__ == "__main__"
# -----------------------------------------------------------------------------
# Every Python module has a __name__ attribute.
#
#   - When a file is *imported*, __name__ is the module's dotted name
#     (e.g., "python.phase7.lessons")
#   - When a file is *run directly* (`python lessons.py`), __name__ is
#     the special string "__main__"
#
# This lets you write code that only runs when the file is the entry point,
# not when it's imported as a library.
#
# JS comparison:
#   Node doesn't have a direct equivalent for plain .js files, but it's
#   similar to checking `if (require.main === module)` in CommonJS, or
#   using a top-level `if` in an ES module entry point.
#
# Common pattern:
#
#   def main():
#       print("Running!")
#
#   if __name__ == "__main__":
#       main()          # only executes when run directly, not on import
#
# Why it matters:
#   Without this guard, any top-level code in a module runs on import.
#   That's fine for definitions, but side effects (print, file writes,
#   network calls) should be gated behind this check.
#
# pytest runs your test files by *importing* them, so __name__ inside a
# test file is the module name, never "__main__". That's why test files
# don't need this guard — pytest controls execution.


def demo_name_when_imported():
    # When imported (as pytest does), __name__ is the full module path
    return __name__  # "python.phase7.lessons"


def test_name_when_imported():
    # pytest imports this file, so __name__ is the dotted module name
    assert demo_name_when_imported() == "python.phase7.lessons"


def demo_main_guard_pattern():
    # Simulates what `if __name__ == "__main__"` protects.
    # Returns True only if we're the entry point, False if imported.
    print(f"__name__ is {__name__}")
    return __name__ == "__main__"


def test_main_guard_is_false_when_imported():
    # When imported (not run directly), the guard is False
    assert demo_main_guard_pattern() is False


# -----------------------------------------------------------------------------
# 6. THE STANDARD LIBRARY TOUR
# -----------------------------------------------------------------------------
# Python ships with a large standard library — "batteries included".
# No npm install needed for most common tasks.
#
# Key modules you'll reach for often (JS equivalent in parens):
#
#   os          — file paths, env vars, process info  (node:os, node:path partially)
#   sys         — interpreter info, sys.path, exit()  (node:process)
#   pathlib     — modern OO path handling             (node:path)
#   json        — JSON encode/decode                  (JSON.parse / JSON.stringify)
#   re          — regular expressions                 (RegExp)
#   datetime    — dates and times                     (Date, date-fns)
#   collections — Counter, defaultdict, deque         (no direct JS equiv)
#   itertools   — combinatorics, chaining iterables   (no direct JS equiv)
#   functools   — reduce, lru_cache, partial          (lodash partially)
#   typing      — type hints                          (TypeScript types)
#   dataclasses — structured data classes             (TS interfaces/classes)
#   abc         — abstract base classes               (TS abstract classes)
#   io          — in-memory streams                   (Buffer/Stream)
#   contextlib  — context manager utilities           (no direct JS equiv)
#   threading   — threads                             (Worker threads)
#   subprocess  — run shell commands                  (child_process)
#   unittest    — built-in test framework             (Jest — we use pytest instead)
#
# A few demos of the most useful ones:

import json  # noqa: E402
from pathlib import Path  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from datetime import date  # noqa: E402


def demo_pathlib():
    # pathlib.Path is the modern way to handle paths — OO, cross-platform.
    # JS: path.join(__dirname, 'sub', 'file.txt')
    p = Path("/some/dir") / "sub" / "file.txt"  # / operator joins path segments
    return str(p), p.suffix, p.stem, p.parent.name


def test_pathlib():
    path_str, suffix, stem, parent = demo_pathlib()
    assert path_str == "/some/dir/sub/file.txt"
    assert suffix == ".txt"
    assert stem == "file"
    assert parent == "sub"


def demo_json():
    # json.dumps / json.loads — same as JSON.stringify / JSON.parse
    data = {"name": "ada", "scores": [10, 20, 30]}
    serialized = json.dumps(data)
    restored = json.loads(serialized)
    return restored["name"], restored["scores"][1]


def test_json():
    name, score = demo_json()
    assert name == "ada"
    assert score == 20


def demo_counter():
    # Counter counts hashable items — like a frequency map
    # JS: arr.reduce((acc, x) => ({ ...acc, [x]: (acc[x] ?? 0) + 1 }), {})
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    freq = Counter(words)
    return freq["apple"], freq.most_common(1)[0]


def test_counter():
    apple_count, most_common = demo_counter()
    assert apple_count == 3
    assert most_common == ("apple", 3)


def demo_defaultdict():
    # defaultdict avoids KeyError by supplying a default factory.
    # JS: map[key] ??= []  (logical nullish assignment)
    groups = defaultdict(list)
    for name, dept in [("alice", "eng"), ("bob", "eng"), ("carol", "hr")]:
        groups[dept].append(name)
    return dict(groups)


def test_defaultdict():
    groups = demo_defaultdict()
    assert groups["eng"] == ["alice", "bob"]
    assert groups["hr"] == ["carol"]


def demo_date():
    d = date(2026, 2, 24)
    return d.year, d.month, d.strftime("%A")  # strftime for formatting


def test_date():
    year, month, weekday = demo_date()
    assert year == 2026
    assert month == 2
    assert weekday == "Tuesday"


# -----------------------------------------------------------------------------
# 7. THIRD-PARTY PACKAGES & pip
# -----------------------------------------------------------------------------
# When the stdlib isn't enough, you install third-party packages via pip.
# pip is Python's package manager — roughly equivalent to npm.
#
# Basic commands:
#   pip install requests          # install a package  (npm install)
#   pip install requests==2.31.0  # specific version   (npm install pkg@x.y.z)
#   pip uninstall requests        # remove a package   (npm uninstall)
#   pip list                      # show installed     (npm list)
#   pip show requests             # package metadata   (npm info)
#   pip freeze                    # pinned versions    (package-lock.json contents)
#   pip freeze > requirements.txt # save dependencies  (package.json / lockfile)
#   pip install -r requirements.txt  # install from file  (npm install)
#
# JS comparison:
#   npm install   → pip install
#   package.json  → pyproject.toml (modern) or requirements.txt (simple)
#   node_modules/ → site-packages/ (but shared system-wide — see concept 8!)
#
# Where packages live after install:
#   pip installs into site-packages, which is on sys.path.
#   Unlike node_modules (local per project), site-packages is typically
#   shared across your whole Python installation — which is why virtual
#   environments (concept 8) are essential.
#
# PyPI (Python Package Index) is the registry — like npmjs.com.
#   Browse at: https://pypi.org
#
# pip vs pip3:
#   On systems with both Python 2 and 3, `pip` might point to Python 2's pip.
#   Always use `pip3` or `python3 -m pip` to be safe.

import subprocess  # noqa: E402


def demo_pip_as_module():
    # `python3 -m pip` runs pip as a module — always uses the correct Python.
    # Here we just check `pip show pip` to confirm pip is available.
    result = subprocess.run(
        ["python3", "-m", "pip", "show", "pip"],
        capture_output=True,
        text=True,
    )
    return "Name: pip" in result.stdout


def test_pip_available():
    assert demo_pip_as_module() is True


def demo_requirements_format():
    # requirements.txt is the simplest way to record dependencies.
    # Each line is a package name with optional version constraint.
    lines = [
        "requests==2.31.0",  # exact version (==)
        "flask>=2.0,<3.0",  # range (>=, <)
        "numpy",  # any version (no constraint)
    ]
    # Parse package names — everything before the version specifier
    import re  # noqa: E402

    names = [re.split(r"[=<>!]", line)[0] for line in lines]
    return names


def test_requirements_format():
    assert demo_requirements_format() == ["requests", "flask", "numpy"]


# -----------------------------------------------------------------------------
# 8. VIRTUAL ENVIRONMENTS
# -----------------------------------------------------------------------------
# A virtual environment is an isolated Python installation for a single project.
# It gets its own site-packages, so dependencies don't bleed between projects.
#
# JS comparison:
#   node_modules/ is already local per project — you never have this problem.
#   virtual envs solve the equivalent of npm's local installs, but for Python where
#   the default behavior is global installs.
#
# Creating and using a virtual env:
#
#   python3 -m venv .venv          # create venv in .venv/ folder
#   source .venv/bin/activate      # activate (Mac/Linux)
#   .venv\Scripts\activate         # activate (Windows)
#   pip install requests           # installs into .venv, not globally
#   deactivate                     # leave the virtual env
#
# When activated, the shell prepends .venv/bin to PATH, so `python` and `pip`
# point to the venv's copies, not the system ones.
#
# Typical project layout:
#
#   myproject/
#     .venv/              ← venv (gitignored, like node_modules/)
#     src/
#     requirements.txt    ← committed (like package.json)
#     .gitignore          ← should include .venv/
#
# Modern alternatives to bare venv:
#   - poetry   — dependency management + packaging (like npm workspaces)
#   - uv       — very fast pip/venv replacement (Rust-based, gaining popularity)
#   - pipenv   — older alternative, less common now
#
# How to tell if a venv is active:
#   - $VIRTUAL_ENV env var is set
#   - `which python` points inside the .venv/ directory
#   - Your shell prompt usually shows (.venv) prefix

import os  # noqa: E402


def demo_venv_detection():
    # VIRTUAL_ENV is set by `source .venv/bin/activate`
    # Returns the path if active, None if not.
    return os.environ.get("VIRTUAL_ENV")


def test_venv_detection():
    # In this repo we don't use a venv, so VIRTUAL_ENV should be unset.
    # This test documents the behaviour — change if you add a venv later.
    assert demo_venv_detection() is None


def demo_python_executable():
    # sys.executable shows which python binary is running right now.
    # Inside a venv it points into .venv/bin/python.
    return sys.executable


def test_python_executable():
    # Whatever Python is running, it should be an absolute path to a binary.
    exe = demo_python_executable()
    assert "python" in exe.lower()


# -----------------------------------------------------------------------------
# 9. pyproject.toml / setup.py BASICS
# -----------------------------------------------------------------------------
# When you want to *distribute* a package (publish to PyPI, or install it
# locally as a proper package), you need a project metadata file.
#
# Evolution of Python packaging:
#   setup.py        — old way (imperative, runs arbitrary code — fragile)
#   setup.cfg       — declarative version of setup.py (better, but deprecated)
#   pyproject.toml  — modern standard (PEP 517/518, adopted ~2021)
#
# JS comparison:
#   pyproject.toml ≈ package.json
#   It declares the package name, version, dependencies, build system, etc.
#
# Minimal pyproject.toml:
#
#   [build-system]
#   requires = ["setuptools"]
#   build-backend = "setuptools.backends.legacy:build"
#
#   [project]
#   name = "mypackage"
#   version = "0.1.0"
#   description = "A short description"
#   requires-python = ">=3.9"
#   dependencies = [
#       "requests>=2.0",
#   ]
#
#   [project.optional-dependencies]
#   dev = ["pytest", "black"]
#
# Key fields (package.json parallel):
#   name            → "name"
#   version         → "version"
#   dependencies    → "dependencies"
#   optional-deps   → "devDependencies"
#   requires-python → "engines.node"
#
# Build backends (what actually builds the .whl / .tar.gz):
#   setuptools  — most common, what pip uses under the hood
#   hatchling   — modern, used by many new projects
#   flit        — simple, good for pure-Python packages
#   poetry      — manages its own format inside pyproject.toml
#
# Install a local package in "editable" mode (like `npm link`):
#   pip install -e .
#   This installs your package from the local directory so changes are
#   reflected immediately without reinstalling.

# tomllib is stdlib in Python 3.11+; this repo runs 3.9 so we parse manually.
# In a real project on 3.9 you'd: pip install tomli  then  import tomli as tomllib

# A sample pyproject.toml represented as a dict (what tomllib.loads() would return)
SAMPLE_PYPROJECT = {
    "project": {
        "name": "mypackage",
        "version": "0.2.0",
        "requires-python": ">=3.9",
        "dependencies": ["requests>=2.0"],
        "optional-dependencies": {
            "dev": ["pytest", "black"],
        },
    }
}


def demo_parse_pyproject():
    # Normally: data = tomllib.loads(Path("pyproject.toml").read_text())
    project = SAMPLE_PYPROJECT["project"]
    return project["name"], project["version"], project["dependencies"]


def test_parse_pyproject():
    name, version, deps = demo_parse_pyproject()
    assert name == "mypackage"
    assert version == "0.2.0"
    assert deps == ["requests>=2.0"]


def demo_optional_deps():
    return SAMPLE_PYPROJECT["project"]["optional-dependencies"]["dev"]


def test_optional_deps():
    dev_deps = demo_optional_deps()
    assert "pytest" in dev_deps
    assert "black" in dev_deps
