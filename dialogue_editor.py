import tkinter as tk
from tkinter import ttk, Toplevel
import db_util as db


# Custom class to represent a dialogue line
class DialogueLine:
    def __init__(self, sequence_id, text, next_seq_id, accept_seq_id, decline_seq_id, challenge_id, mission_start_id, mission_condition_update_id):
        self.sequence_id = sequence_id
        self.text = text if text != "" else None
        self.next_seq_id = next_seq_id if next_seq_id != "" else None
        self.accept_seq_id = accept_seq_id if accept_seq_id != "" else None
        self.decline_seq_id = decline_seq_id if decline_seq_id != "" else None
        self.challenge_id = challenge_id if challenge_id != "" else None
        self.mission_start_id = mission_start_id if mission_start_id != "" else None
        self.mission_condition_update_id = mission_condition_update_id if mission_condition_update_id != "" else None


# Custom class to represent a set of user-input on dialogue editor
class DialogueEntry:
    def __init__(self, entry, next_seq, accept_seq, decline_seq, challenge, mission_start, mission_condition_update):
        self.text_entry = entry
        self.next_seq_entry = next_seq
        self.accept_seq_entry = accept_seq
        self.decline_seq_entry = decline_seq
        self.challenge_entry = challenge
        self.mission_start_entry = mission_start
        self.mission_condition_update_entry = mission_condition_update


def open_dialogue_editor_window(root):
    def submit_record():
        nonlocal sequence_id

        #retrieve next set_id
        conn = db.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(set_id) FROM DIALOGUE_dialogue_line;")
        set_id = int(cursor.fetchone()[0]) + 1

        for index in range(len(text_entries)):
            dialogue_line = DialogueLine(index,
                                         text_entries[index].text_entry.get(),
                                         text_entries[index].next_seq_entry.get(),
                                         text_entries[index].accept_seq_entry.get(),
                                         text_entries[index].decline_seq_entry.get(),
                                         text_entries[index].challenge_entry.get(),
                                         text_entries[index].mission_start_entry.get(),
                                         text_entries[index].mission_condition_update_entry.get())
            dialogue_lines.append(dialogue_line)

        # You'll need to adapt this part to your specific database schema
        # Here's a sample insert query:
        for record in dialogue_lines:
            query = "INSERT INTO DIALOGUE_dialogue_line (set_id, seq_id, text) VALUES", str(set_id), str(record.sequence_id), str(record.text)
            cursor.execute("INSERT INTO DIALOGUE_dialogue_line (set_id, seq_id, next_seq_id, accept_next_seq_id, decline_next_seq_id, text, challenge_id, mission_start_id, mission_condition_update_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (set_id, record.sequence_id, record.next_seq_id, record.accept_seq_id, record.decline_seq_id, record.text, record.challenge_id, record.mission_start_id, record.mission_condition_update_id))
            print(query)
        conn.commit()
        conn.close()

        dialogue_editor_window.destroy()

    def add_dialogue_entry():
        nonlocal sequence_id
        sequence_id += 1
        text_entry = DialogueEntry(ttk.Entry(dialogue_editor_window),
                                   ttk.Entry(dialogue_editor_window),
                                   ttk.Entry(dialogue_editor_window),
                                   ttk.Entry(dialogue_editor_window),
                                   ttk.Entry(dialogue_editor_window),
                                   ttk.Entry(dialogue_editor_window),
                                   ttk.Entry(dialogue_editor_window))
        text_entries.append(text_entry)

        seq_id_value = ttk.Label(dialogue_editor_window, text=str(sequence_id))

        seq_id_value.grid(row=sequence_id + 1, column=0)
        text_entry.text_entry.grid(row=sequence_id + 1, column=1)
        text_entry.next_seq_entry.grid(row=sequence_id + 1, column=2)
        text_entry.accept_seq_entry.grid(row=sequence_id + 1, column=3)
        text_entry.decline_seq_entry.grid(row=sequence_id + 1, column=4)
        text_entry.challenge_entry.grid(row=sequence_id + 1, column=5)
        text_entry.mission_start_entry.grid(row=sequence_id + 1, column=6)
        text_entry.mission_condition_update_entry.grid(row=sequence_id + 1, column=7)

        submit_button.grid(row=sequence_id + 3, column=0, columnspan=2)
        add_line_button.grid(row=sequence_id + 3, column=3, columnspan=2)

    dialogue_editor_window = Toplevel(root)
    dialogue_editor_window.title("Psypet Dialogue Editor")
    # List to store DialogueLine objects
    dialogue_lines = []
    sequence_id = 0
    text_entries = []  # List to store text entry widgets

    text_entry = DialogueEntry(ttk.Entry(dialogue_editor_window),
                               ttk.Entry(dialogue_editor_window),
                               ttk.Entry(dialogue_editor_window),
                               ttk.Entry(dialogue_editor_window),
                               ttk.Entry(dialogue_editor_window),
                               ttk.Entry(dialogue_editor_window),
                               ttk.Entry(dialogue_editor_window))
    text_entries.append(text_entry)

    seq_id_label = ttk.Label(dialogue_editor_window, text="seq id:")
    seq_id_value = ttk.Label(dialogue_editor_window, text=str(sequence_id))
    text_label = ttk.Label(dialogue_editor_window, text="Text:")
    next_seq_label = ttk.Label(dialogue_editor_window, text="next seq id:")
    accept_seq_label = ttk.Label(dialogue_editor_window, text="accept seq id:")
    decline_seq_label = ttk.Label(dialogue_editor_window, text="decline seq id:")
    challenge_id_label = ttk.Label(dialogue_editor_window, text="challenge id:")
    mission_start_id_label = ttk.Label(dialogue_editor_window, text="mission start id:")
    mission_condition_update_id_label = ttk.Label(dialogue_editor_window, text="mission cond update id:")
    submit_button = ttk.Button(dialogue_editor_window, text="Submit", command=submit_record)
    add_line_button = ttk.Button(dialogue_editor_window, text="Add Line", command=add_dialogue_entry)

    seq_id_value.grid(row=sequence_id+1, column=0)
    text_entry.text_entry.grid(row=sequence_id+1, column=1)
    text_entry.next_seq_entry.grid(row=sequence_id+1, column=2)
    text_entry.accept_seq_entry.grid(row=sequence_id+1, column=3)
    text_entry.decline_seq_entry.grid(row=sequence_id+1, column=4)
    text_entry.challenge_entry.grid(row=sequence_id+1, column=5)
    text_entry.mission_start_entry.grid(row=sequence_id+1, column=6)
    text_entry.mission_condition_update_entry.grid(row=sequence_id+1, column=7)

    seq_id_label.grid(row=0, column=0, sticky=tk.W)
    text_label.grid(row=0, column=1, sticky=tk.W)
    next_seq_label.grid(row=0, column=2, sticky=tk.W)
    accept_seq_label.grid(row=0, column=3, sticky=tk.W)
    decline_seq_label.grid(row=0, column=4, sticky=tk.W)
    challenge_id_label.grid(row=0, column=5, sticky=tk.W)
    mission_start_id_label.grid(row=0, column=6, sticky=tk.W)
    mission_condition_update_id_label.grid(row=0, column=7, sticky=tk.W)

    submit_button.grid(row=sequence_id+3, column=0, columnspan=2)
    add_line_button.grid(row=sequence_id+3, column=3, columnspan=2)