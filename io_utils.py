import math, os

# Utilities for reading TSP instances and saving solutions

def parse_tsplib(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f] # Read all lines in the file
        name = lines[0].split(":", 1)[1].strip() # Read the city name

    idx = 0
    while idx < len(lines):
        if lines[idx] == "NODE_COORD_SECTION":
            break
        idx +=1
    idx += 1 # Now idx is at the coordinates line
    coord = []
    while idx < len(lines): # Obtain all vertices IDs and x and y points
        if lines[idx] == "EOF":
            break
        col = lines[idx].split()
        vID = int(col[0])
        x = float(col[1])
        y = float(col[2])
        coord.append((vID, x, y))
        idx += 1
    ids = [vID for vID,_,_ in coord]
    pts = [(x,y) for _,x,y in coord]
    return name, ids, pts

def _euclid_round(p, q): # Calculate Euclidiean distance
    (x1,y1), (x2,y2) = p, q
    return int(round(math.hypot(x1 - x2, y1 - y2)))

def build_dist(pts):
    n = len(pts)
    W = [[0]*n for _ in range(n)] # W = n*n matrix with distance between points
    for i in range(n):
        for j in range(i+1, n):
            d = _euclid_round(pts[i], pts[j])
            W[i][j] = W[j][i] = d
    return W

def tour_cost(tour, W): # Calculate the cost of a given tour
    n = len(tour)
    s = 0
    for i in range(n-1):
        s += W[tour[i]][tour[i+1]]
    s += W[tour[-1]][tour[0]]
    return float(s)

def save_solution(instance_name, method, cutoff, seed, ids, tour, cost, time):
    city = instance_name # Get the city name
    parts = [city, method]
    if method == "BF":
        parts.append(str(0 if cutoff is None else cutoff))
    elif method == "Approx":
        if seed is not None:
            parts.append(str(seed))
    elif method == "LS" or method == "LS-multistart":
        parts.append(str(cutoff))
        parts.append(str(seed))
    fn = " ".join(parts) + ".sol"
    out_dir = str(method)
    os.makedirs(f"../Output/{out_dir}", exist_ok=True)

    filepath = os.path.join(f"../Output/{out_dir}", fn)

    node_order = [str(ids[i]) for i in tour]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{time}\n")
        f.write(f"{float(cost)}\n")
        f.write(", ".join(node_order) + "\n")

    print(f"[saved] {filepath}")