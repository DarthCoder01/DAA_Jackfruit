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
"""

import math
import time
import random

# ─────────────────────────────────────────────────────────────────────────────
# HELPER — Find Maximum Crossing Subarray  [O(n)]
# ─────────────────────────────────────────────────────────────────────────────

def find_max_crossing(A: list[int], lo: int, mid: int, hi: int) -> tuple[int, int, int]:
    left_sum = -math.inf
    total    = 0
    max_left = mid

    for i in range(mid, lo - 1, -1):
        total += A[i]
        if total > left_sum:
            left_sum = total
            max_left = i

    right_sum = -math.inf
    total     = 0
    max_right = mid + 1

    for j in range(mid + 1, hi + 1):
        total += A[j]
        if total > right_sum:
            right_sum = total
            max_right = j

    return max_left, max_right, left_sum + right_sum

# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 1 — Divide and Conquer  [O(n log n)]
# ─────────────────────────────────────────────────────────────────────────────

def find_max_subarray(A: list[int], lo: int, hi: int) -> tuple[int, int, int]:
    if lo == hi:
        return lo, hi, A[lo]

    mid = (lo + hi) // 2

    left_lo,  left_hi,  left_sum  = find_max_subarray(A, lo,      mid)
    right_lo, right_hi, right_sum = find_max_subarray(A, mid + 1, hi)

    cross_lo, cross_hi, cross_sum = find_max_crossing(A, lo, mid, hi)

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
# IMPLEMENTATION 3 — Kadane's Algorithm  [O(n)]
# ─────────────────────────────────────────────────────────────────────────────

def max_subarray_kadane(A: list[int]) -> tuple[int, int, int]:
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
# EXPERIMENTAL COMPARISON & CUSTOM TEST CASE
# ─────────────────────────────────────────────────────────────────────────────

def benchmark_all(n: int) -> None:
    A = [random.randint(-50, 100) for _ in range(n)]

    t0 = time.perf_counter()
    lo_dc, hi_dc, sum_dc = find_max_subarray(A, 0, n - 1)
    t_dc = time.perf_counter() - t0

    if n <= 10_000:
        t0 = time.perf_counter()
        lo_bf, hi_bf, sum_bf = max_subarray_brute(A)
        t_bf = time.perf_counter() - t0
        bf_str = f"{t_bf * 1000:>9.3f} ms"
    else:
        sum_bf = sum_dc
        bf_str = f"{'(skipped)':>12}"

    t0 = time.perf_counter()
    lo_kd, hi_kd, sum_kd = max_subarray_kadane(A)
    t_kd = time.perf_counter() - t0

    assert sum_dc == sum_kd == sum_bf, f"MISMATCH at n={n}"

    print(f"  n={n:<8} | D&C: {t_dc*1000:>8.3f} ms"
          f" | Brute: {bf_str}"
          f" | Kadane: {t_kd*1000:>8.4f} ms"
          f" | max_sum={sum_dc}")

def run_custom_test_case():
    print("\n── Custom Test Case ──")
    try:
        user_input = input("Enter array elements separated by spaces (e.g., -2 1 -3 4 -1 2 1 -5 4): ")
        A = list(map(int, user_input.split()))
        
        if not A:
            print("Error: Array cannot be empty.")
            return

        n = len(A)
        print(f"\nInput Array: {A}")

        print("\n[Running Divide & Conquer (O(n log n))]")
        lo_dc, hi_dc, sum_dc = find_max_subarray(A, 0, n - 1)
        print(f"  Max Sum: {sum_dc}")
        print(f"  Subarray: {A[lo_dc:hi_dc+1]} at indices [{lo_dc}..{hi_dc}]")

        print("\n[Running Brute Force (O(n²))]")
        lo_bf, hi_bf, sum_bf = max_subarray_brute(A)
        print(f"  Max Sum: {sum_bf}")
        print(f"  Subarray: {A[lo_bf:hi_bf+1]} at indices [{lo_bf}..{hi_bf}]")

        print("\n[Running Kadane's Algorithm (O(n))]")
        lo_kd, hi_kd, sum_kd = max_subarray_kadane(A)
        print(f"  Max Sum: {sum_kd}")
        print(f"  Subarray: {A[lo_kd:hi_kd+1]} at indices [{lo_kd}..{hi_kd}]")

    except ValueError:
        print("Invalid input! Make sure you are entering only numbers separated by spaces.")

# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT — INTERACTIVE MENU
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("  MAXIMUM SUBARRAY — Divide and Conquer")
    print("  DAA Project | PES University")
    print("=" * 70)

    while True:
        print("\nMenu:")
        print("1. Run Classic Textbook Trace (CLRS Example)")
        print("2. Run Additional Edge Cases")
        print("3. Run Experimental Benchmarks (D&C vs Brute vs Kadane)")
        print("4. Print Complexity Summary")
        print("5. Enter Custom Test Case")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
            print(f"\n── Classic Trace ──")
            print(f"  Input : {A}")
            lo, hi, total = find_max_subarray(A, 0, len(A) - 1)
            print(f"  D&C   : A[{lo}..{hi}] = {A[lo:hi+1]}, Sum = {total}")
            lo_b, hi_b, total_b = max_subarray_brute(A)
            print(f"  Brute : A[{lo_b}..{hi_b}] = {A[lo_b:hi_b+1]}, Sum = {total_b}")
            lo_k, hi_k, total_k = max_subarray_kadane(A)
            print(f"  Kadane: A[{lo_k}..{hi_k}] = {A[lo_k:hi_k+1]}, Sum = {total_k}")
            print("  ✔ All three approaches agree.")
            
        elif choice == '2':
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
                
        elif choice == '3':
            print("\n── Experimental Comparison (synthetic profit/loss arrays) ──")
            print(f"  {'n':<10} | {'D&C':>12} | {'Brute Force':>12} | {'Kadane':>12} | max_sum")
            print("  " + "-" * 68)
            random.seed(2024)
            for size in [1_000, 5_000, 10_000, 50_000, 100_000]:
                benchmark_all(size)
                
        elif choice == '4':
            print("\n── Complexity Summary ──")
            print(f"  {'Algorithm':<25} {'Time':>10}  {'Space':>10}  Note")
            print("  " + "-" * 65)
            print(f"  {'Brute Force':<25} {'O(n²)':>10}  {'O(1)':>10}  Enumerate all pairs (i,j)")
            print(f"  {'Divide & Conquer':<25} {'O(n log n)':>10}  {'O(log n)':>10}  Stack depth = log n")
            print(f"  {'Kadane (reference)':<25} {'O(n)':>10}  {'O(1)':>10}  Optimal; not D&C")
            print("\n  Master Theorem for D&C:")
            print("    T(n) = 2T(n/2) + O(n)  →  a=2, b=2, f(n)=O(n)")
            print("    n^(log₂ 2) = n¹ = n  →  Case 2  →  T(n) = Θ(n log n)")
            
        elif choice == '5':
            run_custom_test_case()
            
        elif choice == '6':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice, try again.")
