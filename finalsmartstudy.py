import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import pandas as pd
import os
from datetime import datetime, timedelta
import re

# Color Scheme
COLORS = {
    'primary': '#2E4057',     # Dark blue
    'secondary': '#048BA8',   # Teal
    'accent': '#16DB93',      # Mint green
    'warning': '#EFEA5A',     # Yellow
    'error': '#F29E4C',       # Orange
    'background': '#F4F7F5',  # Light gray
    'text': '#2E4057',        # Dark blue
    'white': '#FFFFFF'        # White
}

# Custom Style Setup
def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')  # Use clam theme as base
    
    # Configure main window
    style.configure('.',
                   background=COLORS['background'],
                   foreground=COLORS['text'],
                   font=('Helvetica', 10))
    
    # Configure Frames
    style.configure('Custom.TLabelframe',
                   background=COLORS['background'],
                   padding=10)
    style.configure('Custom.TLabelframe.Label',
                   background=COLORS['background'],
                   foreground=COLORS['primary'],
                   font=('Helvetica', 11, 'bold'))
    
    # Configure Buttons
    style.configure('Primary.TButton',
                   background=COLORS['primary'],
                   foreground=COLORS['white'],
                   padding=(10, 5),
                   font=('Helvetica', 10))
    style.map('Primary.TButton',
              background=[('active', COLORS['secondary'])])
    
    # Configure Labels
    style.configure('Custom.TLabel',
                   background=COLORS['background'],
                   foreground=COLORS['text'],
                   font=('Helvetica', 10))
    
    # Configure Entry fields
    style.configure('Custom.TEntry',
                   fieldbackground=COLORS['white'],
                   padding=5)

# Data Setup
SAVE_FILE = 'study_tasks.csv'
if os.path.exists(SAVE_FILE):
    study_data = pd.read_csv(SAVE_FILE)
else:
    study_data = pd.DataFrame(columns=['Subject', 'Duration', 'Priority', 'Deadline'])

# Define missing functions
def add_task():
    subject = subject_entry.get()
    duration = duration_entry.get()
    priority = priority_entry.get()
    deadline = deadline_entry.get()
    
    if subject and duration and priority and deadline:
        # Add task to the DataFrame
        study_data.loc[len(study_data)] = [subject, duration, priority, deadline]
        task_listbox.insert(tk.END, f"{subject} - {duration} - Priority: {priority} - Deadline: {deadline}")
        clear_entries()
    else:
        messagebox.showerror("Input Error", "Please fill in all fields.")

def save_tasks():
    study_data.to_csv(SAVE_FILE, index=False)
    messagebox.showinfo("Save Successful", "Tasks saved successfully.")

def load_tasks():
    task_listbox.delete(0, tk.END)
    if os.path.exists(SAVE_FILE):
        global study_data
        study_data = pd.read_csv(SAVE_FILE)
        for index, row in study_data.iterrows():
            task_listbox.insert(tk.END, f"{row['Subject']} - {row['Duration']} - Priority: {row['Priority']} - Deadline: {row['Deadline']}")

def clear_tasks():
    global study_data
    study_data = pd.DataFrame(columns=['Subject', 'Duration', 'Priority', 'Deadline'])
    task_listbox.delete(0, tk.END)
    messagebox.showinfo("Clear Successful", "All tasks cleared.")

def delete_task():
    try:
        selected_task = task_listbox.curselection()
        if selected_task:
            task_listbox.delete(selected_task)
            study_data.drop(study_data.index[selected_task[0]], inplace=True)
    except Exception as e:
        messagebox.showerror("Deletion Error", str(e))

def generate_timetable():
    task_display.delete(1.0, tk.END)
    timetable = "Generated timetable (to be implemented)"
    task_display.insert(tk.END, timetable)

def chat_response():
    user_input = chat_input.get()
    chat_display.insert(tk.END, f"\nYou: {user_input}")
    response = "AI Response Placeholder (to be implemented)"
    chat_display.insert(tk.END, f"\nAssistant: {response}")
    chat_input.delete(0, tk.END)

