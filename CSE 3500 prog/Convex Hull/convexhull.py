import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''

def naivehull(points):
	"""
	This will brute-force the hull for small inputs
	O(n^3)
	a p-q edge is only on the hull if and only if every other point lies on or left
	of the directed line
	
	for the initalization: absolute value of points <= base threshold, making it O(1)
	to know we're making progress, every directed pair is tested against all k.
	to know we're done, all n*(n-1) pairs are examined; and hull_set holds hull vertices.
	"""
	n = len(points)
	if n == 1:
		return points[:]
	set_hull = set()

	for i in range(n):
		for j in range(n):
			if i == j:
				continue
			p, q = points[i], points[j]
			on_hull = all( # checks if every item in the collection is true
				triangleArea(p, q, points[k]) >= -EPSILON #ignore tiny floating point errors. 
				for k in range(n) if k != i and k != j
			)
			if on_hull:
				set_hull.add(i)
				set_hull.add(j)
	result = [points[i] for i in set_hull]
	clockwiseSort(result)
	return result


def lowertangent(A,B):
	"""
	FInd the lower tangent of counterclockwise hulls A and B
	Canvas y increases downward, so "lower" means larger y.
	A and B are the inner most points of their respective hulls.
	a only decreases mod n a; b only increases mod n b, is how it's maintained
	loops terminate when both are tangent.

	"""
	a = max(range(len(A)), key=lambda i: A[i][0]) #find rightmost point in a
	b = min(range(len(B)), key=lambda i: B[i][0]) #find leftmost point in b
	lengtha = len(A)
	lenghtb = len(B)

	found = True
	while found:
		found = False
		while triangleArea(A[a], B[b], A[(a-1) % lengtha]) < -EPSILON:
			a = (a - 1) % lengtha
			found = True
		while triangleArea(A[a], B[b], B[(b+1) % lenghtb]) < -EPSILON:
			b = (b + 1) % lenghtb
			found = True
	return a, b


def uppertangent(A,B):
	#Symmetric to _lower_tangent: a moves CCW (+1), b moves CW (-1).

	a = max(range(len(A)), key=lambda i: A[i][0])
	b = min(range(len(B)), key=lambda i: B[i][0])
	lengtha = len(A)
	lenghtb = len(B)
	found = True
	while found:
		found = False
		while triangleArea(A[a], B[b], A[(a + 1) % lengtha]) > EPSILON:
			a = (a + 1) % lengtha
			found = True
		while triangleArea(A[a], B[b], B[(b - 1) % lenghtb]) > EPSILON:
			b = (b - 1) % lenghtb
			found = True
	return a, b

def stripCollinear(hull):
	# removes unnecessary collinear points from a convex hull.
    if len(hull) <= 2:
        return hull
    result = []
    n = len(hull)
    for i in range(n):
        a = hull[(i - 1) % n]
        b = hull[i]
        c = hull[(i + 1) % n]
        if abs(triangleArea(a, b, c)) > EPSILON:
            result.append(b)
    return result if result else hull
	
def mergehulls(A,B):
	"""
	merge 2 ccw hulls into a combined hull
	tangent indices are bridge endpoints
	each vertex is visited exactly once
	arc loop exits when idx reaches the far tangent point

	"""
	lengtha = len(A)
	lengthb = len(B)
	upper_a, upper_b = uppertangent(A, B)
	lower_a, lower_b = lowertangent(A, B)

	merged = []

	#CCW from lower a to upper a
	index = lower_a
	while True:
		merged.append(A[index])
		if index == upper_a:
			break
		index = (index + 1) % lengtha

	#CCW from upper_b to lower_b
	index = upper_b
	while True:
		merged.append(B[index])
		if index == lower_b:
			break
		index = (index + 1) % lengthb


	clockwiseSort(merged)
	return stripCollinear(merged)

base_threshold = 5

def computeHull(points):
	"""
	Divide and conquer Algorithm
	return hull points in cw order O(n log n)
	it sorts the points by x, a left half and a right half
	each recurse call gets smaller
	base case at |points| <= base_threshold
	"""
	points = list(set(points)) #removes exact duplicates
	n = len(points)

	if n <= base_threshold:
		return naivehull(points)
	
	points.sort(key= lambda p: (p[0], p[1])) #sort by x, break ties by y

	mid = n // 2
	# strip before merge
	left_hull  = stripCollinear(computeHull(points[:mid]))   
	right_hull = stripCollinear(computeHull(points[mid:]))   

	return mergehulls(left_hull[::-1], right_hull[::-1])



