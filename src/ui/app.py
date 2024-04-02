# src/ui/app.py

import tkinter as tk
import sys
sys.path.append('../')  # Add the parent directory (src) to the Python path
from geometric import Circle, Rectangle, Line

class GraphicalEditorApp(tk.Tk):  # Inherit from tkinter.Tk
    def __init__(self):
        super().__init__()
        self.title("Graphical Editor")

        # Create toolbar for selecting geometric object types
        self.create_toolbar()

        # Create canvas
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        # Variables to store mouse coordinates
        self.start_x = None
        self.start_y = None
        self.current_shape = None  # Reference to the current shape being drawn

    def create_toolbar(self):
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")

        # Button for creating circles
        circle_button = tk.Button(toolbar, text="Circle", command=self.create_circle)
        circle_button.pack(side="left", padx=5, pady=5)

        # Button for creating rectangles
        rectangle_button = tk.Button(toolbar, text="Rectangle", command=self.create_rectangle)
        rectangle_button.pack(side="left", padx=5, pady=5)

        # Button for creating lines
        line_button = tk.Button(toolbar, text="Line", command=self.create_line)
        line_button.pack(side="left", padx=5, pady=5)

        # Button for creating ellipses
        ellipse_button = tk.Button(toolbar, text="Ellipse", command=self.create_ellipse)
        ellipse_button.pack(side="left", padx=5, pady=5)

        # Button for creating polygons
        polygon_button = tk.Button(toolbar, text="Polygon", command=self.create_polygon)
        polygon_button.pack(side="left", padx=5, pady=5)

        # Button for creating text
        text_button = tk.Button(toolbar, text="Text", command=self.create_text)
        text_button.pack(side="left", padx=5, pady=5)

        # Button for using eraser
        eraser_button = tk.Button(toolbar, text="Eraser", command=self.use_eraser)
        eraser_button.pack(side="left", padx=5, pady=5)

    def create_circle(self):
        # Bind mouse events to handle circle creation
        self.canvas.bind("<Button-1>", self.start_circle)
        self.canvas.bind("<B1-Motion>", self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def start_circle(self, event):
        # Record starting point of circle creation
        self.start_x = event.x
        self.start_y = event.y

    def draw_circle(self, event):
        # Delete the previous shape
        if self.current_shape:
            self.canvas.delete(self.current_shape)

        # Calculate radius based on mouse movement
        radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
        # Draw the circle
        self.current_shape = self.canvas.create_oval(self.start_x - radius, self.start_y - radius,
                                                      self.start_x + radius, self.start_y + radius,
                                                      outline="black")

    def create_rectangle(self):
        # Bind mouse events to handle rectangle creation
        self.canvas.bind("<Button-1>", self.start_rectangle)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def start_rectangle(self, event):
        # Record starting point of rectangle creation
        self.start_x = event.x
        self.start_y = event.y

    def draw_rectangle(self, event):
        # Delete the previous shape
        if self.current_shape:
            self.canvas.delete(self.current_shape)

        # Draw the rectangle
        self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y,
                                                          event.x, event.y,
                                                          outline="black")

    def create_line(self):
        # Bind mouse events to handle line creation
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def start_line(self, event):
        # Record starting point of line creation
        self.start_x = event.x
        self.start_y = event.y

    def draw_line(self, event):
        # Delete the previous shape
        if self.current_shape:
            self.canvas.delete(self.current_shape)

        # Draw the line
        self.current_shape = self.canvas.create_line(self.start_x, self.start_y,
                                                      event.x, event.y,
                                                      fill="black")

    def create_ellipse(self):
        # Bind mouse events to handle ellipse creation
        self.canvas.bind("<Button-1>", self.start_ellipse)
        self.canvas.bind("<B1-Motion>", self.draw_ellipse)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def start_ellipse(self, event):
        # Record starting point of ellipse creation
        self.start_x = event.x
        self.start_y = event.y

    def draw_ellipse(self, event):
        # Delete the previous shape
        if self.current_shape:
            self.canvas.delete(self.current_shape)

        # Draw the ellipse
        self.current_shape = self.canvas.create_oval(self.start_x, self.start_y,
                                                     event.x, event.y,
                                                     outline="black")

    def create_polygon(self):
        # Bind mouse events to handle polygon creation
        self.canvas.bind("<Button-1>", self.start_polygon)
        self.canvas.bind("<B1-Motion>", self.draw_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def start_polygon(self, event):
        # Record starting point of polygon creation
        self.start_x = event.x
        self.start_y = event.y
        # Initialize the list of polygon vertices
        self.polygon_vertices = [self.start_x, self.start_y]

    def draw_polygon(self, event):
        # Add the current point to the polygon vertices
        self.polygon_vertices.extend([event.x, event.y])
        # Delete the previous shape
        if self.current_shape:
            self.canvas.delete(self.current_shape)
        # Draw the polygon
        self.current_shape = self.canvas.create_polygon(self.polygon_vertices,
                                                        outline="black")

    def create_text(self):
        # Bind mouse events to handle text creation
        self.canvas.bind("<Button-1>", self.place_text)

    def place_text(self, event):
        # Prompt the user for text input
        user_text = tk.simpledialog.askstring("Input", "Enter text:")
        if user_text:
            # Create the text object
            self.canvas.create_text(event.x, event.y, text=user_text, fill="black")

    def end_shape(self, event):
        # Reset the current shape reference
        self.current_shape = None

    def use_eraser(self):
        # Bind mouse events to handle eraser
        self.canvas.bind("<Button-1>", self.erase_shape)

    def erase_shape(self, event):
        # Find the item closest to the mouse click
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            # Delete the shape
            self.canvas.delete(item)

def run():
    app = GraphicalEditorApp()
    app.mainloop()

if __name__ == "__main__":
    run()
