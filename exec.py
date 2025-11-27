import argparse, sys, time
from io_utils import parse_tsplib, build_dist, save_solution
from alg_bf import solve_bf
from alg_approx import solve_approx
from alg_ls import solve_ls, solve_ls_multistart

# Main execution function

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("-inst", dest="filename", required=True)
    ap.add_argument("-alg", dest="algorithm", required=True, choices=["BF","Approx","LS", "LS-multistart"])
    ap.add_argument("-time", dest="time_cutoff", type=float, default=None)
    ap.add_argument("-seed", dest="random_seed", type=int, default=None)
    ap.add_argument("-help", dest="help", action="store_true")
    args, _ = ap.parse_known_args()
    if args.help:
        print("Usage: -inst <file> -alg <BF|Approx|LS> -time <sec> -seed <seed>")
        sys.exit(0)
    instance, ids, pts = parse_tsplib(args.filename)
    W = build_dist(pts)
    t0 = time.perf_counter()
    if args.algorithm == "BF":
        if args.time_cutoff is None:
            print("ERROR: BF needs -time", file=sys.stderr)
            sys.exit(2)
        tour, cost = solve_bf(W, cutoff=args.time_cutoff)
        out_cutoff = args.time_cutoff
        out_seed = None
    elif args.algorithm == "Approx":
        tour, cost = solve_approx(W)
        out_cutoff = None
        out_seed = None
    elif args.algorithm == "LS":
        if args.time_cutoff is None or args.random_seed is None:
            print("ERROR: LS needs -time and -seed", file=sys.stderr)
            sys.exit(2)
        tour, cost = solve_ls(W, cutoff=args.time_cutoff, seed=args.random_seed)
        out_cutoff = args.time_cutoff
        out_seed = args.random_seed
    elif args.algorithm == "LS-multistart":
        if args.time_cutoff is None or args.random_seed is None:
            print("ERROR: LS-multistart needs -time and -seed", file=sys.stderr)
            sys.exit(2)
        tour, cost = solve_ls_multistart(W, cutoff=args.time_cutoff, seed=args.random_seed)
        out_cutoff = args.time_cutoff
        out_seed = args.random_seed
    elapsed = time.perf_counter() - t0
    save_solution(instance_name=instance, method=args.algorithm, cutoff=out_cutoff, seed=out_seed, ids=ids, tour=tour, cost=cost, time = repr(elapsed))
    print(f"[{args.algorithm}] instance={instance} cost={cost:.0f} time={repr(elapsed)}s tour_len={len(tour)}")

if __name__ == "__main__":
    main()