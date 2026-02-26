# ============================================================================
# conftest.py — shared fixtures for phase8
# ============================================================================
# pytest discovers this file automatically. No import needed in test files.
# Any fixture defined here is available to every test in this directory
# and all subdirectories.
#
# This is the primary use of conftest.py: DRY fixtures shared across
# multiple test files. Without conftest.py, you'd copy fixtures into every
# file that needs them.

import pytest


@pytest.fixture
def base_user():
    """A minimal user dict — shared across lessons.py and problems.py."""
    return {"id": 1, "name": "ada", "active": True}


@pytest.fixture
def admin_user():
    """An admin variant — also available everywhere in phase8."""
    return {"id": 2, "name": "root", "active": True, "role": "admin"}


@pytest.fixture(scope="module")
def shared_counter():
    """Module-scoped: one instance per file that uses it."""
    return {"value": 0}
