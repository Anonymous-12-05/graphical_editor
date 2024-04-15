import tkinter as tk

class ObjectModifyWindow(tk.Toplevel):
    def __init__(self, parent, shape_id):
        super().__init__(parent)
        self.title("Modify Object")

        self.parent = parent
        self.shape_id = shape_id

        # Create a frame for modification options
        self.modify_frame = tk.Frame(self)
        self.modify_frame.pack(padx=10, pady=10)

        # Example: Entry field for changing color
        self.color_label = tk.Label(self.modify_frame, text="Color:")
        self.color_label.grid(row=0, column=0, sticky="w")
        self.color_entry = tk.Entry(self.modify_frame)
        self.color_entry.grid(row=0, column=1, padx=5, pady=5)

        # Button to apply modifications
        self.modify_button = tk.Button(self, text="Apply Modifications", command=self.apply_modifications)
        self.modify_button.pack(pady=5)

    def apply_modifications(self):
        # Get the color input from the entry field
        color = self.color_entry.get()
        # Apply the color modification to the selected shape
        self.parent.canvas.itemconfig(self.shape_id, fill=color)
        # Close the modification window
        self.destroy()
