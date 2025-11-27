import time
from io_utils import tour_cost

# Brute-force TSP solver

def _nn_init(W):
    n=len(W)
    unv=set(range(1,n))
    tour=[0]; u=0
    while unv:
        v=min(unv, key=lambda x: W[u][x])
        unv.remove(v); tour.append(v); u=v
    return tour

def solve_bf(W, cutoff=None):
    if cutoff is None: cutoff = 60
    n = len(W)
    t_end = time.time() + cutoff

    ub_path = _nn_init(W)
    ub_cost = tour_cost(ub_path, W)

    best_path_holder = [ub_path]
    best_cost_holder = [ub_cost]

    used = [False]*n
    used[0] = True
    path = [0]

    found_first_full = [False]

    def dfs(u, depth, acc):
        if time.time() >= t_end and found_first_full[0]:
            return True

        if depth == n:
            total = acc + W[u][path[0]]
            if total < best_cost_holder[0]:
                best_cost_holder[0] = total
                best_path_holder[0] = path[:]
            found_first_full[0] = True
            return False


        cand = [v for v in range(1, n) if not used[v]]
        cand.sort(key=lambda v: W[u][v])

        for v in cand:
            nc = acc + W[u][v]
            if nc >= best_cost_holder[0]:
                continue
            used[v] = True
            path.append(v)
            stop = dfs(v, depth+1, nc)
            path.pop()
            used[v] = False
            if stop:
                return True
        return False

    dfs(0, 1, 0.0)

    bp = best_path_holder[0]
    bc = best_cost_holder[0]
    if bp is None:
        bp = list(range(n))
        bc = tour_cost(bp, W)
    return bp, float(bc)