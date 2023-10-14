import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import sqlite3


# Custom class to represent a dialogue line
class DialogueLine:
    def __init__(self, sequence_id, text):
        self.sequence_id = sequence_id
        self.text = text

# Function to connect to the SQLite database
def connect_to_database():
    conn = sqlite3.connect('D:\psypet_prototype\psypet\data\database.db')
    return conn

def retrieve_record():
    record_id = record_id_entry.get()
    conn = connect_to_database()
    cursor = conn.cursor()
    # Fetch the record from the SQLite database
    cursor.execute("SELECT * FROM your_table WHERE id=?", (record_id,))
    record = cursor.fetchone()
    conn.close()

    # Display the record in the text widget
    record_display.delete("1.0", tk.END)
    if record:
        record_display.insert(tk.END, f"ID: {record[0]}\nColumn1: {record[1]}\nColumn2: {record[2]}\n")

def save_record():
    conn = connect_to_database()
    cursor = conn.cursor()
    # Update the record in the SQLite database
    # You'll need to adapt this part to your specific database schema
    # Here's a sample update query:
    # cursor.execute("UPDATE your_table SET column1=?, column2=? WHERE id=?", (value1, value2, record_id))
    conn.commit()
    conn.close()


def open_insert_record_window():
    def submit_record():
        nonlocal sequence_id

        #retrieve next set_id
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(set_id) FROM DIALOGUE_dialogue_line;")
        set_id = int(cursor.fetchone()[0]) + 1
        conn.close()

        # Insert the record into the SQLite database
        conn = connect_to_database()
        cursor = conn.cursor()
        # You'll need to adapt this part to your specific database schema
        # Here's a sample insert query:
        for record in dialogue_lines:
            query = "INSERT INTO DIALOGUE_dialogue_line (set_id, seq_id, text) VALUES (?, ?, ?)" + str(set_id) + str(record.sequence_id) + str(record.text)
            cursor.execute("INSERT INTO DIALOGUE_dialogue_line (set_id, seq_id, text) VALUES (?, ?, ?)",
                           (set_id, record.sequence_id, record.text))
            print(query)
        conn.commit()
        conn.close()

    def add_text_entry():
        print("Adding entry")
        nonlocal sequence_id
        sequence_id += 1
        text_entry = ttk.Entry(insert_window)
        # Create a DialogueLine object and add it to the dialogue_lines list
        dialogue_line = DialogueLine(sequence_id, text_entries[-1])
        dialogue_lines.append(dialogue_line)
        text_entries.append(text_entry)

        for line, entry in zip(dialogue_lines, text_entries):
            line.text = entry.get()

        text_entry.grid(row=sequence_id, column=1)
        submit_button.grid(row=sequence_id + 2, column=0, columnspan=2)
        add_line_button.grid(row=sequence_id + 2, column=3, columnspan=2)

    insert_window = Toplevel(root)
    insert_window.title("Insert Record")
    # List to store DialogueLine objects
    dialogue_lines = []
    sequence_id = 0
    text_entries = []  # List to store text entry widgets

    text_label = ttk.Label(insert_window, text="Text:")
    text_entry = ttk.Entry(insert_window)
    text_entries.append(text_entry)
    submit_button = ttk.Button(insert_window, text="Submit", command=submit_record)
    add_line_button = ttk.Button(insert_window, text="Add Line", command=add_text_entry)

    text_label.grid(row=0, column=0, sticky=tk.W)
    text_entry.grid(row=0, column=1)
    submit_button.grid(row=2, column=0, columnspan=2)
    add_line_button.grid(row=2, column=3, columnspan=2)



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
retrieve_button = ttk.Button(main_frame, text="Retrieve Record", command=retrieve_record)
record_display = tk.Text(main_frame, height=10, width=40)
save_button = ttk.Button(main_frame, text="Save Record", command=save_record)

# Add a button to open the insert record window
insert_button = ttk.Button(main_frame, text="Insert Record", command=open_insert_record_window)

# Arrange widgets using the grid layout
record_id_label.grid(column=0, row=0, sticky=tk.W)
record_id_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
retrieve_button.grid(column=2, row=0, sticky=tk.W)
record_display.grid(column=0, row=1, columnspan=3)
save_button.grid(column=2, row=2, sticky=tk.E)
insert_button.grid(column=0, row=2, sticky=tk.W)

# Connect to the database on application startup
connect_to_database()

root.mainloop()
