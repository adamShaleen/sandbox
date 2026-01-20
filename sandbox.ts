//----------------------------------------------------------------------------------------------
// Codewars - "LRU Cache with TTL Memoization" (Least Recently Used)

/**
  Description
  Your task is to create a memoization function that wraps around a given function and enhances it with caching capabilities. The cache should have a configurable maximum size, and each cached result should expire after a specified TTL. This ensures that the cache does not grow indefinitely and that stale data is eventually removed. Additionally, when the cache exceeds its maximum size, the least recently used (LRU) entry should be evicted to make space for new entries.

  Behavior
  The memoized function should return cached results for previously computed inputs, improving performance for repetitive calls.
  The cache should automatically evict the least recently used (LRU) entry when the maximum cache size is exceeded (if maxSize is specified).
  Cached entries should expire after the specified TTL (if ttl is specified).
  If both maxSize and ttl are specified, the memoized function should handle both constraints.

  Edge Cases
  Ensure the function works with various types of input parameters (e.g., numbers, strings, objects).
  Handle the scenario where maxSize is 0 or negative by treating it as unlimited.
  Handle the scenario where ttl is 0 or negative by treating it as no expiration.

  Memoization
  Memoization is an optimization technique that caches function results so repeated calls with the same arguments return the cached value instead of recomputing.

  How it works

  Without memoization - computes every time
  fibonacci(40); takes ~1 second
  fibonacci(40); takes ~1 second again

  With memoization - computes once, then cache hits
  memoizedFib(40); takes ~1 second
  memoizedFib(40); instant (cached)
 */

export type MemoizeOptions = {
  maxSize?: number;
  ttl?: number;
};

export type AnyFunction = (...args: any[]) => any;

export type MemoizedFunction<T extends AnyFunction> = (...args: Parameters<T>) => ReturnType<T>;

export const memoize = <T extends AnyFunction>(
  fn: T,
  { maxSize, ttl }: MemoizeOptions = {}
): MemoizedFunction<T> => {
  // Map maintains insertion order, which we use for LRU tracking
  // The first key is always the least recently used
  const cache = new Map();

  return (...args) => {
    const key = JSON.stringify(args);

    // Cache hit - check if entry exists
    if (cache.has(key)) {
      const entry = cache.get(key);

      // TTL check - if expired, recompute and cache fresh value
      if (ttl && ttl > 0) {
        const isExpired = Date.now() - entry.insertionTimestamp > ttl;

        if (isExpired) {
          const result = fn(...args);
          cache.set(key, { value: result, insertionTimestamp: Date.now() });
          return result;
        }
      }

      // LRU update - move entry to end of Map by deleting and re-inserting
      // This ensures the first key is always the least recently used
      cache.delete(key);
      cache.set(key, entry);

      return entry.value;
    }

    // Cache miss - evict LRU entry if at capacity
    if (maxSize && maxSize > 0 && cache.size === maxSize) {
      const leastRecentlyUsed = cache.keys().next().value;
      cache.delete(leastRecentlyUsed);
    }

    // Compute result and cache with timestamp
    const result = fn(...args);
    cache.set(key, { value: result, insertionTimestamp: Date.now() });

    return result;
  };
};

describe('memoize', () => {
  const add = (a: number, b: number): number => a + b;
  const concat = (a: string, b: string) => a + b;
  const merge = (a: object, b: object) => ({ ...a, ...b });
  const randomFunc = (a: number) => Math.random() * a;

  it('should cache results and return cached values', () => {
    const memoizedAdd = memoize(add);

    expect(memoizedAdd(1, 2)).toBe(3); // calculated
    expect(memoizedAdd(1, 2)).toBe(3); // cached
  });

  it('should respect maxSize', () => {
    let callCount = 0;

    const add = (a: number, b: number): number => {
      callCount++;
      return a + b;
    };

    const memoizedAdd = memoize(add, { maxSize: 2 });

    // cache: empty → [1,2]
    memoizedAdd(1, 2); // callCount = 1, computed

    // cache: [1,2] → [1,2], [2,3]
    memoizedAdd(2, 3); // callCount = 2, computed

    // cache: [1,2], [2,3] → [2,3], [3,4] (evicts [1,2], LRU)
    memoizedAdd(3, 4); // callCount = 3, computed

    // cache: [2,3], [3,4] → [3,4], [1,2] (evicts [2,3], LRU)
    memoizedAdd(1, 2); // callCount = 4, recomputed since evicted

    // cache: [3,4], [1,2] → [1,2], [2,3] (evicts [3,4], LRU)
    memoizedAdd(2, 3); // callCount = 5, recomputed since evicted in previous step

    expect(callCount).toBe(5);
  });

  it('should respect ttl', (done) => {
    let callCount = 0;

    const add = (a: number, b: number) => {
      callCount++;
      return a + b;
    };

    const memoizedAdd = memoize(add, { ttl: 50 });

    memoizedAdd(1, 2); // callCount = 1, computed
    memoizedAdd(1, 2); // callCount = 1, cached

    setTimeout(() => {
      memoizedAdd(1, 2); // callCount = 2, recomputed after TTL expired
      expect(callCount).toBe(2);
      done();
    }, 60);
  });

  it('should handle various input types', () => {
    const memoizedConcat = memoize(concat);

    expect(memoizedConcat('Hello, ', 'World!')).toBe('Hello, World!'); // calculated
    expect(memoizedConcat('Hello, ', 'World!')).toBe('Hello, World!'); // cached
  });

  it('should handle objects as input parameters', () => {
    const memoizedMerge = memoize(merge);

    const obj1 = { foo: 'bar' };
    const obj2 = { baz: 'qux' };

    const result = memoizedMerge(obj1, obj2);
    expect(result).toEqual({ foo: 'bar', baz: 'qux' }); // calculated
    expect(memoizedMerge(obj1, obj2)).toEqual(result); // cached
  });

  it('should treat maxSize 0 or negative as unlimited', () => {
    const memoizedAdd = memoize(add, { maxSize: 0 });
    memoizedAdd(1, 2);
    memoizedAdd(2, 3);
    memoizedAdd(3, 4);

    expect(memoizedAdd(1, 2)).toBe(3); // cached
    expect(memoizedAdd(2, 3)).toBe(5); // cached
    expect(memoizedAdd(3, 4)).toBe(7); // cached
  });

  it('should treat ttl 0 or negative as no expiration', (done) => {
    const memoizedAdd = memoize(add, { ttl: 0 });
    memoizedAdd(1, 2);
    expect(memoizedAdd(1, 2)).toBe(3); // cached
    setTimeout(() => {
      expect(memoizedAdd(1, 2)).toBe(3); // still cached after supposed expiration
      done();
    }, 100);
  });

  it('should handle random data', () => {
    const memoizedRandomFunc = memoize(randomFunc, { maxSize: 5, ttl: 1000 });

    const inputs = [10, 20, 30, 40, 50];
    const results: { [key: number]: number } = {};

    inputs.forEach((input) => {
      results[input] = memoizedRandomFunc(input);
    });

    inputs.forEach((input) => {
      expect(memoizedRandomFunc(input)).toBe(results[input]); // cached
    });
  });
});
