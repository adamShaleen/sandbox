# ============================================================================
# PHASE 11: Async Python & HTTP - PROBLEMS
# ============================================================================

from __future__ import annotations

import asyncio


# ----------------------------------------------------------------------------
# Problem 1 — Your first coroutine
# ----------------------------------------------------------------------------
# `delayed_double(n, delay)` is an async function that waits `delay` seconds,
# then returns `n * 2`.
#
# Then write `run_doubled(n, delay)` — a *synchronous* function that calls
# `delayed_double` and returns its result. Use asyncio.run().
#
# JS/TS hint:
#   async function delayedDouble(n, delay) {
#     await new Promise(r => setTimeout(r, delay * 1000))
#     return n * 2
#   }
#
# Python hint: `await asyncio.sleep(seconds)` is the equivalent of
# `await new Promise(r => setTimeout(r, ms))`


async def delayed_double(n: int, delay: float) -> int:
    await asyncio.sleep(delay)
    return n * 2


def run_doubled(n: int, delay: float) -> int:
    return asyncio.run(delayed_double(n, delay))


async def test_delayed_double():
    result = await delayed_double(5, 0)
    assert result == 10
    result = await delayed_double(3, 0)
    assert result == 6


def test_run_doubled():
    assert run_doubled(4, 0) == 8
    assert run_doubled(0, 0) == 0


# ----------------------------------------------------------------------------
# Problem 2 — Concurrent fetch simulation
# ----------------------------------------------------------------------------
# `fetch_all(urls)` takes a list of URL strings and returns a list of strings
# in the format "fetched: <url>", one per URL, in the same order as input.
#
# Simulate the "fetch" with a coroutine `fake_fetch(url)` that sleeps 0s
# and returns "fetched: <url>".
#
# Use asyncio.gather() so all fetches run concurrently.
#
# JS/TS hint:
#   async function fetchAll(urls) {
#     return Promise.all(urls.map(url => fakeFetch(url)))
#   }


async def fake_fetch(url: str) -> str:
    await asyncio.sleep(0)
    return f"fetched: {url}"


async def fetch_all(urls: list[str]) -> list[str]:
    return await asyncio.gather(*(fake_fetch(url) for url in urls))


async def test_fetch_all():
    urls = ["https://a.com", "https://b.com", "https://c.com"]
    results = await fetch_all(urls)
    assert results == [
        "fetched: https://a.com",
        "fetched: https://b.com",
        "fetched: https://c.com",
    ]
    assert await fetch_all([]) == []


# ----------------------------------------------------------------------------
# Problem 3 — Race to first result
# ----------------------------------------------------------------------------
# `first_result(coros)` takes a list of coroutines and returns the result of
# whichever one finishes first. Cancel the rest.
#
# Use asyncio.create_task() to schedule all coroutines, then
# asyncio.wait() with return_when=asyncio.FIRST_COMPLETED to get the winner.
#
# asyncio.wait() returns two sets: (done, pending)
# Cancel everything in `pending` after the first completes.
# To get the result from a done task, call .result() on it.
#
# JS/TS hint:
#   Promise.race([p1, p2, p3])


async def first_result(coros):
    tasks = [asyncio.create_task(task) for task in coros]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    [p.cancel() for p in pending]
    return next(iter(done)).result()


async def test_first_result():
    async def slow(val, delay):
        await asyncio.sleep(delay)
        return val

    result = await first_result([slow("a", 0.05), slow("b", 0), slow("c", 0.1)])
    assert result == "b"  # b finishes first (0s delay)


# ----------------------------------------------------------------------------
# Problem 4 — Async HTTP client
# ----------------------------------------------------------------------------
# `get_status(url, client)` takes a URL string and an httpx.AsyncClient,
# and returns the response status code as an int.
#
# `get_all_statuses(urls)` takes a list of URLs, creates an AsyncClient,
# and returns a list of status codes (one per URL) fetched concurrently.
# Use gather() so all requests fire at once.
#
# Use MockTransport in the test — no real network calls needed.
# The handler always returns status 200.
#
# JS/TS hint:
#   async function getStatus(url, client) { ... }
#   async function getAllStatuses(urls) {
#     return Promise.all(urls.map(url => getStatus(url, client)))
#   }

import httpx  # noqa: E402


