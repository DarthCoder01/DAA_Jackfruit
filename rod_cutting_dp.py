"""
rod_cutting_dp.py
=================
Design and Analysis of Algorithms – Question 2
Paradigm: Dynamic Programming

Rod Cutting Problem:
  Given a rod of length n and a price table p[1..n], find the maximum
  revenue obtainable by cutting the rod into pieces and selling them.

Recurrence (bottom-up):
  r(0) = 0
  r(n) = max { p[i] + r(n-i) }  for i = 1, 2, …, n

Includes:
  1. Bottom-up DP with cut reconstruction   → O(n²) time, O(n) space
  2. Top-down memoised recursion            → O(n²) time, O(n) space
  3. Extension: fixed cutting cost c/cut    → O(n²) time, O(n) space

Currency: All prices and revenues are expressed in Rupees (₹).

Team Members:
  Ashith Rao K   – PES1UG24CS559
  Girish G N     – PES1UG24CS571
  Ankith Sudala  – PES1UG24CS557
  Preetham V     – PES1UG24CS599
"""

import sys   # For recursion-limit adjustment in top-down version


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 1 — Bottom-Up Dynamic Programming  [O(n²) time, O(n) space]
# ─────────────────────────────────────────────────────────────────────────────

def rod_cut_bottom_up(p: list[int], n: int) -> tuple[int, list[int]]:
    """
    Solve the rod-cutting problem using bottom-up (tabulation) DP.

    Data structures used:
      - p : list[int]  — price table; p[i] = price (₹) of a rod of length i
                         (p[0] = 0, unused sentinel)
      - r : list[int]  — DP table; r[j] = max revenue for a rod of length j
      - s : list[int]  — cut table;  s[j] = best first-cut length for rod j

    Optimal Substructure:
      r(n) = max{ p[i] + r(n-i) }  for i in 1..n
      The optimal solution to a rod of length n embeds optimal solutions
      for every sub-rod of length n-i.

    Time Complexity:  O(n²) — outer loop n, inner loop j → total n(n+1)/2 ops
    Space Complexity: O(n)  — two arrays r[] and s[] of size n+1

    Parameters
    ----------
    p : 1-indexed price list (p[0] = 0 sentinel, p[1..n] = prices in ₹)
    n : total rod length

    Returns
    -------
    (max_revenue, s) where max_revenue is the optimal ₹ value and
    s is the cut-decision table for path reconstruction.
    """
    r = [0] * (n + 1)   # r[j] = max revenue from a rod of length j
    s = [0] * (n + 1)   # s[j] = first cut that achieves r[j]

    for j in range(1, n + 1):           # Subproblem size grows from 1 → n
        max_val = float('-inf')
        for i in range(1, j + 1):       # Try every possible first cut of length i
            candidate = p[i] + r[j - i]
            if candidate > max_val:
                max_val = candidate
                s[j] = i               # Record the best first-cut length
        r[j] = max_val                 # Store optimal revenue for length j

    return r[n], s


def reconstruct_cuts(s: list[int], n: int) -> list[int]:
    """
    Reconstruct the sequence of cuts from the cut-decision table s[].

    Follows the chain: cut s[n] from rod, recurse on remaining rod n - s[n].

    Time Complexity: O(n) — at most n cuts possible.

    Parameters
    ----------
    s : cut-decision table returned by rod_cut_bottom_up()
    n : original rod length

    Returns
    -------
    List of piece lengths in cutting order (e.g. [6, 2] for an 8-unit rod)
    """
    cuts = []
    while n > 0:
        cuts.append(s[n])   # Record the first cut
        n -= s[n]           # Remaining rod after the cut
    return cuts


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 2 — Top-Down Memoisation  [O(n²) time, O(n) space]
# ─────────────────────────────────────────────────────────────────────────────

def rod_cut_top_down(p: list[int], n: int, memo: dict = None) -> int:
    """
    Solve the rod-cutting problem using top-down recursion with memoisation.

    Data structures used:
      - memo : dict {length: max_revenue} — memoisation cache (hash map)

    Same asymptotic complexity as bottom-up but incurs Python call-stack
    overhead; bottom-up is preferred for large n.

    Time Complexity:  O(n²) — each subproblem computed exactly once
    Space Complexity: O(n)  — memo dict + O(n) recursion stack depth

    Parameters
    ----------
    p    : 1-indexed price list
    n    : rod length to solve for
    memo : shared memoisation dict (initialised automatically on first call)

    Returns
    -------
    Maximum revenue (₹) for a rod of length n
    """
    if memo is None:
        memo = {}

    if n == 0:
        return 0                        # Base case: zero-length rod has no revenue
    if n in memo:
        return memo[n]                  # Return cached result

    max_val = float('-inf')
    for i in range(1, n + 1):          # Try every first-cut length i
        val = p[i] + rod_cut_top_down(p, n - i, memo)
        if val > max_val:
            max_val = val

    memo[n] = max_val                  # Cache before returning
    return max_val


# ─────────────────────────────────────────────────────────────────────────────
# EXTENSION — Fixed Cutting Cost c Per Cut  [O(n²) time, O(n) space]
# ─────────────────────────────────────────────────────────────────────────────

