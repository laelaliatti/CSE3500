import random
import time
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '.')
from convexhull import computeHull, naivehull

random.seed(42)

def avg_time(fn, points):
    start = time.time()
    fn(points)
    return time.time() - start

naive_sizes = [5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300, 400, 500, 650, 800, 1000, 1200, 1500, 2000, 3000, 5000]
dc_sizes    = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 75000, 100000, 150000, 200000, 500000, 750000, 1000000]

naive_times = []
for n in naive_sizes:
    pts = [(random.randint(0, 1000), random.randint(0, 800)) for _ in range(n)]
    naive_times.append(avg_time(naivehull, pts))

dc_times = []
for n in dc_sizes:
    pts = [(random.randint(0, 1000), random.randint(0, 800)) for _ in range(n)]
    dc_times.append(avg_time(computeHull, pts))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# naive -- linear both axes so cubic curve shape is visible
ax1.plot(naive_sizes, naive_times, 'o-', color='red', markersize=4)
ax1.set_title('naivehull  O(n³)')
ax1.set_xlabel('n')
ax1.set_ylabel('time (seconds)')
ax1.set_xscale('log')
ax1.grid(True, alpha=0.4)

# computeHull -- log x so the huge range fits, linear y so curve shape shows
ax2.plot(dc_sizes, dc_times, 's-', color='blue', markersize=4)
ax2.set_title('computeHull  O(n log n)')
ax2.set_xlabel('n')
ax2.set_ylabel('time (seconds)')
#ax2.set_xscale('log')
ax2.grid(True, which='both', alpha=0.4)

plt.tight_layout()
plt.savefig('benchmark_plots.png', dpi=150)
plt.show()
print("Saved benchmark_plots.png")