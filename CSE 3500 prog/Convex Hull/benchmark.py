import random
import time
from convexhull import computeHull, naivehull

sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]

print(f"{'n':>10}  {'naiveHull (s)':>15}  {'computeHull (s)':>16}")
print("-" * 45)

for n in sizes:
    points = [(random.randint(0, 1000), random.randint(0, 800)) for _ in range(n)]

    # Benchmark naiveHull (skip for large n it's O(n^3))
    if n <= 1000:
        start = time.time()
        naivehull(points)
        naive_time = time.time() - start
        naive_str = f"{naive_time:.6f}"
    else:
        naive_str = "too slow"

    # Benchmark computeHull
    start = time.time()
    computeHull(points)
    dc_time = time.time() - start

    print(f"{n:>10}  {naive_str:>15}  {dc_time:>16.6f}")