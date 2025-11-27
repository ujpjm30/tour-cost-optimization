import random, time
import numpy as np
from io_utils import tour_cost

# Local Search TSP solver with 2-opt

def _nn_init(W):
    n = len(W)
    start = random.randint(0, n-1) # random start node

    unvisited = set(range(n)) 
    unvisited.remove(start) # build unvisited nodes

    # Iteratively build the tour
    tour = [start]
    current = start
    while unvisited:
        next = min(unvisited, key=lambda v: W[current][v]) # nearest neighbor
        unvisited.remove(next)
        tour.append(next)
        current = next
    return tour

def two_opt(tour, i, k, W):
    n = len(tour) 
    a, b = tour[i-1], tour[i] # edges to be removed
    c, d = tour[k], tour[(k+1)%n] # edges to be removed
    before = W[a][b] + W[c][d] # cost before swap
    after = W[a][c] + W[b][d] # cost after swap
    return after - before # delta

def apply_two_opt(tour, i, k):
    tour[i:k+1] = reversed(tour[i:k+1]) # flips the segment

def solve_ls(W, cutoff, seed):
    random.seed(seed)
    t_end = time.time() + cutoff
    tour = _nn_init(W) # initial solution
    best = tour[:]
    best_cost = tour_cost(best, W)
    n = len(tour)

    improved = True
    # Local search with 2-opt
    while time.time() < t_end and improved:
        improved = False
        for i in range(1, n-1):
            for k in range(i+1, n-1):
                if time.time() >= t_end: 
                    break
                delta = two_opt(tour, i, k, W)
                if delta < 0: # if an improving move is found
                    apply_two_opt(tour, i, k)
                    improved = True
                    c = tour_cost(tour, W) # compute new cost
                    if c < best_cost: # update current best solution
                        best, best_cost = tour[:], c
                    break
            if improved or time.time() >= t_end:
                break
    return best, best_cost 

def solve_ls_multistart(W, cutoff, seed):
    random.seed(seed)
    t_end = time.time() + cutoff
    n = len(W)

    best_global_tour = None
    best_global_cost = np.inf

    while time.time() < t_end:
        tour = _nn_init(W)
        current_cost = tour_cost(tour, W)

        improved = True
        # standard 2-opt hill climbing from this start
        while time.time() < t_end and improved:
            improved = False
            for i in range(1, n-1):
                for k in range(i+1, n):
                    if time.time() >= t_end:
                        break
                    delta = two_opt(tour, i, k, W) # compute cost difference
                    if delta < 0:
                        apply_two_opt(tour, i, k) # apply the 2-opt move, only when delta < 0
                        current_cost += delta # update current cost
                        improved = True 
                        break 
                if improved or time.time() >= t_end:
                    break # after an improving move, restart scanning (first-improvement 2-opt)

        # update global best
        if current_cost < best_global_cost:
            best_global_tour = tour[:]
            best_global_cost = current_cost

    return best_global_tour, best_global_cost
