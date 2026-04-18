"""
dijkstra_decrease_conquer.py
============================
Design and Analysis of Algorithms – Question 1
Paradigm: Decrease and Conquer

Dijkstra's Shortest Path Algorithm implemented in two ways:
  1. Binary Min-Heap + Adjacency List  → O((V + E) log V)
  2. Adjacency Matrix + Linear Scan    → O(V²)

An experimental comparison section benchmarks both on sparse and dense graphs.

Team Members:
  Ashith Rao K   – PES1UG24CS559
  Girish G N     – PES1UG24CS571
  Ankith Sudala  – PES1UG24CS557
  Preetham V     – PES1UG24CS599
"""

import heapq       # Python's built-in min-heap (binary heap)
import math        # For math.inf (∞ representation)
import time        # For wall-clock benchmarking
import random      # For synthetic graph generation


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 1 — Binary Heap + Adjacency List  [O((V + E) log V)]
# ─────────────────────────────────────────────────────────────────────────────

def dijkstra_heap(graph: dict, source) -> tuple[dict, dict]:
    """
    Dijkstra's algorithm using a min-priority queue (binary heap).

    Data structures used:
      - graph  : dict  { u: [(v, weight), ...] }  — adjacency list
      - dist   : dict  { v: float }               — shortest distance from source
      - prev   : dict  { v: vertex | None }       — predecessor for path recon.
      - heap   : list  [(distance, vertex)]       — Python heapq (min-heap)
      - visited: set                              — finalized vertices

    Decrease-and-Conquer insight:
      Each heappop() permanently finalises exactly ONE vertex, shrinking the
      unresolved set U by 1 per iteration.  After |V| iterations, |U| = 0.

    Time Complexity:
      - Each vertex extracted once         → O(V log V)  [V pops from heap]
      - Each edge relaxed at most once     → O(E log V)  [E pushes to heap]
      - Total                              → O((V + E) log V)

    Space Complexity: O(V + E) for adjacency list, O(V) for dist/prev/visited.

    Parameters
    ----------
    graph  : adjacency list as {u: [(v, w), ...]}
    source : starting vertex key

    Returns
    -------
    dist : shortest distances from source to every reachable vertex
    prev : predecessor map for path reconstruction
    """
    # Initialise all distances to infinity; source distance = 0
    dist = {v: math.inf for v in graph}
    prev = {v: None    for v in graph}
    dist[source] = 0

    # Push (distance, vertex) tuples; Python heapq is a min-heap by default
    heap = [(0, source)]
    visited: set = set()

    while heap:
        d, u = heapq.heappop(heap)   # Extract vertex with smallest tentative dist

        if u in visited:
            # Stale entry – a shorter path was already found for u
            continue
        visited.add(u)               # Finalise vertex u (decrease problem by 1)

        for v, weight in graph[u]:
            if v not in visited:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:          # Relaxation step
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(prev: dict, source, target) -> list:
    """
    Reconstruct the shortest path from source → target using the prev[] map.

    Time Complexity: O(V) in the worst case (path traverses all vertices).

    Parameters
    ----------
    prev   : predecessor dictionary returned by dijkstra_heap()
    source : starting vertex
    target : destination vertex

    Returns
    -------
    List of vertices forming the shortest path, or [] if no path exists.
    """
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path and path[0] == source:
        return path
    return []   # No path exists from source to target


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION 2 — Adjacency Matrix + Linear Scan  [O(V²)]
# ─────────────────────────────────────────────────────────────────────────────

