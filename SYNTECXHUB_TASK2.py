import json
import tkinter as tk
from tkinter import ttk, messagebox

class StudentManager:
    def __init__(self):
        self.students = []
        self.load_students()

    def add_student(self, name, student_id, grade):
        if not name or not student_id or not grade:
            return "All fields required"

        for s in self.students:
            if s["id"] == student_id:
                return "ID already exists"

        self.students.append({
            "name": name,
            "id": student_id,
            "grade": grade
        })
        self.save_students()
        return "Student added"

    def delete_student(self, student_id):
        for s in self.students:
            if s["id"] == student_id:
                self.students.remove(s)
                self.save_students()
                return "Deleted"
        return "Not found"

    def save_students(self):
        with open("students.json", "w") as f:
            json.dump(self.students, f, indent=4)

    def load_students(self):
        try:
            with open("students.json", "r") as f:
                self.students = json.load(f)
        except:
            self.students = []



class App:
    def __init__(self, root):
        self.manager = StudentManager()
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("650x450")

        
        title = tk.Label(root, text="Student Management System", font=("Arial", 18, "bold"))
        title.pack(pady=10)

    
        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name").grid(row=0, column=0, padx=10)
        tk.Label(form_frame, text="Student ID").grid(row=0, column=1, padx=10)
        tk.Label(form_frame, text="Grade").grid(row=0, column=2, padx=10)

        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=1, column=0, padx=10)

        self.id_entry = tk.Entry(form_frame)
        self.id_entry.grid(row=1, column=1, padx=10)

        self.grade_entry = tk.Entry(form_frame)
        self.grade_entry.grid(row=1, column=2, padx=10)

    
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Student", width=15, command=self.add_student).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected", width=15, command=self.delete_selected).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Refresh", width=15, command=self.display_students).grid(row=0, column=2, padx=5)

        
        self.tree = ttk.Treeview(root, columns=("Name", "ID", "Grade"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Grade", text="Grade")

        self.tree.column("Name", width=200)
        self.tree.column("ID", width=150)
        self.tree.column("Grade", width=100)

        self.tree.pack(pady=10, fill="both", expand=True)

        self.display_students()

    def add_student(self):
        name = self.name_entry.get().strip()
        student_id = self.id_entry.get().strip()
        grade = self.grade_entry.get().strip()

        result = self.manager.add_student(name, student_id, grade)
        messagebox.showinfo("Info", result)
        self.display_students()

    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return

        confirm = messagebox.askyesno("Confirm", "Delete selected student?")
        if not confirm:
            return

        item = self.tree.item(selected[0])
        student_id = item["values"][1]

        result = self.manager.delete_student(student_id)
        messagebox.showinfo("Info", result)
        self.display_students()

    def display_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for s in self.manager.students:
            self.tree.insert("", tk.END, values=(s["name"], s["id"], s["grade"]))



root = tk.Tk()
app = App(root)
root.mainloop()