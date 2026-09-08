# Benchmarking seam carving with and without dynamic programming
# This assumes you already have ResizeableImage implemented
# and image files available in the same directory.
import os
print(os.getcwd())
import time
import matplotlib.pyplot as plt
import imagematrix
from resizeable_image import ResizeableImage  # adjust if your file name differs

# List of images to test (adjust filenames as needed)
image_files = [
    "sunset_small.png",
    # Add more resized versions like:
    # "sunset_50.png",
    # "sunset_100.png",
    # "sunset_150.png",
]

sizes = []
dp_times = []
naive_times = []

for filename in image_files:
    img = ResizeableImage(filename)
    sizes.append(img.width * img.height)  # total number of pixels as size measure
    
    # ---- Time DP version ----
    start = time.perf_counter()
    img.best_seam(dp=True)
    end = time.perf_counter()
    dp_times.append(end - start)
    
    # ---- Time Naive version ----
    start = time.perf_counter()
    img.best_seam(dp=False)
    end = time.perf_counter()
    naive_times.append(end - start)

# ---- Plot results ----
plt.figure()
plt.plot(sizes, dp_times)
plt.plot(sizes, naive_times)
plt.xlabel("Image Size (Total Pixels)")
plt.ylabel("Running Time (seconds)")
plt.title("Seam Carving: DP vs Naive Running Time")
plt.show()
