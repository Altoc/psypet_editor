import tkinter as tk
from tkinter import ttk, Toplevel
import db_util as db


###--- DB CLASSES ---###

# Custom class to represent a MISSION_mission record
class Mission:
    def __init__(self, mission_id, name, description):
        self.mission_id = mission_id
        self.name = name
        self.description = description


# Custom class to represent a MISSION_condition record
class MissionCondition:
    def __init__(self, condition_id, mission_id, name, mission_completer_flag):
        self.condition_id = condition_id
        self.mission_id = mission_id
        self.name = name
        self.mission_completer_flag = mission_completer_flag


# Custom class to represent a MISSION_condition_prerequisite record
class MissionConditionPrerequisite:
    def __init__(self, condition_prereq_id, mission_id, prereq_of_id, prereq_to_id):
        self.condition_prereq_id = condition_prereq_id
        self.mission_id = mission_id
        self.prereq_of_id = prereq_of_id
        self.prereq_to_id = prereq_to_id


# Custom class to represent a MISSION_condition_world_state record
class MissionConditionWorldState:
    def __init__(self, condition_world_state_id, condition_entity_id, world_state_id, active_flag):
        self.condition_world_state_id = condition_world_state_id
        self.condition_entity_id = condition_entity_id
        self.world_state_id = world_state_id
        self.active_flag = active_flag


###--- TK UI CLASSES ---###

# Custom class to represent a set of user-input on the MISSION portion of the editor
class MissionEntry:
    def __init__(self, mission_id_entry, name_entry, description_entry):
        self.mission_id_entry = mission_id_entry
        self.name_entry = name_entry
        self.description_entry = description_entry


# Custom class to represent a set of user-input on the MISSION portion of the editor
class MissionConditionEntry:
    def __init__(self, mission_id_entry, name_entry, mission_completer_entry, unlocked_conditions_id_entry, unlocked_world_states_id_entry):
        self.mission_id_entry = mission_id_entry
        self.name_entry = name_entry
        self.mission_completer_entry = mission_completer_entry
        #input into one field, comma separated, will be sorted by comma
        self.unlocked_conditions_id_entry = unlocked_conditions_id_entry
        #input into one field, comma separated, will be sorted by comma
        self.unlocked_world_states_id_entry = unlocked_world_states_id_entry


def open_mission_editor_window(root):
    def submit_record():
        nonlocal sequence_id

        mission_editor_window.destroy()

    def add_condition_entry():
        nonlocal sequence_id
        sequence_id += 1
        # text_entry = DialogueEntry(ttk.Entry(insert_window),
        #                            ttk.Entry(insert_window),
        #                            ttk.Entry(insert_window),
        #                            ttk.Entry(insert_window),
        #                            ttk.Entry(insert_window),
        #                            ttk.Entry(insert_window),
        #                            ttk.Entry(insert_window))
        # text_entries.append(text_entry)
        #
        # seq_id_value = ttk.Label(insert_window, text=str(sequence_id))
        #
        # seq_id_value.grid(row=sequence_id + 1, column=0)
        # text_entry.text_entry.grid(row=sequence_id + 1, column=1)
        # text_entry.next_seq_entry.grid(row=sequence_id + 1, column=2)
        # text_entry.accept_seq_entry.grid(row=sequence_id + 1, column=3)
        # text_entry.decline_seq_entry.grid(row=sequence_id + 1, column=4)
        # text_entry.challenge_entry.grid(row=sequence_id + 1, column=5)
        # text_entry.mission_start_entry.grid(row=sequence_id + 1, column=6)
        # text_entry.mission_condition_update_entry.grid(row=sequence_id + 1, column=7)

        submit_button.grid(row=sequence_id + 3, column=0, columnspan=2)
        add_cond_button.grid(row=sequence_id + 3, column=3, columnspan=2)

    mission_editor_window = Toplevel(root)
    mission_editor_window.title("Psypet Mission Editor")
    # List to store DialogueLine objects
    dialogue_lines = []
    sequence_id = 0
    text_entries = []  # List to store text entry widgets

    # text_entry = DialogueEntry(ttk.Entry(insert_window),
    #                            ttk.Entry(insert_window),
    #                            ttk.Entry(insert_window),
    #                            ttk.Entry(insert_window),
    #                            ttk.Entry(insert_window),
    #                            ttk.Entry(insert_window),
    #                            ttk.Entry(insert_window))
    # text_entries.append(text_entry)

    # Widget Creation:

    submit_button = ttk.Button(mission_editor_window, text="Submit", command=submit_record)
    add_cond_button = ttk.Button(mission_editor_window, text="Add Condition", command=add_condition_entry)
    mission_id_label = ttk.Label(mission_editor_window, text="ID:")
    mission_id_value = ttk.Label(mission_editor_window, text="[ID HERE]")
    mission_name_label = ttk.Label(mission_editor_window, text="Mission Name:")
    mission_descr_label = ttk.Label(mission_editor_window, text="Description:")
    separator = ttk.Separator(mission_editor_window, orient="horizontal")

    cond_id_label = ttk.Label(mission_editor_window, text="ID:")
    cond_id_value = ttk.Label(mission_editor_window, text="[ID HERE]")
    cond_name_label = ttk.Label(mission_editor_window, text="Cond Name:")
    completer_checkbutton = ttk.Checkbutton(mission_editor_window, text="Completes Mission", command=lambda: print("Checkbutton clicked"))

    # Widget Gridding:

    submit_button.grid(row=5, column=0, columnspan=2)
    add_cond_button.grid(row=5, column=3, columnspan=2)
    mission_id_label.grid(row=0, column=0, sticky=tk.E)
    mission_id_value.grid(row=0, column=1, sticky=tk.W)
    mission_name_label.grid(row=0, column=2, sticky=tk.W)
    mission_descr_label.grid(row=1, column=2, sticky=tk.W)
    separator.grid(row=2, column=0, columnspan=10, sticky="ew")

    cond_id_label.grid(row=3, column=0, sticky=tk.E)
    cond_id_value.grid(row=3, column=1, sticky=tk.W)
    cond_name_label.grid(row=3, column=2, sticky=tk.W)
    completer_checkbutton.grid(row=4, column=0)
