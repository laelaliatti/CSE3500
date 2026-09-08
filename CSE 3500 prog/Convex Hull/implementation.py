import math
import sys

EPSILON = sys.float_info.epsilon

# ── [keep all the existing helper functions unchanged] ──────────────────────
# yint, triangleArea, cw, ccw, collinear, clockwiseSort  (no changes needed)

def yint(p1, p2, x, y3, y4):
    x1, y1 = p1
    x2, y2 = p2
    x3 = x4 = x
    px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)) / \
         float((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)) / \
         float((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    return (px, py)

def triangleArea(a, b, c):
    return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0]
            - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0

def cw(a, b, c):
    return triangleArea(a, b, c) < EPSILON

def ccw(a, b, c):
    return triangleArea(a, b, c) > EPSILON

def collinear(a, b, c):
    return abs(triangleArea(a, b, c)) <= EPSILON

def clockwiseSort(points):
    xavg = sum(p[0] for p in points) / len(points)
    yavg = sum(p[1] for p in points) / len(points)
    angle = lambda p: ((math.atan2(p[1]-yavg, p[0]-xavg) + 2*math.pi) % (2*math.pi))
    points.sort(key=angle)


# ── BASE CASE ────────────────────────────────────────────────────────────────

def naiveHull(points):
    """
    O(n^3) brute-force hull for small inputs.

    An edge p->q is on the hull iff every other point lies to the LEFT of
    (or on) the directed line p->q, i.e. triangleArea(p, q, r) >= 0.

    Invariants
    ----------
    Init        : |points| <= BASE_THRESHOLD, so O(n^3) is O(1).
    Maintenance : every directed pair (i,j) is tested against all k.
    Termination : all n*(n-1) pairs examined; hull_set holds hull vertices.
    """
    n = len(points)
    if n <= 2:
        return list(points)

    hull_set = set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            p, q = points[i], points[j]
            on_hull = all(
                triangleArea(p, q, points[k]) >= -EPSILON
                for k in range(n) if k != i and k != j
            )
            if on_hull:
                hull_set.add(i)
                hull_set.add(j)

    result = [points[i] for i in hull_set]
    clockwiseSort(result)
    return result


# ── MERGE HELPERS ────────────────────────────────────────────────────────────

def _lower_tangent(A, B):
    """
    Find the lower tangent of CCW hulls A (left) and B (right).

    Canvas y increases downward, so "lower" means larger y.
    Start: a = rightmost of A, b = leftmost of B.
    Walk:  a clockwise (index-1), b counter-clockwise (index+1).

    T = A[a]->B[b] is a lower tangent at a when A[a-1] is NOT below T,
    i.e. triangleArea(A[a], B[b], A[a-1]) >= 0.  Symmetric for b.

    Invariants
    ----------
    Init        : a, b are the innermost points of their respective hulls.
    Maintenance : a only decreases mod n_a; b only increases mod n_b
                  (Lemma 3.8.2 — segment never enters a hull interior).
    Termination : indices bounded; loops terminate when both are tangent.
    """
    a = max(range(len(A)), key=lambda i: A[i][0])
    b = min(range(len(B)), key=lambda i: B[i][0])
    n_a, n_b = len(A), len(B)

    changed = True
    while changed:
        changed = False
        while triangleArea(A[a], B[b], A[(a-1) % n_a]) < -EPSILON:
            a = (a - 1) % n_a
            changed = True
        while triangleArea(A[a], B[b], B[(b+1) % n_b]) < -EPSILON:
            b = (b + 1) % n_b
            changed = True
    return a, b


def _upper_tangent(A, B):
    """
    Find the upper tangent of CCW hulls A (left) and B (right).

    Symmetric to _lower_tangent: a moves CCW (+1), b moves CW (-1).

    Invariants
    ----------
    Init        : a = rightmost of A, b = leftmost of B.
    Maintenance : a only increases mod n_a; b only decreases mod n_b.
    Termination : same bounding argument as lower tangent.
    """
    a = max(range(len(A)), key=lambda i: A[i][0])
    b = min(range(len(B)), key=lambda i: B[i][0])
    n_a, n_b = len(A), len(B)

    changed = True
    while changed:
        changed = False
        while triangleArea(A[a], B[b], A[(a+1) % n_a]) > EPSILON:
            a = (a + 1) % n_a
            changed = True
        while triangleArea(A[a], B[b], B[(b-1) % n_b]) > EPSILON:
            b = (b - 1) % n_b
            changed = True
    return a, b


def _merge(A, B):
    """
    Merge two CCW hulls A (left) and B (right) into their combined hull.

    1. Compute upper tangent (upper_a, upper_b) and lower tangent (lower_a, lower_b).
    2. Trace the merged boundary (CCW):
         - Upper arc of A: upper_a  →  lower_a  (CCW = +1 each step)
         - Lower arc of B: lower_b  →  upper_b  (CCW = +1 each step)
    3. clockwiseSort converts the result to CW for computeHull's contract.

    Invariants
    ----------
    Init        : tangent indices are valid bridge endpoints.
    Maintenance : each vertex visited exactly once; index advances by +1.
    Termination : arc loop exits when idx reaches the far tangent point.
    """
    n_a, n_b = len(A), len(B)
    upper_a, upper_b = _upper_tangent(A, B)
    lower_a, lower_b = _lower_tangent(A, B)

    merged = []

    # Upper arc of A (CCW from upper_a to lower_a)
    idx = upper_a
    while True:
        merged.append(A[idx])
        if idx == lower_a:
            break
        idx = (idx + 1) % n_a

    # Lower arc of B (CCW from lower_b to upper_b)
    idx = lower_b
    while True:
        merged.append(B[idx])
        if idx == upper_b:
            break
        idx = (idx + 1) % n_b

    clockwiseSort(merged)
    return merged


# ── MAIN ENTRY POINT ─────────────────────────────────────────────────────────

BASE_THRESHOLD = 3

def computeHull(points):
    """
    Divide-and-conquer convex hull (Preparata & Hong 1977).
    Returns hull points in clockwise order.

    Time complexity: O(n log n)  [T(n) = 2T(n/2) + O(n), Master Theorem case 2]

    Invariants
    ----------
    Init        : points sorted by x; left half x-values < right half x-values.
    Maintenance : each recursive call gets a strictly smaller list (size < n),
                  so stack depth is O(log n).
    Termination : base case at |points| <= BASE_THRESHOLD handled by naiveHull.
    """
    points = list(set(points))          # remove exact duplicates
    n = len(points)

    if n <= BASE_THRESHOLD:
        return naiveHull(points)

    points.sort(key=lambda p: (p[0], p[1]))   # sort by x, break ties by y

    mid = n // 2
    left_hull  = computeHull(points[:mid])
    right_hull = computeHull(points[mid:])

    # computeHull returns CW; _merge expects CCW — reverse each
    return _merge(left_hull[::-1], right_hull[::-1])