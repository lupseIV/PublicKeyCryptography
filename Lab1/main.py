import math
import multiprocessing
import queue
import random
import time

from gcd import gcd_euclid
from binary_gcd import binary_gcd
from factor_gcd import factor_gcd

# How many times each (algorithm, input) pair is executed.
# A single gcd call on small numbers takes well under a microsecond,
# which is below the clock's useful resolution, so we time many calls
# and divide by RUNS to get the average time of one call.
RUNS = 100

# Maximum time (in seconds) one single call may take. Slower calls are
# reported as "> 1 s" instead of being timed - e.g. factoring 300-digit
# numbers by trial division would take longer than the age of the universe.
TIME_LIMIT = 1


def fibonacci(n):
    """Return the n-th Fibonacci number (F(1) = F(2) = 1)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# The test inputs: (description, a, b).
# They grow from tiny to "really large" so the differences between
# the algorithms become visible.
TEST_CASES = [
    ("small numbers", 48, 18),
    ("10-digit numbers", 1_234_567_890, 9_876_543_210),
    ("consecutive Fibonacci (~21 digits)", fibonacci(100), fibonacci(99)),
    ("~60-digit numbers", 2**100 * 3**50, 2**80 * 3**70 * 7),
    ("~300-digit numbers", 3**600 + 1, 7**350 + 1),

    # --- special cases (edge cases and structured inputs) ---
    ("equal numbers", 123_456_789, 123_456_789),
    ("one divides the other", 1_000_000, 250),
    ("two primes (6 digits)", 999_983, 1_000_003),
    ("one of them is 1", 1, 987_654_321),
    ("one of them is 0", 0, 123_456),
    ("many factors of 2", 2**60, 2**40 * 3),
    ("9-digit prime and its multiple", 999_999_937, 3 * 999_999_937),
    # Bigger Fibonacci worst case for Euclid; its prime factors are too
    # large for trial division to find within the time limit.
    ("consecutive Fibonacci (~42 digits)", fibonacci(200), fibonacci(199)),
    # 2^61 - 1 and 2^31 - 1 are both (Mersenne) primes.
    ("Mersenne primes 2^61-1, 2^31-1", 2**61 - 1, 2**31 - 1),
    # Random 1000-digit numbers with a common factor; the fixed seed makes
    # every run use the same numbers, so results are reproducible.
    ("~1000-digit numbers",
     random.Random(2026).getrandbits(3322) * 12345,
     random.Random(2027).getrandbits(3322) * 12345),
]

ALGORITHMS = [
    ("Euclid (remainder)", gcd_euclid),
    ("Binary GCD (Stein)", binary_gcd),
    ("Factoring GCD", factor_gcd)
]


def _worker(func, a, b, results):
    """Runs inside the child process: compute func(a, b) and send it back."""
    try:
        results.put(("ok", func(a, b)))
    except Exception as e:
        results.put(("error", type(e).__name__))


def probe(func, a, b):
    """
    Run ONE call of func(a, b) in a separate process, so that it can be
    killed if it exceeds TIME_LIMIT (Python cannot stop a running function
    from the outside, but it can terminate a whole process).

    Returns ("ok", result), ("error", error_name) or ("timeout", None).
    This call is only used to detect timeouts and check the result - it is
    NOT used for the timing, because starting a process takes ~50-100 ms
    and would distort the measurement.
    """
    results = multiprocessing.Queue()
    child = multiprocessing.Process(target=_worker, args=(func, a, b, results))
    child.start()
    try:
        # Wait at most TIME_LIMIT seconds for the child's answer.
        outcome = results.get(timeout=TIME_LIMIT)
    except queue.Empty:
        child.terminate()           # too slow: kill the child process
        outcome = ("timeout", None)
    child.join()
    return outcome


def time_one(func, a, b):
    """
    Run func(a, b) RUNS times and return the average time of one call
    in nanoseconds, or the name of the error if the call fails.
    """
    try:
        start = time.perf_counter_ns()      # high-resolution clock, in ns
        for _ in range(RUNS):
            func(a, b)
        end = time.perf_counter_ns()
        return (end - start) / RUNS
    except RecursionError:
        return "RecursionError"


def format_time(ns):
    """Show a time in ns or µs so small and large values are both readable."""
    if isinstance(ns, str):
        return ns
    if ns < 1_000:
        return f"{ns:.0f} ns"
    return f"{ns / 1_000:.2f} µs"


def benchmark():
    """Time every algorithm on every test case and print a table."""
    header = f"{'Test case':<36}" + "".join(f"{name:>22}" for name, _ in ALGORITHMS)
    print(header)
    print("-" * len(header))

    for description, a, b in TEST_CASES:
        row = f"{description:<36}"
        for name, func in ALGORITHMS:
            # Step 1: one guarded call in a child process. This tells us
            # whether the algorithm finishes within TIME_LIMIT and whether
            # its answer matches Python's built-in gcd.
            status, value = probe(func, a, b)
            if status == "timeout":
                cell = f"> {TIME_LIMIT} s"
            elif status == "error":
                cell = value                    # e.g. "RecursionError"
            elif value != math.gcd(a, b):
                cell = "WRONG RESULT"           # never time a wrong answer
            else:
                # Step 2: it is fast and correct, so time it for real
                # in this process (no process start-up overhead).
                cell = format_time(time_one(func, a, b))
            row += f"{cell:>22}"
        print(row, flush=True)

    print(f"\nAverage time of one call, measured over {RUNS} runs.")
    print(f"'> {TIME_LIMIT} s' = a single call did not finish within {TIME_LIMIT} s.")


def interactive():
    """Your original manual test: read two numbers and print both results."""
    a = int(input("Enter the 1st number: "))
    b = int(input("Enter the 2nd number: "))
    print(gcd_euclid(a, b))
    print(binary_gcd(a, b))



if __name__ == "__main__":
    benchmark()
