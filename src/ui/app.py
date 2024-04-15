import tkinter as tk
import sys
sys.path.append('../')  # Add the parent directory (src) to the Python path
from geometric import Circle, Rectangle, Line, Polygon, Text
import tkinter.simpledialog as simpledialog

class GraphicalEditorApp(tk.Tk):
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
        self.polygon_mode = False  # Flag to indicate if polygon mode is activated
        self.polygon_vertices = []  # List to store polygon vertices
        self.eraser_mode = False  # Flag to indicate if eraser mode is activated

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

        # Button for creating polygons
        polygon_button = tk.Button(toolbar, text="Polygon", command=self.activate_polygon_mode)
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

    def activate_polygon_mode(self):
        # Reset polygon mode and vertices list
        self.polygon_mode = True
        self.polygon_vertices = []
        # Bind mouse events to handle polygon creation
        self.canvas.bind("<Button-1>", self.start_polygon)

    def start_polygon(self, event):
        # If polygon mode is activated, record the polygon vertices
        if self.polygon_mode:
            self.polygon_vertices.append((event.x, event.y))
            # Draw a line if there are multiple vertices
            if len(self.polygon_vertices) > 1:
                prev_x, prev_y = self.polygon_vertices[-2]
                self.canvas.create_line(prev_x, prev_y, event.x, event.y, fill="black")
            # Draw the final polygon when the user clicks near the first vertex
            if len(self.polygon_vertices) > 2 and self.is_close_to_first_vertex(event.x, event.y):
                self.draw_polygon()
                self.polygon_mode = False

    def is_close_to_first_vertex(self, x, y):
        # Check if the current mouse position is close to the first vertex
        first_x, first_y = self.polygon_vertices[0]
        return abs(x - first_x) < 5 and abs(y - first_y) < 5

    def draw_polygon(self):
        # Draw the final polygon
        self.canvas.create_polygon(self.polygon_vertices, outline="black", fill="white")

    def use_eraser(self):
        # Toggle eraser mode
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            # Bind mouse events to handle erasing
            self.canvas.bind("<Button-1>", self.erase_object)

    def erase_object(self, event):
        # Find objects overlapping with the mouse click and delete them
        objects = self.canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)
        for obj in objects:
            self.canvas.delete(obj)

def run():
    app = GraphicalEditorApp()
    app.mainloop()

if __name__ == "__main__":
    run()
