import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import os
from datetime import datetime, timedelta
import re

# Data Setup
SAVE_FILE = 'study_tasks.csv'
if os.path.exists(SAVE_FILE):
    study_data = pd.read_csv(SAVE_FILE)
else:
    study_data = pd.DataFrame(columns=['Subject', 'Duration', 'Priority', 'Deadline'])

# Functions
def save_tasks():
    study_data.to_csv(SAVE_FILE, index=False)
    messagebox.showinfo("Info", "Tasks saved!")

def load_tasks():
    global study_data
    if os.path.exists(SAVE_FILE):
        study_data = pd.read_csv(SAVE_FILE)
        display_tasks()
        messagebox.showinfo("Info", "Tasks loaded!")
    else:
        messagebox.showwarning("Warning", "No tasks to load.")

def clear_tasks():
    global study_data
    study_data.drop(study_data.index, inplace=True)
    task_display.delete("1.0", tk.END)
    save_tasks()
    messagebox.showinfo("Info", "All tasks cleared!")

def add_task():
    global study_data
    subject = subject_entry.get().strip()
    duration = duration_entry.get().strip()
    priority = priority_entry.get().strip()
    deadline = deadline_entry.get().strip()

    # Validation
    if not subject or not duration or not priority:
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return

    if not re.match(r"^\d{1,2}:\d{2}$", duration):
        messagebox.showwarning("Warning", "Duration must be in HH:MM format.")
        return

    try:
        priority = int(priority)
        if not (1 <= priority <= 5):
            raise ValueError
    except ValueError:
        messagebox.showwarning("Warning", "Priority must be an integer between 1 and 5.")
        return

    # Append the new task to the DataFrame
    task = pd.DataFrame({
        'Subject': [subject],
        'Duration': [duration],
        'Priority': [priority],
        'Deadline': [deadline]
    })
    study_data = pd.concat([study_data, task], ignore_index=True)
    display_tasks()
    save_tasks()
    messagebox.showinfo("Info", "Task added!")
    clear_inputs()

def clear_inputs():
    subject_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

def display_tasks():
    task_display.delete("1.0", tk.END)
    for _, row in study_data.iterrows():
        task_info = (f"Subject: {row['Subject']}, Duration: {row['Duration']}, "
                     f"Priority: {row['Priority']}, Deadline: {row['Deadline']}\n")
        task_display.insert(tk.END, task_info)

def chat_response():
    user_input = chat_input.get().strip().lower()
    if not user_input:
        return

    response = ""
    if "suggest task" in user_input:
        response = "Try reviewing notes, working on high-priority tasks, or preparing summaries."
    elif "organize schedule" in user_input:
        response = "Start with high-priority tasks, allocate breaks, and adjust as needed."
    elif "study tips" in user_input:
        response = "Use the Pomodoro method: 25 mins study, 5 mins rest. Adjust to your needs."
    elif "break" in user_input:
        response = "Take breaks after each study hour; it helps refresh your mind."
    else:
        response = "To get suggestions, ask for 'task suggestions', 'schedule organization', or 'study tips'."

    chat_display.insert(tk.END, f"You: {user_input}\nAI: {response}\n\n")
    chat_input.delete(0, tk.END)

def generate_timetable():
    if study_data.empty:
        messagebox.showwarning("Warning", "No tasks available to generate a timetable.")
        return

    timetable_display = ""
    sorted_tasks = study_data.sort_values(by="Priority").reset_index(drop=True)
    current_time = datetime.now()

    for _, row in sorted_tasks.iterrows():
        try:
            # Parse duration in HH:MM format
            duration_parts = row['Duration'].split(":")
            duration = timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]))
        except (ValueError, IndexError):
            messagebox.showwarning("Warning", f"Invalid duration format for {row['Subject']}. Skipping task.")
            continue

        end_time = current_time + duration
        timetable_display += (f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: "
                              f"{row['Subject']} (Priority {row['Priority']})\n")
        current_time = end_time + timedelta(minutes=10)

    task_display.delete("1.0", tk.END)
    task_display.insert(tk.END, "Generated Timetable:\n" + timetable_display)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Smart Study Planner")
root.geometry("600x700")

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

tk.Button(root, text="Add Task", command=add_task, width=15).grid(row=4, column=0, pady=10)
tk.Button(root, text="Save Tasks", command=save_tasks, width=15).grid(row=4, column=1, pady=10)
tk.Button(root, text="Load Tasks", command=load_tasks, width=15).grid(row=5, column=0, pady=10)
tk.Button(root, text="Clear All Tasks", command=clear_tasks, width=15).grid(row=5, column=1, pady=10)
tk.Button(root, text="Generate Timetable", command=generate_timetable, width=30).grid(row=6, column=0, columnspan=2, pady=10)

task_display = tk.Text(root, height=10, width=70)
task_display.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="AI Suggestion Chatbox:").grid(row=8, column=0, columnspan=2, pady=10)
chat_display = scrolledtext.ScrolledText(root, height=8, width=70)
chat_display.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

chat_input = tk.Entry(root, width=50)
chat_input.grid(row=10, column=0, padx=10, pady=5)
tk.Button(root, text="Send", command=chat_response).grid(row=10, column=1, pady=5)

root.mainloop()
