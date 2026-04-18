# Design and Analysis of Algorithms — Project

> **Course:** Design and Analysis of Algorithms (DAA)  
> **Institution:** PES University  

---

## Team Members

| Name | USN |
|---|---|
| Ashith Rao K | PES1UG24CS559 |
| Girish G N | PES1UG24CS571 |
| Ankith Sudala | PES1UG24CS557 |
| Preetham V | PES1UG24CS599 |

---

## Project Overview

This project demonstrates three foundational algorithm design paradigms through carefully chosen problems, each implemented in Python with full complexity analysis and experimental benchmarking.

| # | Paradigm | Problem | Time Complexity |
|---|---|---|---|
| 1 | **Decrease and Conquer** | Dijkstra's Shortest Path | O((V + E) log V) |
| 2 | **Dynamic Programming** | Rod Cutting | O(n²) |
| 3 | **Divide and Conquer** | Maximum Subarray | O(n log n) |

---

## Paradigm Summaries

### 1. Decrease and Conquer — Dijkstra's Algorithm

The problem size shrinks by **one vertex per iteration**: the unresolved set U starts at |V| and drops to 0. A min-heap priority queue ensures the greedy extraction of the closest unvisited vertex in O(log V), making the total complexity O((V + E) log V) for sparse graphs and O(V²) for the adjacency-matrix variant on dense graphs.

### 2. Dynamic Programming — Rod Cutting

The problem exhibits **optimal substructure**: the best way to cut a rod of length n includes optimal solutions for every sub-rod. The bottom-up DP table is filled from length 1 to n, solving each subproblem exactly once. An extension supports a fixed per-cut cost, changing the optimal strategy without affecting asymptotic complexity.

### 3. Divide and Conquer — Maximum Subarray

The array is recursively halved (DIVIDE), each half is solved independently (CONQUER), and then the best crossing subarray is computed in O(n) (COMBINE). By the Master Theorem (Case 2: a=2, b=2, f(n)=O(n) → T(n) = Θ(n log n)), this is significantly faster than the O(n²) brute-force approach.

---

## Repository Structure

```
.
├── dijkstra_decrease_conquer.py    # Q1: Dijkstra (heap + matrix), benchmarks
├── rod_cutting_dp.py               # Q2: Rod cutting (bottom-up, top-down, cost variant)
├── max_subarray_divide_conquer.py  # Q3: Max subarray (D&C, brute force, Kadane)
├── DAA_Project_JF.pdf              # Full project report
└── README.md
```

---

## Requirements

- **Python 3.10+** (uses `list[int]` type hints; no third-party packages required)
- All algorithms use only the Python standard library: `heapq`, `math`, `time`, `random`, `sys`

---

## How to Run

Clone the repository and run each file directly — every file contains a `if __name__ == "__main__":` block with built-in test cases and benchmarks.

```bash
git clone <your-repo-url>
cd daa-project

# Question 1 — Dijkstra's Algorithm
python dijkstra_decrease_conquer.py

# Question 2 — Rod Cutting
python rod_cutting_dp.py

# Question 3 — Maximum Subarray
python max_subarray_divide_conquer.py
```

### Expected Output (abbreviated)

**`dijkstra_decrease_conquer.py`**
```
Vertex     Shortest Dist   Path from A
A          0               A
B          3               A → C → B
C          2               A → C
D          6               A → C → B → D
E          4               A → C → B → E
F          7               A → C → B → E → F

Sparse n=500   | Heap:   ~0.012 ms | Matrix:  ~0.31 ms | Winner: Heap
Dense  n=500   | Heap:   ~0.48 ms  | Matrix:  ~0.29 ms | Winner: Matrix
```

**`rod_cutting_dp.py`**
```
Maximum Revenue : ₹22
Optimal Cuts    : [6, 2]
```

**`max_subarray_divide_conquer.py`**
```
D&C   : A[7..10] = [18, 20, -7, 12], Sum = 43
✔ All three approaches agree.
```

---

## Complexity Reference

### Dijkstra's Algorithm

| Implementation | Extract-Min | Decrease-Key | Total |
|---|---|---|---|
| Adjacency Matrix + linear scan | O(V) | O(1) | **O(V²)** |
| Binary Heap + adjacency list | O(log V) | O(log V) | **O((V+E) log V)** |
| Fibonacci Heap (theoretical) | O(log V) amortised | O(1) amortised | **O(E + V log V)** |

### Rod Cutting

| Approach | Time | Space |
|---|---|---|
| Naïve recursive | O(2ⁿ) | O(n) |
| Top-down memoisation | O(n²) | O(n) |
| Bottom-up DP | O(n²) | O(n) |

### Maximum Subarray

| Algorithm | Time | Space |
|---|---|---|
| Brute Force | O(n²) | O(1) |
| Divide and Conquer | O(n log n) | O(log n) stack |
| Kadane's (reference) | O(n) | O(1) |

**Master Theorem for D&C Max Subarray:**
```
T(n) = 2T(n/2) + O(n)
a=2, b=2, f(n)=O(n), n^(log₂2) = n¹
f(n) = Θ(n^(log_b a))  →  Case 2  →  T(n) = Θ(n log n)
```

---

## Experimental Setup

Benchmarks use **synthetically generated graphs and arrays** with a fixed random seed (42 / 2024) for reproducibility:

- **Dijkstra sparse:** n ∈ {500, 1000} vertices, ~2n random directed edges, weights ∈ [1, 100]
- **Dijkstra dense:** n ∈ {500, 1000} vertices, ~48% of all possible edges populated
- **Max Subarray:** arrays of size n ∈ {1 000, 5 000, 10 000, 50 000, 100 000}, values ∈ [−50, 100]

Results confirm theoretical predictions: heap beats matrix on sparse graphs; D&C (O(n log n)) substantially outpaces brute force (O(n²)) at n = 100 000.
