import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from dialogue_editor import open_dialogue_editor_window
from mission_editor import open_mission_editor_window


# Create the main application window
root = tk.Tk()
root.title("SQLite Database Editor")

# Create and configure the main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

# Create widgets (labels, text inputs, buttons) to interact with the database
record_id_label = ttk.Label(main_frame, text="Record ID:")
record_id_entry = ttk.Entry(main_frame)
record_display = tk.Text(main_frame, height=10, width=40)

# Add a button to open the Dialogue Editor window
dialogue_editor_button = ttk.Button(main_frame, text="Dialogue Editor", command=lambda: open_dialogue_editor_window(root))

# Add a button to open the Mission Editor window
mission_editor_button = ttk.Button(main_frame, text="Mission Editor", command=lambda: open_mission_editor_window(root))

# Arrange widgets using the grid layout
record_id_label.grid(column=0, row=0, sticky=tk.W)
record_id_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
record_display.grid(column=0, row=1, columnspan=3)
dialogue_editor_button.grid(column=0, row=2, sticky=tk.W)
mission_editor_button.grid(column=0, row=3, sticky=tk.W)

root.mainloop()
