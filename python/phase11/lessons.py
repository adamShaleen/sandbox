# ============================================================================
# PHASE 11: Async Python & HTTP - LESSONS
# ============================================================================
# Python's async model is very similar to JS/TS — but with one key difference
# that trips everyone up coming from JS.
#
# Concepts covered:
#   1. async/await basics — coroutines vs JS Promises
#   2. asyncio.gather() — like Promise.all()
#   3. asyncio.create_task() — concurrent tasks
#   4. httpx.AsyncClient — async HTTP (like fetch/axios)
#   5. async context managers — `async with`
#   6. error handling in async code
#   7. asyncio.wait_for() — timeouts

import asyncio
from contextlib import asynccontextmanager
import pytest


# -----------------------------------------------------------------------------
# 1. async/await BASICS
# -----------------------------------------------------------------------------
# In JS, calling an async function starts it immediately and returns a Promise.
# In Python, calling an async function returns a *coroutine object* — it does
# NOT run yet. You must await it (or pass it to asyncio.run()).
#
# JS:
#   async function greet(name) { return `Hello, ${name}` }
#   const result = await greet("adam")  // starts running immediately
#
# Python:
#   async def greet(name):
#       return f"Hello, {name}"
#   result = await greet("adam")  # must be inside an async context
#
# JS Promises are *eager* — they start when created.
# Python coroutines are *lazy* — they start only when awaited.
#
# asyncio.run(coro) is the entry point from synchronous code.
# It creates an event loop, runs the coroutine to completion, then closes it.
# pytest-asyncio handles this automatically for async test_ functions.


async def demo_basic_coroutine():
    async def greet(name: str) -> str:
        return f"Hello, {name}"

    result = await greet("adam")
    return result


async def test_basic_coroutine():
    result = await demo_basic_coroutine()
    assert result == "Hello, adam"


def demo_asyncio_run():
    async def compute() -> int:
        return 42

    # calling from sync context — asyncio.run() starts the event loop
    return asyncio.run(compute())


def test_asyncio_run():
    assert demo_asyncio_run() == 42


# -----------------------------------------------------------------------------
# 2. asyncio.gather() — LIKE Promise.all()
# -----------------------------------------------------------------------------
# Run multiple coroutines *concurrently* and wait for all to finish.
# Results are returned in the same order as the input coroutines.
#
# JS:
#   const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()])
#
# Python:
#   a, b, c = await asyncio.gather(fetch_a(), fetch_b(), fetch_c())
#
# Key: all coroutines run on the *same thread* (cooperative multitasking).
# While one is awaiting I/O, others can run. This is NOT multi-threading.
#
# Without gather — sequential (slow):
#   r1 = await slow_task()  # waits 1s
#   r2 = await slow_task()  # waits another 1s — 2s total
#
# With gather — concurrent (fast):
#   r1, r2 = await asyncio.gather(slow_task(), slow_task())  # ~1s total


async def demo_gather():
    async def slow_double(x: int) -> int:
        await asyncio.sleep(0)  # simulate I/O (0s to keep tests fast)
        return x * 2

    results = await asyncio.gather(
        slow_double(1),
        slow_double(2),
        slow_double(3),
    )
    return list(results)


async def test_gather():
    results = await demo_gather()
    assert results == [2, 4, 6]


# -----------------------------------------------------------------------------
# 3. asyncio.create_task() — CONCURRENT TASKS
# -----------------------------------------------------------------------------
# create_task() schedules a coroutine to start running *immediately*,
# returning a Task object you can await later.
#
# This is the closest Python equivalent to constructing a Promise in JS:
#
# JS:
#   const p = fetchData()   // starts immediately, returns a Promise
#   doOtherWork()
#   const result = await p  // wait for it here
#
# Python:
#   task = asyncio.create_task(fetch_data())  # starts immediately
#   do_other_work()
#   result = await task
#
# vs gather(): gather() is simpler when you just want N results.
# create_task() gives you more control — you can cancel tasks, check if
# they're done, or await them selectively.
#
# Important: create_task() only works *inside* a running event loop
# (i.e., inside an async function). You can't call it from sync code.


async def demo_create_task():
    results = []

    async def worker(n: int):
        await asyncio.sleep(0)
        results.append(n)

    task1 = asyncio.create_task(worker(1))
    task2 = asyncio.create_task(worker(2))

    await task1
    await task2

    return results


async def test_create_task():
    results = await demo_create_task()
    assert sorted(results) == [1, 2]


