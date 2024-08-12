import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def get_size(path):
    """Return the total size of the folder specified by path."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except FileNotFoundError:
                pass
    return total_size

def format_size(size):
    """Format the size in bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def list_subfolders_and_sizes(path):
    """List all subfolders and their sizes."""
    subfolders_sizes = {}
    
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            folder_size = get_size(entry_path)
            subfolders_sizes[entry] = folder_size
    
    # Sort by size in descending order
    sorted_subfolders = sorted(subfolders_sizes.items(), key=lambda x: x[1], reverse=True)
    return sorted_subfolders

def display_single_folder_size():
    """Open a folder dialog and display the size of a single folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        try:
            folder_size = get_size(folder_path)
            formatted_size = format_size(folder_size)
            messagebox.showinfo("Folder Size", f"Size of '{os.path.basename(folder_path)}': {formatted_size}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def display_subfolders_sizes():
    """Open a folder dialog and display sizes of subfolders."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        try:
            subfolders_sizes = list_subfolders_and_sizes(folder_path)
            if subfolders_sizes:
                # Clear the treeview
                for item in tree.get_children():
                    tree.delete(item)
                
                # Insert data into the treeview
                for idx, (folder, size) in enumerate(subfolders_sizes, start=1):
                    tree.insert("", "end", values=(idx, folder, format_size(size)))
            else:
                messagebox.showinfo("Info", f"No subfolders found in '{folder_path}'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create main application window
app = tk.Tk()
app.title("Folder Size Viewer")

# Create and place widgets
browse_subfolders_button = tk.Button(app, text="Browse Folder for Subfolders", command=display_subfolders_sizes)
browse_subfolders_button.pack(pady=10)

browse_single_folder_button = tk.Button(app, text="Browse Single Folder", command=display_single_folder_size)
browse_single_folder_button.pack(pady=10)

# Create and configure treeview
columns = ("#1", "#2", "#3")
tree = ttk.Treeview(app, columns=columns, show="headings")
tree.heading("#1", text="Sr. No.")
tree.heading("#2", text="Folder Name")
tree.heading("#3", text="Size")

tree.column("#1", width=50, anchor=tk.CENTER)
tree.column("#2", width=200, anchor=tk.W)
tree.column("#3", width=150, anchor=tk.W)

tree.pack(padx=10, pady=10)

# Start the Tkinter event loop
app.mainloop()