async def get_status(url: str, client: httpx.AsyncClient) -> int:
    response = await client.get(url)
    return response.status_code


async def get_all_statuses(urls: list[str]) -> list[int]:
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*[get_status(url, client) for url in urls])


async def test_get_all_statuses():
    def handler(_):
        return httpx.Response(200)

    transport = httpx.MockTransport(handler)
    urls = ["https://a.com", "https://b.com", "https://c.com"]

    async with httpx.AsyncClient(transport=transport) as client:
        statuses = await asyncio.gather(*(get_status(url, client) for url in urls))

    assert statuses == [200, 200, 200]


# ----------------------------------------------------------------------------
# Problem 5 — Build an async context manager
# ----------------------------------------------------------------------------
# `timer()` is an async context manager (built with @asynccontextmanager)
# that measures how long the `async with` block takes to run.
#
# It should record the start time, yield (nothing — caller doesn't need it),
# and after the block finishes, append the elapsed time to a log list
# passed in as an argument.
#
# Signature:
#   timer(log: list) — async context manager, yields nothing (yield None)
#
# Usage:
#   log = []
#   async with timer(log):
#       await asyncio.sleep(0)
#   assert log[0] >= 0  # elapsed time in seconds
#
# JS/TS hint:
#   async function withTimer(fn) {
#     const start = performance.now()
#     await fn()
#     return performance.now() - start
#   }
#
# Hint: asyncio.get_running_loop().time() returns a float (seconds)
# Use get_running_loop() — get_event_loop() is deprecated inside async code

from contextlib import asynccontextmanager  # noqa: E402


@asynccontextmanager
async def timer(log: list):
    start_time = asyncio.get_running_loop().time()

    try:
        yield None
    finally:
        elapsed_time = asyncio.get_running_loop().time() - start_time
        log.append(elapsed_time)


async def test_timer():
    log = []
    async with timer(log):
        await asyncio.sleep(0)

    assert len(log) == 1
    assert log[0] >= 0  # elapsed seconds


# ----------------------------------------------------------------------------
# Problem 6 — Partition results
# ----------------------------------------------------------------------------
# `partition_results(coros)` runs all coroutines concurrently using
# gather(return_exceptions=True) and returns a tuple (successes, errors):
#   - successes: list of values from coroutines that completed normally
#   - errors: list of Exception instances from coroutines that raised
#
# Order within each list should match the original input order.
#
# Use isinstance(r, Exception) to tell values from errors apart.
#
# JS/TS hint:
#   const settled = await Promise.allSettled(coros)
#   const successes = settled.filter(r => r.status === "fulfilled").map(r => r.value)
#   const errors = settled.filter(r => r.status === "rejected").map(r => r.reason)


async def partition_results(coros):
    results = await asyncio.gather(*coros, return_exceptions=True)
    successes, errors = [], []

    for result in results:
        if not isinstance(result, Exception):
            successes.append(result)
        else:
            errors.append(result)

    return (successes, errors)


async def test_partition_results():
    async def ok(val):
        return val

    async def fail(msg):
        raise ValueError(msg)

    successes, errors = await partition_results(
        [ok(1), fail("bad"), ok(2), fail("worse"), ok(3)]
    )

    assert successes == [1, 2, 3]
    assert len(errors) == 2
    assert all(isinstance(e, ValueError) for e in errors)
    assert str(errors[0]) == "bad"
    assert str(errors[1]) == "worse"


# ----------------------------------------------------------------------------
# Problem 7 — Timeout with fallback
# ----------------------------------------------------------------------------
# `with_timeout(coro, timeout, default)` runs a coroutine with a deadline.
# If it completes in time, return its result.
# If it exceeds the timeout, return `default` instead of raising.
#
# Use asyncio.wait_for() and catch asyncio.TimeoutError.
#
# JS/TS hint:
#   async function withTimeout(promise, ms, fallback) {
#     try {
#       return await Promise.race([promise, rejectAfter(ms)])
#     } catch { return fallback }
#   }


async def with_timeout(coro, timeout: float, default):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return default


async def test_with_timeout():
    async def fast():
        await asyncio.sleep(0)
        return "done"

    async def slow():
        await asyncio.sleep(10)
        return "done"

    assert await with_timeout(fast(), 1.0, "timed out") == "done"
    assert await with_timeout(slow(), 0.01, "timed out") == "timed out"
