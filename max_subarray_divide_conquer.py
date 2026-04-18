"""
max_subarray_divide_conquer.py
==============================
Design and Analysis of Algorithms – Question 3
Paradigm: Divide and Conquer

Maximum Subarray Problem (Kadane-style profit/loss interpretation):
  Given an array A[0..n-1] of integers (positive = profit, negative = loss),
  find the contiguous subarray with the largest sum.

Three approaches included:
  1. Divide and Conquer   → T(n) = 2T(n/2) + O(n) = O(n log n)  [D&C paradigm]
  2. Brute Force          → O(n²)
  3. Kadane's Algorithm   → O(n)  [optimal; included for comparison only]

The D&C approach is the primary submission demonstrating the required paradigm.
The Master Theorem analysis is documented in Task 4 of the report.

Team Members:
  Ashith Rao K   – PES1UG24CS559
  Girish G N     – PES1UG24CS571
  Ankith Sudala  – PES1UG24CS557
  Preetham V     – PES1UG24CS599
"""

import math    # For math.inf (−∞ initialisation)
import time    # For wall-clock benchmarking
import random  # For synthetic array generation


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — Find Maximum Crossing Subarray  [O(n)]
# ─────────────────────────────────────────────────────────────────────────────

def find_max_crossing(A: list[int], lo: int, mid: int, hi: int) -> tuple[int, int, int]:
    """
    Find the maximum subarray that crosses the midpoint.

    The crossing subarray MUST include A[mid] on the left and A[mid+1] on the
    right.  We extend greedily left from mid and right from mid+1, tracking
    the running maximum prefix/suffix sum at each step.

    Divide-and-Conquer role — COMBINE step:
      This is called once per recursive level to merge left and right results.

    Time Complexity: O(n) — two linear scans (left half + right half)
    Space Complexity: O(1) extra

    Parameters
    ----------
    A   : input array
    lo  : left boundary of the current subarray (inclusive)
    mid : midpoint index
    hi  : right boundary of the current subarray (inclusive)

    Returns
    -------
    (max_left, max_right, crossing_sum) where
      max_left  = leftmost index of best crossing subarray
      max_right = rightmost index of best crossing subarray
      crossing_sum = maximum sum of A[max_left..max_right]
    """
    # ── Extend LEFT from mid ──────────────────────────────────────────────
    left_sum = -math.inf
    total    = 0
    max_left = mid

    for i in range(mid, lo - 1, -1):   # Scan right-to-left from mid
        total += A[i]
        if total > left_sum:
            left_sum = total
            max_left = i               # Best left boundary so far

    # ── Extend RIGHT from mid+1 ───────────────────────────────────────────
    right_sum = -math.inf
    total     = 0
    max_right = mid + 1

    for j in range(mid + 1, hi + 1):  # Scan left-to-right from mid+1
        total += A[j]
        if total > right_sum:
            right_sum = total
            max_right = j             # Best right boundary so far

    return max_left, max_right, left_sum + right_sum


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 1 — Divide and Conquer  [O(n log n)]
# ─────────────────────────────────────────────────────────────────────────────

