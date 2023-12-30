import tkinter as tk
from tkinter import filedialog, ttk
import zipfile
import os
from collections import deque

def browse_for_file_or_folder(entry):
    file_or_folder = filedialog.askopenfilename(
        title="Select a Zip File or Folder",
        filetypes=[("Zip files", "*.zip"), ("All files", "*.*")])
    
    if not file_or_folder:
        file_or_folder = filedialog.askdirectory(title="Select Folder")
    
    if file_or_folder:
        entry.set(file_or_folder)
        
def browse_for_output_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.set(folder)

def unzip_iteratively(source, target_dir):
    # Check if the source is a directory or a single file
    if os.path.isdir(source):
        # Unzip all zip files in the directory
        for file in os.listdir(source):
            file_path = os.path.join(source, file)
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
    elif zipfile.is_zipfile(source):
        # Unzip a single file
        with zipfile.ZipFile(source, 'r') as zip_ref:
            zip_ref.extractall(target_dir)

def select_source():
    source_path = source_entry.get()
    if not source_path:
        tk.messagebox.showerror("Error", "Please select a source file or directory.")
        return

    output_location = output_dir_location_entry.get()
    if not output_location:
        tk.messagebox.showerror("Error", "Please select an output directory location.")
        return

    output_dir_name = output_dir_entry.get()
    if not output_dir_name:
        tk.messagebox.showerror("Error", "Please enter a name for the output directory.")
        return

    target_dir = os.path.join(output_location, output_dir_name)
    os.makedirs(target_dir, exist_ok=True)

    # This section is where the change is needed
    if os.path.isfile(source_path) and zipfile.is_zipfile(source_path):
        unzip_iteratively(source_path, target_dir)
    elif os.path.isdir(source_path):
        for file in os.listdir(source_path):
            if zipfile.is_zipfile(os.path.join(source_path, file)):
                unzip_iteratively(os.path.join(source_path, file), target_dir)
    else:
        tk.messagebox.showerror("Error", "Selected file is not a zip or not a valid directory.")

    tk.messagebox.showinfo("Success", "Files have been unzipped successfully!")

root = tk.Tk()
root.title("Zip File Unzipper")
root.geometry("800x400")  # Set the standard size of the window

# Source file/folder selection
ttk.Label(root, text="Select Zip File or Folder:").pack(pady=5)
source_entry = tk.StringVar()
source_combo = ttk.Combobox(root, textvariable=source_entry)
source_combo.pack(pady=5)
ttk.Button(root, text="Browse", command=lambda: browse_for_file_or_folder(source_entry)).pack(pady=5)

# Output directory location selection
ttk.Label(root, text="Output Directory Location:").pack(pady=5)
output_dir_location_entry = tk.StringVar()
output_dir_location_combo = ttk.Combobox(root, textvariable=output_dir_location_entry)
output_dir_location_combo.pack(pady=5)
ttk.Button(root, text="Browse", command=lambda: browse_for_output_folder(output_dir_location_entry)).pack(pady=5)

# Output directory entry
ttk.Label(root, text="Output Directory Name:").pack(pady=5)
output_dir_entry = tk.StringVar()
output_dir_combo = ttk.Combobox(root, textvariable=output_dir_entry)
output_dir_combo.pack(pady=5)

# Select zip file and unzip button
select_button = ttk.Button(root, text="Unzip", command=select_source)
select_button.pack(pady=20)

root.mainloop()