# -----------------------------------------------------------------------------
# 4. httpx.AsyncClient — ASYNC HTTP
# -----------------------------------------------------------------------------
# httpx is the standard async HTTP client in Python (like fetch/axios in JS).
# Always use it as a context manager so the connection pool closes properly.
#
# JS:
#   const res = await fetch("https://example.com/data")
#   const data = await res.json()
#
# Python:
#   async with httpx.AsyncClient() as client:
#       res = await client.get("https://example.com/data")
#       data = res.json()  # no second await — already decoded
#
# Key response attributes:
#   res.status_code  → int (e.g. 200)
#   res.json()       → dict (parsed JSON)
#   res.text         → str (raw body)
#
# For testing without real network calls, httpx supports a MockTransport:
#
#   def handler(request):
#       return httpx.Response(200, json={"ok": True})
#
#   async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
#       res = await client.get("https://example.com")


import httpx  # noqa: E402


async def demo_httpx():
    def handler(request):
        return httpx.Response(200, json={"url": str(request.url)})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        res = await client.get("https://example.com/hello")
        return res.status_code, res.json()


async def test_httpx():
    status, body = await demo_httpx()
    assert status == 200
    assert body == {"url": "https://example.com/hello"}


# -----------------------------------------------------------------------------
# 5. ASYNC CONTEXT MANAGERS — `async with`
# -----------------------------------------------------------------------------
# Some resources need async setup/teardown (e.g. opening a DB connection,
# acquiring a lock). `async with` handles this — like regular `with` but the
# enter/exit steps are themselves awaitable.
#
# JS doesn't have a direct equivalent. Closest pattern:
#   const resource = await openResource()
#   try { ... } finally { await resource.close() }
#
# Python:
#   async with open_resource() as resource:
#       ...  # cleanup happens automatically, even on exception
#
# You already used this with httpx.AsyncClient — that's an async context manager.
#
# You can build your own with @asynccontextmanager (mirrors @contextmanager
# from phase 6 — same idea, just async):
#
#   from contextlib import asynccontextmanager
#
#   @asynccontextmanager
#   async def managed(name):
#       print(f"open {name}")
#       try:
#           yield name          # <-- value bound to `as` variable
#       finally:
#           print(f"close {name}")  # runs even if an exception occurs


async def demo_async_context_manager():
    log = []

    @asynccontextmanager
    async def managed(name: str):
        log.append(f"open:{name}")
        try:
            yield name
        finally:
            log.append(f"close:{name}")

    async with managed("db") as r:
        log.append(f"use:{r}")

    return log


async def test_async_context_manager():
    log = await demo_async_context_manager()
    assert log == ["open:db", "use:db", "close:db"]


# -----------------------------------------------------------------------------
# 6. ERROR HANDLING IN ASYNC CODE
# -----------------------------------------------------------------------------
# try/except works identically inside async functions — no surprises there.
#
# The interesting case is gather() with multiple coroutines where one fails.
#
# DEFAULT behavior — raises immediately on first exception, others are cancelled:
#   results = await asyncio.gather(good(), bad(), good())  # raises BadError
#
# This is like Promise.all() in JS — one rejection rejects the whole thing.
#
# return_exceptions=True — collects exceptions as values instead of raising:
#   results = await asyncio.gather(good(), bad(), good(), return_exceptions=True)
#   # results → [value, BadError(...), value]
#
# This is like Promise.allSettled() in JS — all run to completion regardless.
# You check each result with isinstance(r, Exception) to detect failures.


async def demo_gather_errors():
    async def risky(n: int):
        if n == 2:
            raise ValueError("boom")
        return n * 10

    # With return_exceptions=True — all coroutines run, errors become values
    results = await asyncio.gather(
        risky(1),
        risky(2),
        risky(3),
        return_exceptions=True,
    )
    return results


async def test_gather_errors():
    results = await demo_gather_errors()
    assert results[0] == 10
    assert isinstance(results[1], ValueError)
    assert results[2] == 30

    # Without return_exceptions — raises on first failure
    async def bad():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        await asyncio.gather(bad(), bad())


# -----------------------------------------------------------------------------
# 7. asyncio.wait_for() — TIMEOUTS
# -----------------------------------------------------------------------------
# Wraps a coroutine with a deadline. If the coroutine doesn't finish in time,
# it is cancelled and asyncio.TimeoutError is raised.
#
# JS:
#   await Promise.race([fetchData(), timeout(5000)])
#
# Python:
#   await asyncio.wait_for(fetch_data(), timeout=5.0)  # seconds as a float
#
# If the timeout fires, the coroutine is cancelled automatically — you don't
# need to clean it up manually.
#
# Catch asyncio.TimeoutError to handle the timeout gracefully:
#
#   try:
#       result = await asyncio.wait_for(slow_task(), timeout=1.0)
#   except asyncio.TimeoutError:
#       result = "timed out"


async def demo_wait_for():
    async def fast() -> str:
        await asyncio.sleep(0)
        return "done"

    async def slow() -> str:
        await asyncio.sleep(10)
        return "done"

    # completes in time — returns normally
    result = await asyncio.wait_for(fast(), timeout=1.0)
    assert result == "done"

    # exceeds timeout — raises TimeoutError
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow(), timeout=0.01)


async def test_wait_for():
    await demo_wait_for()
