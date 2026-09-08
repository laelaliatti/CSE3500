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
	points.sort(key = angle, reverse = True)

def right_most(points):
	#find the rightmost index
	#only call after clockwise sorted
	right = 0
	a = len(points)
	found = False
	while not found:
		found = True
		if points[right][0] < points[(right + 1) % a][0]:
			right = (right + 1) % a
			found = False
		elif points[right][0] < points[right - 1][0]:
			right = (right - 1 + a) % a
			found = False
	return right
	
def left_most(points):
	#find the leftmost index
	#only call after clockwise sorted

	left = 0
	b = len(points)
	found = False
	while not found:
		found = True
		if points[left][0] > points[(left + 1) % b][0]:
			left = (left + 1) % b
			found = False
		elif points[left][0] > points[left - 1][0]:
			left = (left - 1 + b) % b
			found = False
	return left
	

def find_upper_tan(points_a, points_b, left, right):
	#takes in two hulls and the extremes of those, returns a top tangent line in the form of the 2 idecies that make it up
	right_tan = right
	left_tan = left
	
	a = len(points_a)
	b = len(points_b)

	found = True

	while found:
		found = False
		while ccw(points_a[right_tan], points_b[left_tan], points_b[(left_tan + 1) % b]):
			#checks if three points make ccw cycle, if they do move b until cw
			left_tan = (left_tan + 1) % b
			found = True

		while cw(points_b[left_tan], points_a[right_tan], points_a[(right_tan - 1 + a) % a]):
			#checks if 3 points make a cw cycle, if they do move a until ccw
			right_tan = (right_tan - 1 + a) % a
			found = True

		
	
	return right_tan, left_tan

def find_lower_tan(points_a, points_b, left, right):
	#takes in two hulls and the extremes of those, returns a bottom tangent line in the form of the 2 idecies that make it up
	right_tan = right
	left_tan = left
	
	a = len(points_a)
	b = len(points_b)

	found = True

	while found:
		found = False
		while cw(points_a[right_tan], points_b[left_tan], points_b[(left_tan - 1 + b) % b]):
			#checks if 3 points make a cw cycle, if they do move b until ccw
			left_tan = (left_tan - 1 + b) % b
			found = True

		while ccw(points_b[left_tan], points_a[right_tan], points_a[(right_tan + 1) % a]):
			#checks if 3 points make a ccw cycle, if they do move a until cw
			right_tan = (right_tan + 1) % a
			found = True

	return right_tan, left_tan


def naive_hull(points):
	#brute forces a hull, used for small inputs
	if len(points) == 2:
		#trivial
		return points[:]
	in_hull = set()
	#iterates through all points, tripply nested, to test every possible line segment to see if its part of the hull
	for i in points:
		for j in points:
			if i is j:
				continue
			truth_value = None
			found = True
			for k in points:
				if i is k: continue
				if truth_value is None:
					truth_value = cw(i, j, k)
				elif cw(i, j, k) != truth_value:
					found = False
					break
			if found == True:
				in_hull.add(i)
				in_hull.add(j)

	hull_points = list(in_hull)
	# clockwiseSort(final_points) //gave a counterclockwise orientation somehow
	# had to do more

	#finds the furthest left points (extreme)
	start = min(hull_points, key=lambda p: p[0])
	hull = [start]
	current = start
	
	while True:
		#iterates through adding points combination if they're clockwise oriented, if not it doesn't. Iterates through all points forcing them into clockwise orientation
		next_point = None
		for p in hull_points:
			if p is current:
				continue
			if next_point is None or cw(current, next_point, p):
				next_point = p
		if next_point == start:
			break
		hull.append(next_point)
		current = next_point


	clockwiseSort(hull) #sort of a just in case kind of thing, betrayed me before
	return hull



'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(points):
	#take in a list of points, divide and conquer
	points_a = []
	points_b = []
	points_len = len(points)
	if len(points) > 4:
		#base case, divide based on left-right location
		points.sort()
		points_a = computeHull(points[:points_len//2])
		points_b = computeHull(points[points_len//2:])

	else:
		#everything not base case, split further
		final_points = naive_hull(points)
		return(final_points)
	
	#find the top tangent and bottom tangent lines, and cooresponding points

	right = right_most(points_a)
	left = left_most(points_b)

	top_tan_a, top_tan_b = find_upper_tan(points_a, points_b, left, right)
	bottom_tan_a, bottom_tan_b = find_lower_tan(points_a, points_b, left, right)

	#walk the points, produced a clockwise oriented convex hull based on two clockwise oriented convex hulls

	final_points = []

	i = bottom_tan_a
	final_points.append(points_a[i])
	while i != top_tan_a:
		i = (i + 1) % len(points_a)
		final_points.append(points_a[i])

	i = top_tan_b
	final_points.append(points_b[i])
	while i != bottom_tan_b:
		i = (i + 1) % len(points_b)
		final_points.append(points_b[i])

	clockwiseSort(final_points)

	return final_points
