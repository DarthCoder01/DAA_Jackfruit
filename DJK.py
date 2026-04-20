"""
Dijkstra's Shortest Path Algorithm implemented in two ways:
  1. Binary Min-Heap + Adjacency List  → O((V + E) log V)
  2. Adjacency Matrix + Linear Scan    → O(V²)
"""

import heapq
import math
import time
import random

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHMS
# ─────────────────────────────────────────────────────────────────────────────

def dijkstra_heap(graph: dict, source) -> tuple[dict, dict]:
    dist = {v: math.inf for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0

    heap = [(0, source)]
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)

        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph[u]:
            if v not in visited:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(heap, (new_dist, v))

    return dist, prev

def reconstruct_path(prev: dict, source, target) -> list:
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path and path[0] == source:
        return path
    return []

def dijkstra_matrix(matrix: list[list[float]], source: int) -> list[float]:
    n = len(matrix)
    dist = [math.inf] * n
    visited = [False] * n
    dist[source] = 0

    for _ in range(n):
        u = min((d, i) for i, d in enumerate(dist) if not visited[i])[1]
        visited[u] = True

        for v in range(n):
            if not visited[v] and matrix[u][v] < math.inf:
                new_dist = dist[u] + matrix[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist

# ─────────────────────────────────────────────────────────────────────────────
# GRAPH BUILDERS & BENCHMARKS
# ─────────────────────────────────────────────────────────────────────────────

def build_adjacency_list(n: int, edges: list[tuple]) -> dict:
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph

def build_adjacency_matrix(n: int, edges: list[tuple]) -> list[list[float]]:
    matrix = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    for u, v, w in edges:
        matrix[u][v] = w
    return matrix

def benchmark(n: int, edges: list[tuple], label: str) -> None:
    graph = build_adjacency_list(n, edges)
    matrix = build_adjacency_matrix(n, edges)

    t0 = time.perf_counter()
    dijkstra_heap(graph, source=0)
    t_heap = time.perf_counter() - t0

    t0 = time.perf_counter()
    dijkstra_matrix(matrix, source=0)
    t_mat = time.perf_counter() - t0

    winner = "Heap" if t_heap < t_mat else "Matrix"
    print(f"{label:<30} | Vertices: {n:>4} | Edges: {len(edges):>7} "
          f"| Heap: {t_heap*1000:>7.3f} ms | Matrix: {t_mat*1000:>7.3f} ms "
          f"| Winner: {winner}")

def generate_sparse_edges(n: int, multiplier: int = 2) -> list[tuple]:
    edges = set()
    while len(edges) < n * multiplier:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edges.add((u, v, random.randint(1, 100)))
    return list(edges)

def generate_dense_edges(n: int) -> list[tuple]:
    edges = []
    for u in range(n):
        for v in range(n):
            if u != v and random.random() < 0.48:
                edges.append((u, v, random.randint(1, 100)))
    return edges

# ─────────────────────────────────────────────────────────────────────────────
# INTERACTIVE MENU
# ─────────────────────────────────────────────────────────────────────────────

def run_custom_test_case():
    print("\n── Custom Test Case ──")
    try:
        n = int(input("Enter number of vertices (e.g., 5 for nodes 0 to 4): "))
        e = int(input("Enter number of edges: "))
        
        print("Enter each edge as: source destination weight (separated by spaces)")
        edges = []
        for i in range(e):
            u, v, w = map(int, input(f"Edge {i+1}: ").split())
            edges.append((u, v, w))
            
        source = int(input("Enter the source vertex: "))
        
        graph = build_adjacency_list(n, edges)
        matrix = build_adjacency_matrix(n, edges)
        
        print("\n[Running Heap + Adjacency List]")
        dist_heap, prev = dijkstra_heap(graph, source)
        for i in range(n):
            path = reconstruct_path(prev, source, i)
            path_str = " → ".join(map(str, path)) if path else "unreachable"
            print(f"Node {i}: Dist = {dist_heap[i]}, Path = {path_str}")
            
        print("\n[Running Matrix + Linear Scan]")
        dist_matrix = dijkstra_matrix(matrix, source)
        for i in range(n):
            print(f"Node {i}: Dist = {dist_matrix[i]}")
            
    except ValueError:
        print("Invalid input! Make sure you are entering numbers.")

if __name__ == "__main__":
    print("=" * 70)
    print("  DIJKSTRA'S ALGORITHM — Decrease and Conquer")
    print("  DAA Project | PES University")
    print("=" * 70)

    while True:
        print("\nMenu:")
        print("1. Run Default Trace (6-Vertex Sample)")
        print("2. Run Experimental Benchmarks (Heap vs Matrix)")
        print("3. Enter Custom Test Case")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
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
            for vertex in ['A', 'B', 'C', 'D', 'E', 'F']:
                path = reconstruct_path(prev, 'A', vertex)
                path_str = " → ".join(path) if path else "unreachable"
                print(f"  {vertex:<8} {dist[vertex]:<15} {path_str}")
                
        elif choice == '2':
            print("\n── Experimental Comparison: Heap vs. Matrix ──")
            random.seed(42)
            for n in [500, 1000]:
                benchmark(n, generate_sparse_edges(n, multiplier=2), f"Sparse n={n}")
            for n in [500, 1000]:
                benchmark(n, generate_dense_edges(n), f"Dense  n={n}")
                
        elif choice == '3':
            run_custom_test_case()
            
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")
