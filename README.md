# CSE 6140 Final Project  
**Seungjun Cha, Jimin Park, Soomin Lim**

## Overview
This repository contains the implementation and evaluation of three algorithms for the Traveling Salesman Problem (TSP): a depth-first brute force search with pruning, a minimum spanning tree (MST)–based approximation, and a 2-opt local search with a multi-start variant. The objective is to compare their performance in terms of solution quality, runtime efficiency, and sensitivity to cutoff times. All experiments were executed on the provided city datasets, and the total tour cost was used as the primary evaluation metric.

## Algorithms

### Brute Force Search  
The brute force algorithm performs a depth-first search over all possible tours. It prunes any partial path whose accumulated cost exceeds the best solution found so far. A nearest-neighbor–constructed tour is used to initialize the upper bound, and a predefined time cutoff ensures termination. Although exponential in the number of cities, this method can solve small instances optimally within the cutoff window.

### Minimum Spanning Tree Approximation  
This approximation method constructs a minimum spanning tree using Prim’s algorithm and generates a Hamiltonian tour through a preorder depth-first traversal of the tree. The resulting tour satisfies the classical 2-approximation bound for metric TSP instances. This method is computationally efficient and completes nearly instantaneously for all datasets.

### 2-opt Local Search (Single-Start and Multi-Start)  
The 2-opt local search begins with a tour generated via a nearest-neighbor heuristic with a random starting city. It then performs first-improvement 2-opt moves, scanning for the earliest edge swap that decreases the total tour cost. When an improving swap is found, it is immediately applied, and the search continues until no further improvement is possible or the time cutoff is reached.

For part (c), a multi-start variant was implemented. New random initial tours are repeatedly generated, and 2-opt hill climbing is applied to each one within the remaining time. This approach allows the search to escape local minima and improves the probability of finding near-optimal solutions within the cutoff.

## Experimental Results

### Summary  
Across all datasets, the local search method significantly outperformed the brute force and approximation algorithms in both solution quality and runtime. While brute force was able to reach optimal solutions for very small instances, it frequently timed out on larger datasets. The MST approximation consistently produced feasible tours but with noticeably higher cost. The 10-run average costs from 2-opt were consistently superior to the MST results, and the minimum cost across all 2-opt runs was the best overall solution for every dataset.

### Tables  
Complete numerical results, including runtime, best tour cost, and relative error, are provided in the report tables for all three algorithms. The relative error for each city is computed with respect to the lowest tour cost found across all local search runs.

## Cutoff Time Analysis  
To study the relationship between cutoff time and solution quality, multi-start 2-opt was executed with eight time limits: 0.1, 1, 3, 5, 10, 30, 60, and 120 seconds. For each cutoff, 10 independent runs were performed. Average tour cost decreased rapidly as the cutoff increased, with all runs converging to the same tour by approximately the 10-second mark. No further improvements were observed beyond that point.

## Files  
This repository includes:
- Implementations of all three algorithms  
- Scripts for running experiments under varying cutoff times  
- Output logs and tables for performance comparison  
- The final project report containing analysis and discussion  

## References  
Course materials and standard algorithmic references for TSP, MST construction, and local search heuristics.

