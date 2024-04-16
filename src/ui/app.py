import tkinter as tk
import sys
import os
sys.path.append('../')  # Add the parent directory (src) to the Python path
from geometric import Circle, Rectangle, Line, Polygon, Text
import tkinter.simpledialog as simpledialog
import tkinter.colorchooser as colorchooser
from tkinter import filedialog
from PIL import Image, ImageGrab

class GraphicalEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphical Editor")

        # Create toolbar for selecting geometric object types
        self.create_toolbar()

        # Create canvas
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

        # List to store references to all shapes drawn on the canvas
        self.shapes = []

        # Variables to store mouse coordinates
        self.start_x = None
        self.start_y = None
        self.current_shape = None  # Reference to the current shape being drawn
        self.polygon_mode = False  # Flag to indicate if polygon mode is activated
        self.polygon_vertices = []  # List to store polygon vertices
        self.eraser_mode = False  # Flag to indicate if eraser mode is activated
        self.copy_shape_id = None  # ID of the shape to be copied

        # Bind right-click event to handle shape modification
        self.canvas.bind("<Button-3>", self.modify_shape)
        # Bind Ctrl+C to copy shape
        self.bind_all("<Control-c>", self.copy_shape)
        # Bind Ctrl+V to paste shape
        self.bind_all("<Control-v>", self.paste_shape)
        # Bind left mouse button click event to start moving object
        self.canvas.bind("<Button-1>", self.start_move)
        # Bind left mouse button release event to end moving object
        self.canvas.bind("<ButtonRelease-1>", self.end_move)

        # Add menu options for file operations
        self.create_file_menu()

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

        # Button for resizing
        resize_button = tk.Button(toolbar, text="Resize", command=self.use_eraser)
        resize_button.pack(side="left", padx=5, pady=5)

        

    def create_circle(self):
        # Bind mouse events to handle circle creation
        self.canvas.bind("<Button-1>", self.start_circle)
        self.canvas.bind("<B1-Motion>", self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>", self.end_circle)

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

    def end_circle(self, event):
        # Save the circle shape
        self.shapes.append(self.current_shape)
        self.current_shape = None

    def create_rectangle(self):
        # Bind mouse events to handle rectangle creation
        self.canvas.bind("<Button-1>", self.start_rectangle)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)

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

    def end_rectangle(self, event):
        # Save the rectangle shape
        self.shapes.append(self.current_shape)
        self.current_shape = None

    def create_line(self):
        # Bind mouse events to handle line creation
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

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

    def end_line(self, event):
        # Save the line shape
        self.shapes.append(self.current_shape)
        self.current_shape = None

    def create_text(self):
        # Bind mouse events to handle text creation
        self.canvas.bind("<Button-1>", self.place_text)

    def place_text(self, event):
        # Prompt the user for text input
        user_text = simpledialog.askstring("Input", "Enter text:")
        if user_text:
            # Create the text object
            text_id = self.canvas.create_text(event.x, event.y, text=user_text, fill="black")
            self.shapes.append(text_id)

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
        polygon_id = self.canvas.create_polygon(self.polygon_vertices, outline="black", fill="white")
        self.shapes.append(polygon_id)

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
            self.shapes.remove(obj)

    def modify_shape(self, event):
        # Find the shape under the mouse click
        clicked_objects = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if clicked_objects:
            clicked_shape_id = clicked_objects[-1]  # Get the topmost shape (last in the list)
            # Open modify window for the clicked shape
            self.open_modify_window(clicked_shape_id)
            # Bind left-click event for resizing
            self.canvas.tag_bind(clicked_shape_id, "<Button-1>", lambda event, shape_id=clicked_shape_id: self.resize_shape(event, shape_id))

    def open_modify_window(self, shape_id):
        # Placeholder for opening the modify window with color selection
        color_choice = colorchooser.askcolor(title="Choose Color")
        if color_choice[1]:  # Check if a color was chosen
            print(f"Shape {shape_id} modified with color: {color_choice[1]}")
            self.canvas.itemconfig(shape_id, fill=color_choice[1])  # Change shape color

    def resize_shape(self, event, shape_id):
        if isinstance(shape_id, int):  # Check if it's a valid shape ID
            shape_type = self.get_shape_type(shape_id)
            if shape_type == "circle":
                self.resize_circle(event, shape_id)
            elif shape_type == "rectangle":
                self.resize_rectangle(event, shape_id)
            elif shape_type == "line":
                self.resize_line(event, shape_id)
            # Add more conditions for other shape types as needed

    def get_shape_type(self, shape_id):
        if shape_id in self.shapes:
            if isinstance(shape_id, int):
                if isinstance(self.shapes[shape_id], Circle):
                    return "circle"
                elif isinstance(self.shapes[shape_id], Rectangle):
                    return "rectangle"
                elif isinstance(self.shapes[shape_id], Line):
                    return "line"
                # Add more conditions for other shape types as needed
        return None

    def resize_circle(self, event, shape_id):
        # Get the current coordinates of the circle
        bbox = self.canvas.bbox(shape_id)
        x1, y1, x2, y2 = bbox
        # Calculate the new radius based on mouse movement
        new_radius = ((event.x - x1) ** 2 + (event.y - y1) ** 2) ** 0.5
        # Update the circle with the new coordinates
        self.canvas.coords(shape_id, x1 - new_radius, y1 - new_radius, x1 + new_radius, y1 + new_radius)

    def resize_rectangle(self, event, shape_id):
        # Get the current coordinates of the rectangle
        bbox = self.canvas.bbox(shape_id)
        x1, y1, x2, y2 = bbox
        # Update the rectangle with the new coordinates
        self.canvas.coords(shape_id, x1, y1, event.x, event.y)

    def resize_line(self, event, shape_id):
        # Update the line with the new coordinates
        self.canvas.coords(shape_id, self.start_x, self.start_y, event.x, event.y)

    def copy_shape(self, event=None):
        # Check if a shape is selected
        if self.shapes:
            selected_shape_id = self.shapes[-1]  # Get the topmost shape (last in the list)
            self.copy_shape_id = selected_shape_id
            print(f"Shape {selected_shape_id} copied")

    def paste_shape(self, event=None):
        # Check if a shape is copied
        if self.copy_shape_id is not None:
            # Get the type of the copied shape
            copied_shape_type = self.get_shape_type(self.copy_shape_id)
            # Get the mouse cursor position
            x, y = self.canvas.winfo_pointerxy()
            x = self.canvas.canvasx(x)
            y = self.canvas.canvasy(y)
            if copied_shape_type == "circle":
                # Get the coordinates and radius of the copied circle
                x1, y1, x2, y2 = self.canvas.coords(self.copy_shape_id)
                radius = (x2 - x1) / 2
                # Create a new circle with the same properties at the mouse cursor position
                new_circle_id = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black")
                self.shapes.append(new_circle_id)
            elif copied_shape_type == "rectangle":
                # Get the coordinates of the copied rectangle
                x1, y1, x2, y2 = self.canvas.coords(self.copy_shape_id)
                # Create a new rectangle with the same properties at the mouse cursor position
                new_rectangle_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                self.shapes.append(new_rectangle_id)
            elif copied_shape_type == "line":
                # Get the coordinates of the copied line
                x1, y1, x2, y2 = self.canvas.coords(self.copy_shape_id)
                # Create a new line with the same properties at the mouse cursor position
                new_line_id = self.canvas.create_line(x1, y1, x2, y2, fill="black")
                self.shapes.append(new_line_id)
            # Add support for other shape types as needed

    def start_move(self, event):
        # Find the shape under the mouse click
        clicked_objects = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if clicked_objects:
            clicked_shape_id = clicked_objects[-1]  # Get the topmost shape (last in the list)
            self.current_shape = clicked_shape_id
            bbox = self.canvas.bbox(clicked_shape_id)
            self.start_x, self.start_y = event.x - bbox[0], event.y - bbox[1]

    def end_move(self, event):
        self.current_shape = None

    def move_shape(self, event):
        if self.current_shape:
            # Calculate the new coordinates based on mouse movement
            x, y = event.x - self.start_x, event.y - self.start_y
            # Move the shape to the new coordinates
            self.canvas.coords(self.current_shape, x, y)
    def create_file_menu(self):
        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Delete", command=self.delete_file)

    def save_file(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                        filetypes=(("JPEG files", "*.jpg"), 
                                                   ("PNG files", "*.png"),
                                                   ("GIF files", "*.gif"),
                                                   ("BMP files", "*.bmp")))

        if filename:
            x = self.winfo_x()
            y = self.winfo_y()
            im = ImageGrab.grab(bbox=(x + 91, y + 31, x + 891, y + 653))  # Screenshot canvas area
            im.save(filename)
            print("File saved successfully.")

    def open_file(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                        filetypes=(("JPEG files", "*.jpg"), 
                                                   ("PNG files", "*.png"),
                                                   ("GIF files", "*.gif"),
                                                   ("BMP files", "*.bmp")))

        if filename:
            imgtemp = Image.open(filename)
            if imgtemp.size[0] > 800 or imgtemp.size[1] > 600:  # if image is larger than 800x600, resize
                imgtemp = imgtemp.resize((800, 600), Image.ANTIALIAS)
            imgtemp.save("Temp.gif", "gif")
            self.file_to_open = tk.PhotoImage(file="Temp.gif")  # reference to image, otherwise will be lost to garbage collection
            self.canvas.delete("all")  # clear canvas beforehand
            self.canvas.create_image(3, 3, image=self.file_to_open, anchor=tk.NW)  # image must be anchored to be centered on screen
            print("File opened successfully.")

    def delete_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"),
                                                         ("gif files", "*.gif"), ("bmp files", "*.bmp")))
        if filename:
            try:
                os.remove(filename)
                print("File deleted successfully.")
            except FileNotFoundError:
                print("File not found.")

def run():
    app = GraphicalEditorApp()
    app.mainloop()

if __name__ == "__main__":
    run()
