from io_utils import tour_cost
import heapq

# Prim's algorithm to find the Minimum Spanning Tree (MST)

def MST_PRIM(W):
    # Initialize
    n = len(W)
    pq = [] # Priority queue to store vertices with their minimum distance
    r = 0 # Taking vertex 0 as the root
    key = [float("inf")] * n # Initialize all keys as infinite
    parent = [-1] * n # store the parent
    T = [False] * n # Nodes in MST
    heapq.heappush(pq, (0, r)) # Insert root into the priority queue
    key[r] = 0 # initialize roots key as 0

    while pq: # While pq is not empty
        u = heapq.heappop(pq)[1] # Current vertex. Pop the vertex with the smallest distance
        if T[u]: # If the current vertex is already included in MST, skip it
            continue
        T[u] = True

        for v in range(n): # Iterate through all neighbors of u
            if not T[v] and W[u][v] < key[v]:
                key[v] = W[u][v]
                heapq.heappush(pq, (key[v], v)) # Enqueue the node found to be less distance
                parent[v] = u

    # Build adjacency list for MST
    T_adj = [[] for _ in range(n)]
    for v in range(1, n):
        u = parent[v]
        T_adj[u].append(v)
        T_adj[v].append(u)
    return T_adj

def preorder(adj, root=0):
    H = [] # Preorder list
    stack =[root] # DFS stack
    visited = [False] * len(adj)
    while stack:
        current = stack.pop()
        if not visited[current]:
            visited[current] = True
            H.append(current)
            for v in reversed(adj[current]): # Explore neighbors in reversed order to maintain order
                if not visited[v]: # If the nieghbor is not visited
                    stack.append(v) # Add to stack
    return H

def solve_approx(W):
    T_adj = MST_PRIM(W)
    H = preorder(T_adj, 0)
    cost = tour_cost(H, W)
    return H, cost