def find_max_subarray(A: list[int], lo: int, hi: int) -> tuple[int, int, int]:
    """
    Find the maximum subarray using the divide-and-conquer paradigm.

    Strategy (three-case analysis):
      DIVIDE : Split A[lo..hi] at mid = (lo+hi)//2
      CONQUER: Recursively find max subarray in A[lo..mid] and A[mid+1..hi]
      COMBINE: Find max crossing subarray via find_max_crossing()
      RETURN : Best of left_sum, right_sum, crossing_sum

    Recurrence: T(n) = 2T(n/2) + O(n),  T(1) = O(1)

    Master Theorem — Case 2 (a=2, b=2, f(n)=O(n)):
      n^(log_b a) = n^(log_2 2) = n^1 = n
      f(n) = O(n) = O(n^(log_b a))  → Case 2 applies
      ∴  T(n) = Θ(n log n)

    Time Complexity:  O(n log n)
    Space Complexity: O(log n) — recursion stack depth = height of binary tree

    Parameters
    ----------
    A  : input array of integers
    lo : left boundary (inclusive)
    hi : right boundary (inclusive)

    Returns
    -------
    (low_idx, high_idx, max_sum) — indices and sum of the maximum subarray
    """
    # Base case: single element — it IS the maximum subarray
    if lo == hi:
        return lo, hi, A[lo]

    mid = (lo + hi) // 2   # DIVIDE at midpoint

    # CONQUER — recurse on each half
    left_lo,  left_hi,  left_sum  = find_max_subarray(A, lo,      mid)
    right_lo, right_hi, right_sum = find_max_subarray(A, mid + 1, hi)

    # COMBINE — find maximum crossing subarray
    cross_lo, cross_hi, cross_sum = find_max_crossing(A, lo, mid, hi)

    # RETURN the best of three candidates
    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_lo, left_hi, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_lo, right_hi, right_sum
    else:
        return cross_lo, cross_hi, cross_sum


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 2 — Brute Force  [O(n²)]
# ─────────────────────────────────────────────────────────────────────────────

def max_subarray_brute(A: list[int]) -> tuple[int, int, int]:
    """
    Find the maximum subarray using brute-force enumeration of all pairs (i, j).

    For every starting index i, accumulate sum from i rightward;
    update the global maximum whenever a better sum is found.

    Time Complexity:  O(n²) — nested loops over all O(n²) subarrays
    Space Complexity: O(1) — only a handful of scalar variables

    Parameters
    ----------
    A : input array of integers

    Returns
    -------
    (best_lo, best_hi, max_sum)
    """
    n        = len(A)
    max_sum  = -math.inf
    best_lo  = 0
    best_hi  = 0

    for i in range(n):
        total = 0
        for j in range(i, n):
            total += A[j]
            if total > max_sum:
                max_sum = total
                best_lo = i
                best_hi = j

    return best_lo, best_hi, max_sum


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 3 — Kadane's Algorithm  [O(n)]  (for comparison only)
# ─────────────────────────────────────────────────────────────────────────────

def max_subarray_kadane(A: list[int]) -> tuple[int, int, int]:
    """
    Find the maximum subarray using Kadane's linear-time algorithm.

    NOT divide-and-conquer — included only for performance comparison.
    Kadane's maintains a running maximum ending at each position and resets
    when the running sum drops below the current element.

    Time Complexity:  O(n) — single left-to-right pass
    Space Complexity: O(1)

    Parameters
    ----------
    A : input array of integers

    Returns
    -------
    (best_lo, best_hi, max_sum)
    """
    max_sum   = A[0]
    cur_sum   = A[0]
    best_lo   = 0
    best_hi   = 0
    cur_start = 0

    for i in range(1, len(A)):
        if cur_sum + A[i] < A[i]:
            cur_sum   = A[i]
            cur_start = i
        else:
            cur_sum += A[i]

        if cur_sum > max_sum:
            max_sum = cur_sum
            best_lo = cur_start
            best_hi = i

    return best_lo, best_hi, max_sum


# ─────────────────────────────────────────────────────────────────────────────
# EXPERIMENTAL COMPARISON — varying array sizes
# ─────────────────────────────────────────────────────────────────────────────

