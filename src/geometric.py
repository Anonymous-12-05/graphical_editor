# src/geometric.py

import tkinter as tk
import tkinter.simpledialog as simpledialog

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, canvas):
        # Draw a circle on the canvas
        canvas.create_oval(self.x - self.radius, self.y - self.radius, 
                           self.x + self.radius, self.y + self.radius, 
                           outline="black", width=2)

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        # Draw a rectangle on the canvas
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline="black", width=2)

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        # Draw a line on the canvas
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="black", width=2)

# src/geometric.py

class Polygon:
    def __init__(self, canvas):
        self.canvas = canvas
        self.vertices = []
        self.polygon = None

    def start_drawing(self):
        self.canvas.bind("<Button-1>", self.add_vertex)
        self.canvas.bind("<B1-Motion>", self.adjust_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def add_vertex(self, event):
        self.vertices.extend([event.x, event.y])
        if self.polygon:
            self.canvas.delete(self.polygon)
        self.polygon = self.canvas.create_polygon(self.vertices, outline="black", width=2)

    def adjust_polygon(self, event):
        if len(self.vertices) >= 2:
            self.vertices[-2] = event.x
            self.vertices[-1] = event.y
            self.canvas.coords(self.polygon, self.vertices)

    def end_drawing(self, event):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")


class Text:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, canvas):
        # Draw text on the canvas
        canvas.create_text(self.x, self.y, text=self.text, fill="black")
