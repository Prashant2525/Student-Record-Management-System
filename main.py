import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_manager import StudentManager, Student
from typing import Optional


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Management System - Login")
        self.root.geometry("450x400")
        self.root.resizable(False, False)

        self.center_window()

        self.user_role = None
        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(main_frame, text="Student Management System",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 30))

        login_frame = ttk.Frame(main_frame)
        login_frame.pack(pady=10)

        ttk.Label(login_frame, text="Username:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=12, padx=(0, 10))
        self.username_entry = ttk.Entry(login_frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=12)

        ttk.Label(login_frame, text="Password:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=12, padx=(0, 10))
        self.password_entry = ttk.Entry(login_frame, width=25, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, pady=12)

        ttk.Label(login_frame, text="Role:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=12, padx=(0, 10))
        self.role_var = tk.StringVar(value="Admin")
        role_combo = ttk.Combobox(login_frame, textvariable=self.role_var,
                                  values=["Admin", "Teacher", "Viewer"],
                                  state="readonly", width=22, font=("Arial", 10))
        role_combo.grid(row=2, column=1, pady=12)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        login_btn = tk.Button(button_frame, text="Login", command=self.login,
                              width=20, height=2, font=("Arial", 10, "bold"),
                              bg="#4CAF50", fg="white", cursor="hand2",
                              activebackground="#45a049")
        login_btn.pack()

        info_frame = ttk.LabelFrame(main_frame, text="Copyright © 2025 - Prashant", padding="10")
        info_frame.pack(pady=10, fill=tk.X)

        info_text = ("Admin: admin / admin123\n"
                     "Teacher: teacher / teach123\n"
                     "Viewer: viewer / view123")
        info_label = tk.Label(info_frame, text=info_text, font=("Arial", 9),
                              fg="gray", justify=tk.LEFT)
        info_label.pack()

        self.root.bind('<Return>', lambda e: self.login())

        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        credentials = {
            'admin': {'password': 'admin123', 'role': 'Admin'},
            'teacher': {'password': 'teach123', 'role': 'Teacher'},
            'viewer': {'password': 'view123', 'role': 'Viewer'}
        }

        if username in credentials and credentials[username]['password'] == password:
            if credentials[username]['role'] == role:
                self.user_role = role
                self.root.destroy()
            else:
                messagebox.showerror("Error", "Invalid role selected for this user")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()

    def show(self) -> Optional[str]:

        self.root.mainloop()
        return self.user_role


class StudentManagementGUI:

    def __init__(self, user_role: str, filename: str = "students.txt"):

        self.root = tk.Tk()
        self.root.title(f"Student Management System - {user_role}")
        self.root.geometry("1200x700")

        self.user_role = user_role
        self.manager = StudentManager(filename)

        self.setup_ui()
        self.refresh_student_list()

    def setup_ui(self):
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)

        title_frame = ttk.Frame(main_container)
        title_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        title_label = tk.Label(title_frame,
                               text=f"Student Record Management System ({self.user_role})",
                               font=("Arial", 18, "bold"))
        title_label.pack()

        left_panel = ttk.LabelFrame(main_container, text="Operations", padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        self.setup_input_forms(left_panel)

        right_panel = ttk.LabelFrame(main_container, text="Student Records", padding="10")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        self.setup_student_list(right_panel)

        # Bottom panel - Statistics and actions
        bottom_panel = ttk.Frame(main_container)
        bottom_panel.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.setup_bottom_panel(bottom_panel)

    def setup_input_forms(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)

        add_tab = ttk.Frame(notebook, padding="10")
        notebook.add(add_tab, text="Add Student")
        self.setup_add_student_form(add_tab)

        enroll_tab = ttk.Frame(notebook, padding="10")
        notebook.add(enroll_tab, text="Enroll Subject")
        self.setup_enroll_form(enroll_tab)

        complete_tab = ttk.Frame(notebook, padding="10")
        notebook.add(complete_tab, text="Mark Completed")
        self.setup_complete_form(complete_tab)

        search_tab = ttk.Frame(notebook, padding="10")
        notebook.add(search_tab, text="Search Student")
        self.setup_search_form(search_tab)

        if self.user_role == "Teacher":
            notebook.tab(0, state="disabled")  # Disable Add Student
        elif self.user_role == "Viewer":
            notebook.tab(0, state="disabled")  # Disable Add Student
            notebook.tab(1, state="disabled")  # Disable Enroll
            notebook.tab(2, state="disabled")  # Disable Mark Completed

    def setup_add_student_form(self, parent):
        ttk.Label(parent, text="Student ID:", font=("Arial", 10)).grid(row=0, column=0,
                                                                       sticky=tk.W, pady=5)
        self.add_id_entry = ttk.Entry(parent, width=30)
        self.add_id_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(parent, text="Student Name:", font=("Arial", 10)).grid(row=1, column=0,
                                                                         sticky=tk.W, pady=5)
        self.add_name_entry = ttk.Entry(parent, width=30)
        self.add_name_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(parent, text="Subjects Enrolled:", font=("Arial", 10)).grid(row=2, column=0,
                                                                              sticky=tk.W, pady=5)
        ttk.Label(parent, text="(comma-separated)", font=("Arial", 8),
                  foreground="gray").grid(row=2, column=1, sticky=tk.W, padx=5)
        self.add_enrolled_entry = ttk.Entry(parent, width=30)
        self.add_enrolled_entry.grid(row=3, column=1, pady=5, padx=5)

        add_btn = ttk.Button(parent, text="Add Student", command=self.add_student)
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)

        if self.user_role != "Admin":
            add_btn.config(state="disabled")

    def setup_enroll_form(self, parent):
        ttk.Label(parent, text="Student ID:", font=("Arial", 10)).grid(row=0, column=0,
                                                                       sticky=tk.W, pady=5)
        self.enroll_id_entry = ttk.Entry(parent, width=30)
        self.enroll_id_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(parent, text="Subject Code:", font=("Arial", 10)).grid(row=1, column=0,
                                                                         sticky=tk.W, pady=5)
        self.enroll_subject_entry = ttk.Entry(parent, width=30)
        self.enroll_subject_entry.grid(row=1, column=1, pady=5, padx=5)

        enroll_btn = ttk.Button(parent, text="Enroll Student", command=self.enroll_student)
        enroll_btn.grid(row=2, column=0, columnspan=2, pady=20)

        if self.user_role == "Viewer":
            enroll_btn.config(state="disabled")

    def setup_complete_form(self, parent):
        ttk.Label(parent, text="Student ID:", font=("Arial", 10)).grid(row=0, column=0,
                                                                       sticky=tk.W, pady=5)
        self.complete_id_entry = ttk.Entry(parent, width=30)
        self.complete_id_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(parent, text="Subject Code:", font=("Arial", 10)).grid(row=1, column=0,
                                                                         sticky=tk.W, pady=5)
        self.complete_subject_entry = ttk.Entry(parent, width=30)
        self.complete_subject_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(parent, text="Mark (0-100):", font=("Arial", 10)).grid(row=2, column=0,
                                                                         sticky=tk.W, pady=5)
        self.complete_mark_entry = ttk.Entry(parent, width=30)
        self.complete_mark_entry.grid(row=2, column=1, pady=5, padx=5)

        complete_btn = ttk.Button(parent, text="Mark as Completed",
                                  command=self.mark_completed)
        complete_btn.grid(row=3, column=0, columnspan=2, pady=20)

        if self.user_role == "Viewer":
            complete_btn.config(state="disabled")

    def setup_search_form(self, parent):
        ttk.Label(parent, text="Student ID:", font=("Arial", 10)).grid(row=0, column=0,
                                                                       sticky=tk.W, pady=5)
        self.search_id_entry = ttk.Entry(parent, width=30)
        self.search_id_entry.grid(row=0, column=1, pady=5, padx=5)

        search_btn = ttk.Button(parent, text="Search Student", command=self.search_student)
        search_btn.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(parent, text="Search Results:", font=("Arial", 10, "bold")).grid(row=2,
                                                                                   column=0,
                                                                                   columnspan=2,
                                                                                   sticky=tk.W,
                                                                                   pady=(20, 5))

        self.search_result_text = scrolledtext.ScrolledText(parent, height=10, width=40,
                                                            wrap=tk.WORD)
        self.search_result_text.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

    def setup_student_list(self, parent):
        # Create treeview
        columns = ("ID", "Name", "Enrolled", "Completed", "Avg Mark")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)

        # Define column headings
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Enrolled", text="Subjects Enrolled")
        self.tree.heading("Completed", text="Subjects Completed")
        self.tree.heading("Avg Mark", text="Average Mark")

        # Define column widths
        self.tree.column("ID", width=100)
        self.tree.column("Name", width=150)
        self.tree.column("Enrolled", width=150)
        self.tree.column("Completed", width=150)
        self.tree.column("Avg Mark", width=100)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<Double-1>', self.view_student_details)

    def setup_bottom_panel(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(side=tk.LEFT, padx=10)

        refresh_btn = ttk.Button(btn_frame, text="Refresh List", command=self.refresh_student_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        stats_btn = ttk.Button(btn_frame, text="View Statistics", command=self.show_statistics)
        stats_btn.pack(side=tk.LEFT, padx=5)

        undo_btn = ttk.Button(btn_frame, text="Undo Last Action", command=self.undo_action)
        undo_btn.pack(side=tk.LEFT, padx=5)
        if self.user_role == "Viewer":
            undo_btn.config(state="disabled")

        if self.user_role == "Admin":
            remove_btn = ttk.Button(btn_frame, text="Remove Selected Student",
                                    command=self.remove_student)
            remove_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(parent, text="Ready", font=("Arial", 9),
                                     fg="green", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)

    def add_student(self):
        student_id = self.add_id_entry.get().strip()
        student_name = self.add_name_entry.get().strip()
        enrolled_str = self.add_enrolled_entry.get().strip()

        if not student_id or not student_name:
            messagebox.showerror("Error", "Student ID and Name are required")
            return

        subjects_enrolled = []
        if enrolled_str:
            subjects_enrolled = [s.strip() for s in enrolled_str.split(',') if s.strip()]

        student = Student(student_id, student_name, subjects_enrolled)

        if self.manager.add_student(student):
            messagebox.showinfo("Success", f"Student {student_name} added successfully")
            self.clear_add_form()
            self.refresh_student_list()
            self.update_status(f"Added student: {student_name}")
        else:
            messagebox.showerror("Error", f"Failed to add student (ID may already exist)")

    def enroll_student(self):
        student_id = self.enroll_id_entry.get().strip()
        subject = self.enroll_subject_entry.get().strip().upper()

        if not student_id or not subject:
            messagebox.showerror("Error", "Student ID and Subject are required")
            return

        if self.manager.update_enrollment(student_id, subject):
            messagebox.showinfo("Success", f"Student enrolled in {subject}")
            self.clear_enroll_form()
            self.refresh_student_list()
            self.update_status(f"Enrolled student {student_id} in {subject}")
        else:
            messagebox.showerror("Error", "Failed to enroll student (check console for details)")

    def mark_completed(self):
        student_id = self.complete_id_entry.get().strip()
        subject = self.complete_subject_entry.get().strip().upper()
        mark_str = self.complete_mark_entry.get().strip()

        if not student_id or not subject or not mark_str:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            mark = int(mark_str)
        except ValueError:
            messagebox.showerror("Error", "Mark must be a valid integer")
            return

        if self.manager.mark_subject_completed(student_id, subject, mark):
            messagebox.showinfo("Success", f"Subject {subject} marked as completed with mark {mark}")
            self.clear_complete_form()
            self.refresh_student_list()
            self.update_status(f"Marked {subject} completed for {student_id}")
        else:
            messagebox.showerror("Error", "Failed to mark subject as completed (check console for details)")

    def search_student(self):
        student_id = self.search_id_entry.get().strip()

        if not student_id:
            messagebox.showerror("Error", "Student ID is required")
            return

        student = self.manager.search_student(student_id)

        self.search_result_text.delete(1.0, tk.END)

        if student:
            result = f"Student ID: {student.student_id}\n"
            result += f"Name: {student.student_name}\n\n"
            result += f"Subjects Enrolled ({len(student.subjects_enrolled)}):\n"
            if student.subjects_enrolled:
                for subject in student.subjects_enrolled:
                    result += f"  • {subject}\n"
            else:
                result += "  None\n"

            result += f"\nSubjects Completed ({len(student.subjects_completed)}):\n"
            if student.subjects_completed:
                for i, subject in enumerate(student.subjects_completed):
                    mark = student.subjects_marks[i] if i < len(student.subjects_marks) else "N/A"
                    result += f"  • {subject}: {mark}\n"
            else:
                result += "  None\n"

            if student.subjects_marks:
                avg_mark = sum(student.subjects_marks) / len(student.subjects_marks)
                result += f"\nAverage Mark: {avg_mark:.2f}"

            self.search_result_text.insert(1.0, result)
            self.update_status(f"Found student: {student.student_name}")
        else:
            self.search_result_text.insert(1.0, f"No student found with ID: {student_id}")
            self.update_status(f"Student not found: {student_id}")

    def remove_student(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student to remove")
            return

        item = self.tree.item(selection[0])
        student_id = item['values'][0]

        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to remove student {student_id}?")
        if confirm:
            if self.manager.remove_student(student_id):
                messagebox.showinfo("Success", f"Student {student_id} removed successfully")
                self.refresh_student_list()
                self.update_status(f"Removed student: {student_id}")
            else:
                messagebox.showerror("Error", "Failed to remove student")

    def refresh_student_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = self.manager.list_all_students()

        for student in students:
            enrolled_count = len(student.subjects_enrolled)
            completed_count = len(student.subjects_completed)

            if student.subjects_marks:
                avg_mark = sum(student.subjects_marks) / len(student.subjects_marks)
                avg_mark_str = f"{avg_mark:.1f}"
            else:
                avg_mark_str = "N/A"

            self.tree.insert('', tk.END, values=(
                student.student_id,
                student.student_name,
                f"{enrolled_count} subjects",
                f"{completed_count} subjects",
                avg_mark_str
            ))

        self.update_status(f"Displaying {len(students)} students")

    def view_student_details(self, event):
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        student_id = item['values'][0]

        student = self.manager.search_student(student_id)
        if not student:
            return

        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Student Details - {student.student_name}")
        detail_window.geometry("500x400")

        text = scrolledtext.ScrolledText(detail_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)

        details = f"{'=' * 50}\n"
        details += f"STUDENT DETAILS\n"
        details += f"{'=' * 50}\n\n"
        details += f"Student ID: {student.student_id}\n"
        details += f"Name: {student.student_name}\n\n"

        details += f"SUBJECTS ENROLLED ({len(student.subjects_enrolled)}):\n"
        details += f"{'-' * 50}\n"
        if student.subjects_enrolled:
            for subject in student.subjects_enrolled:
                details += f"  • {subject}\n"
        else:
            details += "  No subjects currently enrolled\n"

        details += f"\nSUBJECTS COMPLETED ({len(student.subjects_completed)}):\n"
        details += f"{'-' * 50}\n"
        if student.subjects_completed:
            for i, subject in enumerate(student.subjects_completed):
                mark = student.subjects_marks[i] if i < len(student.subjects_marks) else "N/A"
                details += f"  • {subject}: {mark}/100\n"
        else:
            details += "  No subjects completed yet\n"

        if student.subjects_marks:
            avg_mark = sum(student.subjects_marks) / len(student.subjects_marks)
            details += f"\n{'=' * 50}\n"
            details += f"Average Mark: {avg_mark:.2f}/100\n"
            details += f"{'=' * 50}\n"

        text.insert(1.0, details)
        text.config(state=tk.DISABLED)

    def show_statistics(self):
        stats = self.manager.get_statistics()

        stats_window = tk.Toplevel(self.root)
        stats_window.title("System Statistics")
        stats_window.geometry("600x500")

        text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)

        stats_text = f"{'=' * 60}\n"
        stats_text += f"SYSTEM STATISTICS\n"
        stats_text += f"{'=' * 60}\n\n"

        stats_text += f"Total Students: {stats['total_students']}\n\n"

        stats_text += f"SUBJECT ENROLLMENT COUNT:\n"
        stats_text += f"{'-' * 60}\n"
        if stats['subjects_enrollment_count']:
            sorted_subjects = sorted(stats['subjects_enrollment_count'].items(),
                                     key=lambda x: x[1], reverse=True)
            for subject, count in sorted_subjects:
                stats_text += f"  {subject}: {count} student(s)\n"
        else:
            stats_text += "  No enrollments\n"

        stats_text += f"\nCOMPLETED SUBJECTS PER STUDENT:\n"
        stats_text += f"{'-' * 60}\n"
        if stats['students_by_completed_count']:
            sorted_students = sorted(stats['students_by_completed_count'].items(),
                                     key=lambda x: x[1], reverse=True)
            for name, count in sorted_students:
                stats_text += f"  {name}: {count} subject(s)\n"
        else:
            stats_text += "  No completed subjects\n"

        text.insert(1.0, stats_text)
        text.config(state=tk.DISABLED)

    def undo_action(self):
        if self.manager.undo_last_action():
            messagebox.showinfo("Success", "Last action undone successfully")
            self.refresh_student_list()
            self.update_status("Undid last action")
        else:
            messagebox.showinfo("Info", "No actions to undo")

    def update_status(self, message: str):
        self.status_label.config(text=message)
        self.root.after(5000, lambda: self.status_label.config(text="Ready"))

    def clear_add_form(self):
        self.add_id_entry.delete(0, tk.END)
        self.add_name_entry.delete(0, tk.END)
        self.add_enrolled_entry.delete(0, tk.END)

    def clear_enroll_form(self):
        self.enroll_id_entry.delete(0, tk.END)
        self.enroll_subject_entry.delete(0, tk.END)

    def clear_complete_form(self):
        self.complete_id_entry.delete(0, tk.END)
        self.complete_subject_entry.delete(0, tk.END)
        self.complete_mark_entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()


def main():
    login = LoginWindow()
    user_role = login.show()

    # If login successful, show main application
    if user_role:
        app = StudentManagementGUI(user_role)
        app.run()


if __name__ == "__main__":
    main()
