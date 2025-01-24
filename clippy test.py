import tkinter as tk
import os
import json


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

# Scrollbar setup
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


# Load fields from JSON file
def load_fields_from_json(json_path):
    """Load fields from JSON file."""
    if not os.path.exists(json_path):
        return None
    with open(json_path, "r") as file:
        return json.load(file)


# Attempt to load the JSON file
fields = load_fields_from_json("data.json")
if fields is None:
    from tkinter import filedialog, messagebox

    messagebox.showwarning("File Not Found", "No JSON file found. Please select one.")
    json_file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not json_file:
        messagebox.showerror("Error", "No JSON file selected. Exiting application.")
        root.destroy()
        exit()
    fields = load_fields_from_json(json_file)


# Create fields in the GUI
row = 0
for field, data in fields.items():
    field_type = data["type"]
    default_value = data["value"]

    # Create label for the field
    label = tk.Label(frame, text=field, anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    # Multi-line text input
    if field_type == 2:
        text_box = tk.Text(frame, wrap=tk.WORD, height=5, width=40)
        text_box.insert("1.0", default_value)
        text_box.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        copy_button = tk.Button(
            frame, text="Copy", command=lambda t=text_box: copy_to_clipboard(t.get("1.0", tk.END).strip())
        )
        copy_button.grid(row=row + 1, column=2, padx=10, pady=5, sticky="e")

    # Single-line text input
    elif field_type == 1:
        entry = tk.Entry(frame)
        entry.insert(0, default_value)
        entry.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        copy_button = tk.Button(
            frame, text="Copy", command=lambda e=entry: copy_to_clipboard(e.get())
        )
        copy_button.grid(row=row + 1, column=2, padx=10, pady=5, sticky="e")

    row += 2

# Update window size dynamically
root.update_idletasks()  # Calculate correct dimensions after all widgets are placed
root.geometry(f"{frame.winfo_reqwidth()}x600")  # Set dynamic width and fixed height

root.mainloop()
