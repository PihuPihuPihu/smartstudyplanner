import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
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
    update_task_listbox()
    save_tasks()
    messagebox.showinfo("Info", "All tasks cleared!")

def delete_task():
    global study_data
    selection = task_listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        return
    
    index = selection[0]
    study_data.drop(index, inplace=True)
    study_data.reset_index(drop=True, inplace=True)
    display_tasks()
    update_task_listbox()
    save_tasks()
    messagebox.showinfo("Info", "Task deleted!")

def update_task_listbox():
    task_listbox.delete(0, tk.END)
    for _, row in study_data.iterrows():
        task_info = f"{row['Subject']} - {row['Duration']} (Priority: {row['Priority']})"
        task_listbox.insert(tk.END, task_info)

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

    # Append the new task
    task = pd.DataFrame({
        'Subject': [subject],
        'Duration': [duration],
        'Priority': [priority],
        'Deadline': [deadline]
    })
    study_data = pd.concat([study_data, task], ignore_index=True)
    display_tasks()
    update_task_listbox()
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

def parse_duration(duration_str):
    try:
        hours, minutes = map(int, duration_str.split(":"))
        return timedelta(hours=hours, minutes=minutes)
    except ValueError:
        return None

def chat_response():
    user_input = chat_input.get().strip().lower()
    if not user_input:
        return

    responses = {
        "suggest task": "Try reviewing notes, working on high-priority tasks, or preparing summaries.",
        "organize schedule": "Start with high-priority tasks, allocate breaks, and adjust as needed.",
        "study tips": "Use the Pomodoro method: 25 mins study, 5 mins rest. Adjust to your needs.",
        "break": "Take regular breaks: 15 minutes after each hour of study helps maintain focus.",
        "motivation": "Remember your goals! Each study session brings you closer to success.",
        "focus": "Try the 5-4-3-2-1 grounding technique or meditation before studying.",
        "help": "You can ask about: 'suggest task', 'organize schedule', 'study tips', 'break', 'motivation', or 'focus'."
    }

    response = responses.get(user_input, "To get suggestions, try asking about 'task suggestions', 'schedule organization', 'study tips', 'breaks', 'motivation', or 'focus'.")
    
    chat_display.insert(tk.END, f"You: {user_input}\nAI: {response}\n\n")
    chat_display.see(tk.END)
    chat_input.delete(0, tk.END)

def generate_timetable():
    if study_data.empty:
        messagebox.showwarning("Warning", "No tasks available to generate a timetable.")
        return

    timetable_display = ""
    sorted_tasks = study_data.sort_values(by="Priority").reset_index(drop=True)
    current_time = datetime.now()
    accumulated_study_time = timedelta()

    for _, row in sorted_tasks.iterrows():
        duration = parse_duration(row['Duration'])
        if not duration:
            messagebox.showwarning("Warning", f"Invalid duration format for {row['Subject']}. Skipping task.")
            continue

        # Check if we need a break (after each hour of accumulated study time)
        if accumulated_study_time >= timedelta(hours=1):
            # Add 15-minute break
            break_end_time = current_time + timedelta(minutes=15)
            timetable_display += f"\n{current_time.strftime('%H:%M')} - {break_end_time.strftime('%H:%M')}: "
            timetable_display += "*** BREAK TIME ***\n\n"
            current_time = break_end_time
            accumulated_study_time = timedelta()

        # Add the task
        end_time = current_time + duration
        timetable_display += (f"{current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: "
                            f"{row['Subject']} (Priority {row['Priority']})\n")
        
        current_time = end_time
        accumulated_study_time += duration

    task_display.delete("1.0", tk.END)
    task_display.insert(tk.END, "Generated Timetable:\n" + timetable_display)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Smart Study Planner")
root.geometry("800x800")

# Input Frame
input_frame = ttk.LabelFrame(root, text="Add New Task", padding="10")
input_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(input_frame, text="Subject:").grid(row=0, column=0, padx=5, pady=5)
subject_entry = ttk.Entry(input_frame)
subject_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Duration (HH:MM):").grid(row=0, column=2, padx=5, pady=5)
duration_entry = ttk.Entry(input_frame)
duration_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(input_frame, text="Priority (1-5):").grid(row=1, column=0, padx=5, pady=5)
priority_entry = ttk.Entry(input_frame)
priority_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Deadline:").grid(row=1, column=2, padx=5, pady=5)
deadline_entry = ttk.Entry(input_frame)
deadline_entry.grid(row=1, column=3, padx=5, pady=5)

# Buttons Frame
button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(button_frame, text="Add Task", command=add_task).pack(side="left", padx=5)
ttk.Button(button_frame, text="Save Tasks", command=save_tasks).pack(side="left", padx=5)
ttk.Button(button_frame, text="Load Tasks", command=load_tasks).pack(side="left", padx=5)
ttk.Button(button_frame, text="Clear All Tasks", command=clear_tasks).pack(side="left", padx=5)
ttk.Button(button_frame, text="Generate Timetable", command=generate_timetable).pack(side="left", padx=5)

# Task List Frame
task_list_frame = ttk.LabelFrame(root, text="Task List", padding="10")
task_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

task_listbox = tk.Listbox(task_list_frame, height=6)
task_listbox.pack(fill="both", expand=True)
ttk.Button(task_list_frame, text="Delete Selected Task", command=delete_task).pack(pady=5)

# Display Frame
display_frame = ttk.LabelFrame(root, text="Timetable Display", padding="10")
display_frame.pack(fill="both", expand=True, padx=10, pady=5)

task_display = tk.Text(display_frame, height=10)
task_display.pack(fill="both", expand=True)

# Chat Frame
chat_frame = ttk.LabelFrame(root, text="AI Study Assistant", padding="10")
chat_frame.pack(fill="both", expand=True, padx=10, pady=5)

chat_display = scrolledtext.ScrolledText(chat_frame, height=8)
chat_display.pack(fill="both", expand=True)

chat_input_frame = ttk.Frame(chat_frame)
chat_input_frame.pack(fill="x", pady=5)

chat_input = ttk.Entry(chat_input_frame)
chat_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
ttk.Button(chat_input_frame, text="Send", command=chat_response).pack(side="right")

root.mainloop()
