import random
import os, glob, subprocess

# BF
# for f in glob.glob("../DATA/*.tsp"):
#     subprocess.run(f"python exec.py -inst {f} -alg BF -time 600", shell=True)

# # Approx
# for f in glob.glob("../DATA/*.tsp"):
#     subprocess.run(f"python exec.py -inst {f} -alg Approx", shell=True)

# LS
# for f in glob.glob("../DATA/*.tsp"):
#     for n in range(1, 11):
#         subprocess.run(f"python exec.py -inst {f} -alg LS -time 60 -seed {n}", shell=True)

# LS-multistart
for t in [0.1, 1, 3, 5, 10, 30, 60, 120]:
    for i in range(10):
        subprocess.run(f"python exec.py -inst \"../DATA/Toronto.tsp\" -alg LS-multistart -time {t} -seed {random.randint(1, 100)}", shell=True)