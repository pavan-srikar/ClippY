import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

def load_fields_from_json(json_path):
    """Load fields from a JSON file."""
    if not os.path.exists(json_path):
        return None
    with open(json_path, "r") as file:
        return json.load(file)

def copy_to_clipboard(text):
    """Copy text to clipboard."""
    root.clipboard_clear()
    root.clipboard_append(text)

# Main application
root = tk.Tk()
root.title("Clippy - Job Application Helper")

# Set an initial height and allow dynamic width
root.geometry("1x600")  # 1 pixel width to let it auto-resize based on content
root.resizable(True, False)  # Allow resizing horizontally only

# Path to JSON file in the same folder as this script
base_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(base_dir, "data.json")

# Load fields
fields = load_fields_from_json(json_file)

# If JSON file is not found, use file picker
if fields is None:
    messagebox.showwarning("File Not Found", "No JSON file found in the folder. Please select a JSON file.")
    json_file = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")])
    if not json_file:  # If no file is selected, exit
        messagebox.showerror("Error", "No JSON file selected. Exiting application.")
        root.destroy()
        exit()
    else:
        fields = load_fields_from_json(json_file)
        if fields is None:  # If selected file is invalid, exit
            messagebox.showerror("Error", "Invalid JSON file. Exiting application.")
            root.destroy()
            exit()

# Scrollbar setup
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create GUI fields
row = 0
for field, data in fields.items():
    field_type = data["type"]
    default_value = data["value"]

    label = tk.Label(frame, text=field, anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    if field_type == 2:  # Multi-line text input
        text_box = tk.Text(frame, wrap=tk.WORD, height=5, width=40)
        text_box.insert("1.0", default_value)
        text_box.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        copy_button = tk.Button(frame, text="Copy", command=lambda t=text_box: copy_to_clipboard(t.get("1.0", tk.END).strip()))
        copy_button.grid(row=row + 1, column=2, padx=10, pady=5, sticky="e")
    elif field_type == 1:  # Single-line text input
        entry = tk.Entry(frame)
        entry.insert(0, default_value)
        entry.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        copy_button = tk.Button(frame, text="Copy", command=lambda e=entry: copy_to_clipboard(e.get()))
        copy_button.grid(row=row + 1, column=2, padx=10, pady=5, sticky="e")

    row += 2  # Increment for next field

    # Update window size dynamically
root.update_idletasks()  # Calculate correct dimensions after all widgets are placed
root.geometry(f"{frame.winfo_reqwidth()+20}x600")  # Set dynamic width and fixed height

root.mainloop()
