import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Data and Save File
study_data = pd.DataFrame(columns=['Subject', 'Duration', 'Priority', 'Deadline'])
SAVE_FILE = 'study_tasks.csv'
if not os.path.exists(SAVE_FILE):
    study_data.to_csv(SAVE_FILE, index=False)

def save_tasks():
    study_data.to_csv(SAVE_FILE, index=False)
    messagebox.showinfo("Info", "Tasks saved!")

def load_tasks():
    global study_data
    study_data = pd.read_csv(SAVE_FILE)
    messagebox.showinfo("Info", "Tasks loaded!")

def clear_tasks():
    global study_data
    study_data.drop(study_data.index, inplace=True)
    messagebox.showwarning("Info", "All tasks cleared!")

def add_task():
    global study_data
    task = {
        'Subject': subject_entry.get(),
        'Duration': duration_entry.get(),
        'Priority': priority_entry.get(),
        'Deadline': deadline_entry.get()
    }
    study_data = study_data.append(task, ignore_index=True)
    messagebox.showinfo("Info", "Task added!")
    clear_inputs()

def clear_inputs():
    subject_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

# Tkinter setup
root = tk.Tk()
root.title("Smart Study Planner")
root.geometry("500x400")

# Task Inputs
tk.Label(root, text="Subject:").grid(row=0, column=0, padx=10, pady=5)
subject_entry = tk.Entry(root)
subject_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Duration (HH:MM):").grid(row=1, column=0, padx=10, pady=5)
duration_entry = tk.Entry(root)
duration_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Priority (1-5):").grid(row=2, column=0, padx=10, pady=5)
priority_entry = tk.Entry(root)
priority_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Deadline (e.g., Monday):").grid(row=3, column=0, padx=10, pady=5)
deadline_entry = tk.Entry(root)
deadline_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Task", command=add_task, width=15).grid(row=4, column=0, pady=10)
tk.Button(root, text="Save Tasks", command=save_tasks, width=15).grid(row=4, column=1, pady=10)
tk.Button(root, text="Load Tasks", command=load_tasks, width=15).grid(row=5, column=0, pady=10)
tk.Button(root, text="Clear All Tasks", command=clear_tasks, width=15).grid(row=5, column=1, pady=10)

root.mainloop()