def benchmark_all(n: int) -> None:
    """
    Generate a random profit/loss array of size n and time all three approaches.

    Arrays contain both positive and negative integers in range [-50, 100]
    to simulate realistic profit/loss scenarios.

    Parameters
    ----------
    n : array length
    """
    A = [random.randint(-50, 100) for _ in range(n)]

    # Divide and Conquer
    t0 = time.perf_counter()
    lo_dc, hi_dc, sum_dc = find_max_subarray(A, 0, n - 1)
    t_dc = time.perf_counter() - t0

    # Brute Force (skip for very large n — too slow)
    if n <= 10_000:
        t0 = time.perf_counter()
        lo_bf, hi_bf, sum_bf = max_subarray_brute(A)
        t_bf = time.perf_counter() - t0
        bf_str = f"{t_bf * 1000:>9.3f} ms"
    else:
        sum_bf = sum_dc   # Skip, assume correct
        bf_str = f"{'(skipped)':>12}"

    # Kadane
    t0 = time.perf_counter()
    lo_kd, hi_kd, sum_kd = max_subarray_kadane(A)
    t_kd = time.perf_counter() - t0

    # Verify all three agree
    assert sum_dc == sum_kd == sum_bf, (
        f"MISMATCH at n={n}: D&C={sum_dc}, Kadane={sum_kd}, BF={sum_bf}"
    )

    print(f"  n={n:<8} | D&C: {t_dc*1000:>8.3f} ms"
          f" | Brute: {bf_str}"
          f" | Kadane: {t_kd*1000:>8.4f} ms"
          f" | max_sum={sum_dc}")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT — trace + benchmarks
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("  MAXIMUM SUBARRAY — Divide and Conquer")
    print("  DAA Project | PES University")
    print("=" * 70)

    # ── Classic textbook example (CLRS) ──────────────────────────────────
    # Expected answer: subarray [18, 20, -7, 12] at indices [7..10], sum = 43
    A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    print(f"\n── Classic Trace ──")
    print(f"  Input : {A}")

    lo, hi, total = find_max_subarray(A, 0, len(A) - 1)
    print(f"  D&C   : A[{lo}..{hi}] = {A[lo:hi+1]}, Sum = {total}")

    lo_b, hi_b, total_b = max_subarray_brute(A)
    print(f"  Brute : A[{lo_b}..{hi_b}] = {A[lo_b:hi_b+1]}, Sum = {total_b}")

    lo_k, hi_k, total_k = max_subarray_kadane(A)
    print(f"  Kadane: A[{lo_k}..{hi_k}] = {A[lo_k:hi_k+1]}, Sum = {total_k}")

    assert total == total_b == total_k, "Results do not agree!"
    print("  ✔ All three approaches agree.")

    # ── Additional test cases ─────────────────────────────────────────────
    print("\n── Additional Test Cases ──")
    tests = [
        ([1, 2, 3, 4, 5],              "All positive  → entire array"),
        ([-5, -3, -1, -8],             "All negative  → single max element"),
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], "Mixed        → [4,-1,2,1]=6"),
        ([0, 0, 0, 0],                 "All zeros     → 0"),
    ]
    for arr, desc in tests:
        l, h, s = find_max_subarray(arr, 0, len(arr) - 1)
        print(f"  {desc:<35} subarray={arr[l:h+1]}, sum={s}")

    # ── Experimental Benchmarks ───────────────────────────────────────────
    print("\n── Experimental Comparison (synthetic profit/loss arrays) ──")
    print(f"  {'n':<10} | {'D&C':>12} | {'Brute Force':>12} | {'Kadane':>12} | max_sum")
    print("  " + "-" * 68)

    random.seed(2024)
    for size in [1_000, 5_000, 10_000, 50_000, 100_000]:
        benchmark_all(size)

    # ── Complexity Summary ────────────────────────────────────────────────
    print("\n── Complexity Summary ──")
    print(f"  {'Algorithm':<25} {'Time':>10}  {'Space':>10}  Note")
    print("  " + "-" * 65)
    print(f"  {'Brute Force':<25} {'O(n²)':>10}  {'O(1)':>10}  Enumerate all pairs (i,j)")
    print(f"  {'Divide & Conquer':<25} {'O(n log n)':>10}  {'O(log n)':>10}  Stack depth = log n")
    print(f"  {'Kadane (reference)':<25} {'O(n)':>10}  {'O(1)':>10}  Optimal; not D&C")
    print("\n  Master Theorem for D&C:")
    print("    T(n) = 2T(n/2) + O(n)  →  a=2, b=2, f(n)=O(n)")
    print("    n^(log₂ 2) = n¹ = n  →  Case 2  →  T(n) = Θ(n log n)")