def rod_cut_with_cost(p: list[int], n: int, c: int) -> tuple[int, list[int]]:
    """
    Rod-cutting with a fixed cost c (₹) charged per physical cut made.

    Modified Recurrence:
      r(0) = 0
      r(n) = max {
                p[n],                        # sell whole rod — no cut cost
                max{ p[i] + r(n-i) - c }    # cut of length i, pay ₹c once
              }   for i = 1, …, n-1

    Key insight: the cutting cost discourages many small cuts.
    The algorithm may prefer fewer, larger pieces depending on c.

    Time Complexity:  O(n²) — same as standard rod cutting
    Space Complexity: O(n)

    Parameters
    ----------
    p : 1-indexed price list (₹)
    n : total rod length
    c : fixed cost (₹) charged for each cut operation

    Returns
    -------
    (max_net_revenue, s) — net revenue after cut costs, plus cut table
    """
    r = [0] * (n + 1)
    s = [0] * (n + 1)

    for j in range(1, n + 1):
        max_val = p[j]      # Option 0: sell the rod whole (no cut, no cost)
        s[j] = j

        for i in range(1, j):           # Try cuts that produce piece of length i
            val = p[i] + r[j - i] - c  # Subtract ₹c for the cut
            if val > max_val:
                max_val = val
                s[j] = i

        r[j] = max_val

    return r[n], s


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT — trace + test cases
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print("  ROD CUTTING — Dynamic Programming")
    print("  DAA Project | PES University")
    print("=" * 65)

    # ── Example price table (n = 8) ───────────────────────────────────────
    # Length i:  1    2    3    4    5    6    7    8
    # Price ₹:   1    5    8    9   10   17   17   20
    p = [0, 1, 5, 8, 9, 10, 17, 17, 20]   # p[0] = 0 (unused sentinel)
    n = 8

    print(f"\n── Price Table (rod length 1–{n}) ──")
    print(f"  Length : {list(range(1, n + 1))}")
    print(f"  Price  : {[p[i] for i in range(1, n + 1)]} (₹)")

    # ── Bottom-Up DP Trace ────────────────────────────────────────────────
    print(f"\n── Bottom-Up DP Trace (n = {n}) ──")
    r_table = [0] * (n + 1)
    s_table = [0] * (n + 1)
    print(f"{'j (len)':<10} {'Best cut s[j]':<16} {'r[j] (₹)':<12} {'Pieces'}")
    print("-" * 55)
    for j in range(1, n + 1):
        mx = float('-inf')
        for i in range(1, j + 1):
            if p[i] + r_table[j - i] > mx:
                mx = p[i] + r_table[j - i]
                s_table[j] = i
        r_table[j] = mx
        # Reconstruct pieces for display
        rem, pieces = j, []
        temp_s = s_table[:]
        while rem > 0:
            pieces.append(str(temp_s[rem]))
            rem -= temp_s[rem]
        print(f"  {j:<8} {s_table[j]:<16} {r_table[j]:<12} {'+'.join(pieces)}")

    revenue, s = rod_cut_bottom_up(p, n)
    cuts = reconstruct_cuts(s, n)
    print(f"\n  ✔ Maximum Revenue : ₹{revenue}")
    print(f"  ✔ Optimal Cuts    : {cuts}  (pieces that maximise revenue)")

    # ── Top-Down Verification ─────────────────────────────────────────────
    sys.setrecursionlimit(10_000)
    td_revenue = rod_cut_top_down(p, n)
    print(f"\n── Top-Down Memoisation Result: ₹{td_revenue}  "
          f"({'✔ matches' if td_revenue == revenue else '✗ MISMATCH'})")

    # ── Extension: Fixed Cut Cost c = ₹2 per cut ─────────────────────────
    c = 2
    print(f"\n── Extension: Fixed Cutting Cost c = ₹{c}/cut ──")
    net_revenue, sc = rod_cut_with_cost(p, n, c)
    cost_cuts = reconstruct_cuts(sc, n)
    num_cuts   = len(cost_cuts) - 1          # Number of physical cuts made
    gross      = sum(p[piece] for piece in cost_cuts)
    total_cost = num_cuts * c
    print(f"  Cuts         : {cost_cuts}")
    print(f"  Gross Revenue: ₹{gross}")
    print(f"  Cutting Cost : {num_cuts} cut(s) × ₹{c} = ₹{total_cost}")
    print(f"  Net Revenue  : ₹{net_revenue}")

    # ── Naïve Recursive Complexity Note ──────────────────────────────────
    print("\n── Complexity Summary ──")
    print(f"  {'Approach':<25} {'Time':>10}  {'Space':>10}")
    print("  " + "-" * 48)
    print(f"  {'Naïve Recursive':<25} {'O(2ⁿ)':>10}  {'O(n)':>10}")
    print(f"  {'Top-Down Memo':<25} {'O(n²)':>10}  {'O(n)':>10}")
    print(f"  {'Bottom-Up DP':<25} {'O(n²)':>10}  {'O(n)':>10}")
    print(f"  {'With Cut Cost c':<25} {'O(n²)':>10}  {'O(n)':>10}")

    # ── Additional test cases ─────────────────────────────────────────────
    print("\n── Additional Test Cases ──")
    test_cases = [
        ([0, 1, 5, 8, 9], 4),     # Classic n=4 case; expected ₹10 (2+2)
        ([0, 3, 5, 8, 9, 10], 5), # n=5
    ]
    for tp, tn in test_cases:
        tr, ts = rod_cut_bottom_up(tp, tn)
        tc = reconstruct_cuts(ts, tn)
        print(f"  n={tn}: revenue=₹{tr}, cuts={tc}")
