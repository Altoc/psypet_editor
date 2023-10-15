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
    def __init__(self, name_entry, description_entry):
        self.name_entry = name_entry
        self.description_entry = description_entry


# Custom class to represent a set of user-input on the MISSION portion of the editor
class MissionConditionEntry:
    def __init__(self, name_entry, mission_completer_check_var, mission_completer_entry, unlocked_conditions_id_entry, unlocked_world_states_id_entry):
        self.name_entry = name_entry
        self.mission_completer_check_var = mission_completer_check_var
        self.mission_completer_entry = mission_completer_entry
        #input into one field, comma separated, will be sorted by comma
        self.unlocked_conditions_id_entry = unlocked_conditions_id_entry
        #input into one field, comma separated, will be sorted by comma
        self.unlocked_world_states_id_entry = unlocked_world_states_id_entry


def open_mission_editor_window(root):
    def submit_record():
        nonlocal row_seq_id

        conn = db.connect_to_database()
        cursor = conn.cursor()

        # Create MISSION_mission record
        cursor.execute("SELECT MAX(mission_id) FROM MISSION_mission;")
        mission_id = int(cursor.fetchone()[0]) + 1
        cursor.execute("INSERT INTO MISSION_mission (mission_id, name, description) values (?, ?, ?)",
                       (mission_id, mission_entry.name_entry.get(), mission_entry.description_entry.get()))

        # Create MISSION_condition records
        cursor.execute("SELECT MAX(condition_id) FROM MISSION_condition;")
        condition_id = int(cursor.fetchone()[0])
        for input in condition_entry_widgets:
            condition_id += 1
            cursor.execute("INSERT INTO MISSION_condition (condition_id, mission_id, name, complete_mission_flag) values (?, ?, ?, ?)",
                           (condition_id, mission_id, input.name_entry.get(), input.mission_completer_check_var.get()))

        conn.commit()
        conn.close()

        mission_editor_window.destroy()

    def add_condition_entry():
        nonlocal row_seq_id
        row_seq_id += 7
        separator = ttk.Separator(mission_editor_window, orient="horizontal")

        mission_completer_check_var = tk.IntVar()
        condition_entry = MissionConditionEntry(ttk.Entry(mission_editor_window),
                                                mission_completer_check_var,
                                                ttk.Checkbutton(mission_editor_window, text="Completes Mission", variable=mission_completer_check_var),
                                                ttk.Entry(mission_editor_window),
                                                ttk.Entry(mission_editor_window))
        condition_entry_widgets.append(condition_entry)

        cond_id_label = ttk.Label(mission_editor_window, text="ID:")
        cond_id_value = ttk.Label(mission_editor_window, text="[ID HERE]")
        cond_name_label = ttk.Label(mission_editor_window, text="Cond Name:")
        prereq_ids_label = ttk.Label(mission_editor_window, text="Condition Unlocks:")
        world_state_ids_label = ttk.Label(mission_editor_window, text="World State Unlocks:")

        separator.grid(row=row_seq_id + 2, column=0, columnspan=10, sticky="ew")

        cond_id_label.grid(row=row_seq_id + 3, column=0, sticky=tk.E)
        cond_id_value.grid(row=row_seq_id + 3, column=1, sticky=tk.W)
        cond_name_label.grid(row=row_seq_id + 3, column=2, sticky=tk.E)
        prereq_ids_label.grid(row=row_seq_id + 4, column=2, sticky=tk.E)
        world_state_ids_label.grid(row=row_seq_id + 5, column=2, sticky=tk.E)

        condition_entry.name_entry.grid(row=row_seq_id + 3, column=3, sticky=tk.W)
        condition_entry.mission_completer_entry.grid(row=row_seq_id + 4, column=0)
        condition_entry.unlocked_conditions_id_entry.grid(row=row_seq_id + 4, column=3, sticky=tk.W)
        condition_entry.unlocked_world_states_id_entry.grid(row=row_seq_id + 5, column=3, sticky=tk.W)

        submit_button.grid(row=row_seq_id + 6, column=0, columnspan=2)
        add_cond_button.grid(row=row_seq_id + 6, column=3, columnspan=2)

    mission_editor_window = Toplevel(root)
    mission_editor_window.title("Psypet Mission Editor")
    row_seq_id = 0
    condition_entry_widgets = []  # List to store mission condition entry widgets

    # Widget Creation:

    mission_entry = MissionEntry(ttk.Entry(mission_editor_window),
                                 ttk.Entry(mission_editor_window))

    submit_button = ttk.Button(mission_editor_window, text="Submit", command=submit_record)
    add_cond_button = ttk.Button(mission_editor_window, text="Add Condition", command=add_condition_entry)
    mission_id_label = ttk.Label(mission_editor_window, text="ID:")
    mission_id_value = ttk.Label(mission_editor_window, text="[ID HERE]")
    mission_name_label = ttk.Label(mission_editor_window, text="Mission Name:")
    mission_descr_label = ttk.Label(mission_editor_window, text="Description:")
    separator = ttk.Separator(mission_editor_window, orient="horizontal")

    mission_completer_check_var = tk.IntVar()
    condition_entry = MissionConditionEntry(ttk.Entry(mission_editor_window),
                                            mission_completer_check_var,
                                            ttk.Checkbutton(mission_editor_window, text="Completes Mission", variable=mission_completer_check_var),
                                            ttk.Entry(mission_editor_window),
                                            ttk.Entry(mission_editor_window))
    condition_entry_widgets.append(condition_entry)

    cond_id_label = ttk.Label(mission_editor_window, text="ID:")
    cond_id_value = ttk.Label(mission_editor_window, text="[ID HERE]")
    cond_name_label = ttk.Label(mission_editor_window, text="Cond Name:")
    prereq_ids_label = ttk.Label(mission_editor_window, text="Condition Unlocks:")
    world_state_ids_label = ttk.Label(mission_editor_window, text="World State Unlocks:")

    # Widget Gridding:

    mission_id_label.grid(row=0, column=0, sticky=tk.E)
    mission_id_value.grid(row=0, column=1, sticky=tk.W)
    mission_name_label.grid(row=0, column=2, sticky=tk.E)
    mission_descr_label.grid(row=1, column=2, sticky=tk.E)

    mission_entry.name_entry.grid(row=0, column=3, sticky=tk.W)
    mission_entry.description_entry.grid(row=1, column=3, sticky=tk.W)

    separator.grid(row=2, column=0, columnspan=10, sticky="ew")

    cond_id_label.grid(row=3, column=0, sticky=tk.E)
    cond_id_value.grid(row=3, column=1, sticky=tk.W)
    cond_name_label.grid(row=3, column=2, sticky=tk.E)
    prereq_ids_label.grid(row=4, column=2, sticky=tk.E)
    world_state_ids_label.grid(row=5, column=2, sticky=tk.E)

    condition_entry.name_entry.grid(row=3, column=3, sticky=tk.W)
    condition_entry.mission_completer_entry.grid(row=4, column=0)
    condition_entry.unlocked_conditions_id_entry.grid(row=4, column=3, sticky=tk.W)
    condition_entry.unlocked_world_states_id_entry.grid(row=5, column=3, sticky=tk.W)

    submit_button.grid(row=6, column=0, columnspan=2)
    add_cond_button.grid(row=6, column=3, columnspan=2)
