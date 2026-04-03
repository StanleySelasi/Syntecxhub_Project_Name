import tkinter as tk
from tkinter import messagebox
import json
import os

FILE = "tasks.json"


def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def update_list():
    listbox.delete(0, tk.END)

    completed = 0

    for task in tasks:
        if task["done"]:
            completed += 1
            listbox.insert(tk.END, "☑  " + task["task"])
        else:
            listbox.insert(tk.END, "☐  " + task["task"])

    stats_label.config(
        text=f"{completed} of {len(tasks)} tasks completed"
    )

def add_task():
    task = entry.get()

    if task.strip() == "":
        messagebox.showwarning("Warning", "Enter a task")
        return

    tasks.append({"task": task, "done": False})
    entry.delete(0, tk.END)

    update_list()
    save_tasks()

def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)

        update_list()
        save_tasks()

    except:
        messagebox.showwarning("Warning", "Select a task")

def mark_done():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = True

        update_list()
        save_tasks()

    except:
        messagebox.showwarning("Warning", "Select a task")


root = tk.Tk()
root.title("To-Do List Manager")
root.geometry("460x560")
root.configure(bg="#f5f6fa")
root.resizable(False, False)

tasks = load_tasks()


title = tk.Label(
    root,
    text="To-Do List Manager",
    font=("Segoe UI", 20, "bold"),
    bg="#f5f6fa",
    fg="#2f3640"
)
title.pack(pady=15)


entry = tk.Entry(
    root,
    font=("Segoe UI", 12),
    width=30,
    bd=0,
    highlightthickness=1,
    highlightbackground="#dcdde1",
    relief="flat"
)
entry.pack(pady=10, ipady=6)


btn_frame = tk.Frame(root, bg="#f5f6fa")
btn_frame.pack(pady=10)

add_btn = tk.Button(
    btn_frame,
    text="Add Task",
    bg="#4078c0",
    fg="white",
    width=12,
    font=("Segoe UI", 10, "bold"),
    bd=0,
    command=add_task
)
add_btn.grid(row=0, column=0, padx=5)

delete_btn = tk.Button(
    btn_frame,
    text="Delete Task",
    bg="#e84118",
    fg="white",
    width=12,
    font=("Segoe UI", 10, "bold"),
    bd=0,
    command=delete_task
)
delete_btn.grid(row=0, column=1, padx=5)

done_btn = tk.Button(
    btn_frame,
    text="Mark Done",
    bg="#44bd32",
    fg="white",
    width=12,
    font=("Segoe UI", 10, "bold"),
    bd=0,
    command=mark_done
)
done_btn.grid(row=0, column=2, padx=5)


frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)

listbox = tk.Listbox(
    frame,
    width=42,
    height=15,
    font=("Segoe UI", 11),
    bd=0,
    highlightthickness=1,
    highlightbackground="#dcdde1",
    selectbackground="#dfe6e9",
    activestyle="none",
    yscrollcommand=scrollbar.set
)

scrollbar.config(command=listbox.yview)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack()


stats_label = tk.Label(
    root,
    text="0 tasks",
    font=("Segoe UI", 10),
    bg="#f5f6fa",
    fg="#718093"
)
stats_label.pack(pady=10)

update_list()

root.mainloop()