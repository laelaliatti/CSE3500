#!/usr/bin/env python
# if using python 3, swap the next two lines
# from tkinter import *
from tkinter import *
import copy
from convexhull import computeHull
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

def hello(event):
    print("Single Click, Button-l") 

def addPoint(event):
	drawPoint(w, event.x, event.y)
	points.append((event.x,event.y))

def drawPoint(canvas,x,y):
	# r = 4
	# id = canvas.create_oval(x-r,y-r,x+r,y+r)
	id = canvas.create_image((x,y),image=ram,state=NORMAL)
	return id

def showPoints(event):
	print(points)

def drawHull():
	w.delete("hull")
	hull = copy.copy(computeHull(points))
	hull.append(hull[0])
	
	for i in range(0,len(hull)-1):
		x1 = hull[i][0]; y1 = hull[i][1]
		x2 = hull[i+1][0]; y2 = hull[i+1][1]
		w.create_line(x1, y1, x2, y2, width=3, tags="hull")


master = Tk()
points = []

submit_button = Button(master, text="Draw Hull", command=drawHull)
submit_button.pack()
quit_button = Button(master, text="Quit", command=master.quit)
quit_button.pack()

canvas_width = 1000
canvas_height = 800
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
ram = PhotoImage(file="oldhuski.png")
w.pack()
w.bind('<Button-1>', addPoint)

w.mainloop()