def clear_entries():
    subject_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Smart Study Planner")
root.geometry("800x800")
root.configure(bg=COLORS['background'])

# Apply custom styles
setup_styles()

# Input Frame
input_frame = ttk.LabelFrame(root, text="Add New Task", style='Custom.TLabelframe')
input_frame.pack(fill="x", padx=10, pady=5)

# Labels and Entries with custom styles
ttk.Label(input_frame, text="Subject:", style='Custom.TLabel').grid(row=0, column=0, padx=5, pady=5)
subject_entry = ttk.Entry(input_frame, style='Custom.TEntry')
subject_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Duration (HH:MM):", style='Custom.TLabel').grid(row=0, column=2, padx=5, pady=5)
duration_entry = ttk.Entry(input_frame, style='Custom.TEntry')
duration_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(input_frame, text="Priority (1-5):", style='Custom.TLabel').grid(row=1, column=0, padx=5, pady=5)
priority_entry = ttk.Entry(input_frame, style='Custom.TEntry')
priority_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Deadline:", style='Custom.TLabel').grid(row=1, column=2, padx=5, pady=5)
deadline_entry = ttk.Entry(input_frame, style='Custom.TEntry')
deadline_entry.grid(row=1, column=3, padx=5, pady=5)

# Buttons Frame
button_frame = ttk.Frame(root, style='Custom.TLabelframe')
button_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(button_frame, text="Add Task", command=add_task, style='Primary.TButton').pack(side="left", padx=5)
ttk.Button(button_frame, text="Save Tasks", command=save_tasks, style='Primary.TButton').pack(side="left", padx=5)
ttk.Button(button_frame, text="Load Tasks", command=load_tasks, style='Primary.TButton').pack(side="left", padx=5)
ttk.Button(button_frame, text="Clear All Tasks", command=clear_tasks, style='Primary.TButton').pack(side="left", padx=5)
ttk.Button(button_frame, text="Generate Timetable", command=generate_timetable, style='Primary.TButton').pack(side="left", padx=5)

# Task List Frame
task_list_frame = ttk.LabelFrame(root, text="Task List", style='Custom.TLabelframe')
task_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Custom style for Listbox
task_listbox = tk.Listbox(task_list_frame, height=6,
                         bg=COLORS['white'],
                         fg=COLORS['text'],
                         selectbackground=COLORS['secondary'],
                         selectforeground=COLORS['white'],
                         font=('Helvetica', 10))
task_listbox.pack(fill="both", expand=True)
ttk.Button(task_list_frame, text="Delete Selected Task", command=delete_task, style='Primary.TButton').pack(pady=5)

# Display Frame
display_frame = ttk.LabelFrame(root, text="Timetable Display", style='Custom.TLabelframe')
display_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Custom style for Text widget
task_display = tk.Text(display_frame, height=10,
                      bg=COLORS['white'],
                      fg=COLORS['text'],
                      font=('Helvetica', 10))
task_display.pack(fill="both", expand=True)

# Chat Frame
chat_frame = ttk.LabelFrame(root, text="AI Study Assistant", style='Custom.TLabelframe')
chat_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Custom style for ScrolledText
chat_display = scrolledtext.ScrolledText(
    chat_frame, height=8,
    bg=COLORS['white'],
    fg=COLORS['text'],
    font=('Helvetica', 10))
chat_display.pack(fill="both", expand=True)

chat_input_frame = ttk.Frame(chat_frame, style='Custom.TLabelframe')
chat_input_frame.pack(fill="x", pady=5)

chat_input = ttk.Entry(chat_input_frame, style='Custom.TEntry')
chat_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
ttk.Button(chat_input_frame, text="Send", command=chat_response, style='Primary.TButton').pack(side="right")

# Add some welcome text to the chat display
welcome_message = """Welcome to Smart Study Planner! 🎓
You can ask me about:
• study tips
• schedule organization
• break timing
• motivation
• focus techniques

How can I help you today?
"""
chat_display.insert(tk.END, welcome_message)

root.mainloop()