def dijkstra_matrix(matrix: list[list[float]], source: int) -> list[float]:
    """
    Dijkstra's algorithm using an adjacency matrix and linear scan for min.

    Data structures used:
      - matrix  : V×V list of floats (math.inf = no edge)
      - dist    : list[float] — shortest distance from source
      - visited : list[bool]  — whether vertex is finalised

    Time Complexity:
      - Outer loop runs V times
      - Inner linear scan for minimum  → O(V) per iteration
      - Edge relaxation scan           → O(V) per iteration
      - Total                          → O(V²)
      Best for DENSE graphs where E ≈ V² (matrix overhead is amortised).

    Space Complexity: O(V²) for the matrix itself.

    Parameters
    ----------
    matrix : V×V adjacency matrix; matrix[u][v] = edge weight or math.inf
    source : integer index of the source vertex

    Returns
    -------
    dist : list of shortest distances from source to each vertex index
    """
    n       = len(matrix)
    dist    = [math.inf] * n
    visited = [False] * n
    dist[source] = 0

    for _ in range(n):
        # Find the unvisited vertex with the smallest tentative distance (O(V))
        u = min(
            (d, i) for i, d in enumerate(dist) if not visited[i]
        )[1]
        visited[u] = True   # Finalise vertex u

        # Relax all outgoing edges from u (O(V))
        for v in range(n):
            if not visited[v] and matrix[u][v] < math.inf:
                new_dist = dist[u] + matrix[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist


# ─────────────────────────────────────────────────────────────────────────────
# GRAPH BUILDERS — helper utilities for the experimental section
# ─────────────────────────────────────────────────────────────────────────────

def build_adjacency_list(n: int, edges: list[tuple]) -> dict:
    """
    Build an adjacency-list graph from an edge list.

    Parameters
    ----------
    n     : number of vertices (labelled 0 … n-1)
    edges : list of (u, v, weight) tuples

    Returns
    -------
    dict {vertex: [(neighbour, weight), ...]}
    """
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph


def build_adjacency_matrix(n: int, edges: list[tuple]) -> list[list[float]]:
    """
    Build a V×V adjacency matrix from an edge list.

    Parameters
    ----------
    n     : number of vertices
    edges : list of (u, v, weight) tuples

    Returns
    -------
    V×V list of floats; diagonal = 0, missing edges = math.inf
    """
    matrix = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0          # Self-loop cost is zero
    for u, v, w in edges:
        matrix[u][v] = w
    return matrix


# ─────────────────────────────────────────────────────────────────────────────
# EXPERIMENTAL COMPARISON — sparse vs. dense graphs
# ─────────────────────────────────────────────────────────────────────────────

def benchmark(n: int, edges: list[tuple], label: str) -> None:
    """
    Time both Dijkstra implementations on the same graph and print results.

    Parameters
    ----------
    n     : number of vertices
    edges : edge list (u, v, weight)
    label : human-readable graph descriptor (e.g. 'Sparse n=500')
    """
    graph  = build_adjacency_list(n, edges)
    matrix = build_adjacency_matrix(n, edges)

    # --- Binary Heap ---
    t0 = time.perf_counter()
    dijkstra_heap(graph, source=0)
    t_heap = time.perf_counter() - t0

    # --- Adjacency Matrix ---
    t0 = time.perf_counter()
    dijkstra_matrix(matrix, source=0)
    t_mat = time.perf_counter() - t0

    winner = "Heap" if t_heap < t_mat else "Matrix"
    print(f"{label:<30} | Vertices: {n:>4} | Edges: {len(edges):>7} "
          f"| Heap: {t_heap*1000:>7.3f} ms | Matrix: {t_mat*1000:>7.3f} ms "
          f"| Winner: {winner}")


def generate_sparse_edges(n: int, multiplier: int = 2) -> list[tuple]:
    """Generate ~n*multiplier random directed edges (sparse graph, E ≈ 2V)."""
    edges = set()
    while len(edges) < n * multiplier:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edges.add((u, v, random.randint(1, 100)))
    return list(edges)


def generate_dense_edges(n: int) -> list[tuple]:
    """Generate ≈ 48% of all possible directed edges (dense graph, E ≈ V²/2)."""
    edges = []
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < 0.48:
                edges.append((u, v, random.randint(1, 100)))
    return edges


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT — manual trace + experimental benchmarks
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("  DIJKSTRA'S ALGORITHM — Decrease and Conquer")
    print("  DAA Project | PES University")
    print("=" * 70)

    # ── Trace: 6-Vertex Sample Graph ──────────────────────────────────────
    # Vertices: A, B, C, D, E, F   |   Source: A
    # Edges (directed, weighted):
    #   A→B:4, A→C:2, B→D:3, B→E:1, C→B:1, C→D:5, D→F:2, E→F:3
    sample_graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('D', 3), ('E', 1)],
        'C': [('B', 1), ('D', 5)],
        'D': [('F', 2)],
        'E': [('F', 3)],
        'F': [],
    }

    print("\n── Trace: 6-Vertex Sample Graph (source = A) ──")
    dist, prev = dijkstra_heap(sample_graph, 'A')

    print(f"\n{'Vertex':<10} {'Shortest Dist':<15} {'Path from A'}")
    print("-" * 50)
    for vertex in ['A', 'B', 'C', 'D', 'E', 'F']:
        path = reconstruct_path(prev, 'A', vertex)
        path_str = " → ".join(path) if path else "unreachable"
        print(f"  {vertex:<8} {dist[vertex]:<15} {path_str}")

    # Expected output:
    #   A: 0   (A)
    #   B: 3   (A → C → B)
    #   C: 2   (A → C)
    #   D: 6   (A → C → B → D)
    #   E: 4   (A → C → B → E)
    #   F: 7   (A → C → B → E → F)

    # ── Experimental Benchmarks ───────────────────────────────────────────
    print("\n── Experimental Comparison: Heap vs. Matrix ──")
    print(f"{'Graph':<30} | {'Vertices':>8} | {'Edges':>7} "
          f"| {'Heap':>12} | {'Matrix':>12} | {'Winner'}")
    print("-" * 90)

    random.seed(42)   # Reproducible results
    for n in [500, 1000]:
        benchmark(n, generate_sparse_edges(n, multiplier=2), f"Sparse n={n}")
    for n in [500, 1000]:
        benchmark(n, generate_dense_edges(n), f"Dense  n={n}")

    print("\nConclusion:")
    print("  • Binary Heap wins on SPARSE graphs  (E << V²)  → O((V+E) log V)")
    print("  • Adjacency Matrix wins on DENSE graphs (E ≈ V²) → O(V²)")
