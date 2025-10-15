import os
import json
from datetime import datetime
from typing import List, Optional, Dict
import shutil


class Student:

    def __init__(self, student_id: str, student_name: str,
                 subjects_enrolled: List[str] = None,
                 subjects_completed: List[str] = None,
                 subjects_marks: List[int] = None):

        self.student_id = student_id
        self.student_name = student_name
        self.subjects_enrolled = subjects_enrolled if subjects_enrolled else []
        self.subjects_completed = subjects_completed if subjects_completed else []
        self.subjects_marks = subjects_marks if subjects_marks else []

    def to_string(self) -> str:

        enrolled_str = ";".join(self.subjects_enrolled) if self.subjects_enrolled else ""
        completed_str = ";".join(self.subjects_completed) if self.subjects_completed else ""
        marks_str = ";".join(map(str, self.subjects_marks)) if self.subjects_marks else ""

        return f"{self.student_id},{self.student_name},{enrolled_str},{completed_str},{marks_str}"

    @staticmethod
    def from_string(line: str) -> 'Student':

        parts = line.strip().split(',')
        if len(parts) < 2:
            raise ValueError(f"Invalid student record format: {line}")

        student_id = parts[0]
        student_name = parts[1]

        subjects_enrolled = []
        if len(parts) > 2 and parts[2]:
            subjects_enrolled = parts[2].split(';')

        subjects_completed = []
        if len(parts) > 3 and parts[3]:
            subjects_completed = parts[3].split(';')

        subjects_marks = []
        if len(parts) > 4 and parts[4]:
            subjects_marks = [int(mark) for mark in parts[4].split(';')]

        return Student(student_id, student_name, subjects_enrolled,
                       subjects_completed, subjects_marks)

    def __str__(self) -> str:
        return (f"ID: {self.student_id} | Name: {self.student_name} | "
                f"Enrolled: {', '.join(self.subjects_enrolled) if self.subjects_enrolled else 'None'} | "
                f"Completed: {', '.join(self.subjects_completed) if self.subjects_completed else 'None'}")


class StudentManager:

    def __init__(self, filename: str = "students.txt", auto_backup: bool = True):

        self.filename = filename
        self.students: List[Student] = []
        self.action_history: List[Dict] = []  # Stack for undo functionality
        self.auto_backup = auto_backup
        self.backup_dir = "backups"

        if self.auto_backup and not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        self.load_data()

    def load_data(self) -> bool:

        try:
            if not os.path.exists(self.filename):
                # Create empty file if it doesn't exist
                with open(self.filename, 'w') as f:
                    pass
                print(f"Created new data file: {self.filename}")
                return True

            with open(self.filename, 'r') as f:
                lines = f.readlines()
                self.students = []

                for line in lines:
                    line = line.strip()
                    if line:  # Skip empty lines
                        try:
                            student = Student.from_string(line)
                            self.students.append(student)
                        except ValueError as e:
                            print(f"Warning: Skipping invalid record - {e}")

            print(f"Loaded {len(self.students)} student records from {self.filename}")
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def save_data(self) -> bool:

        try:
            if self.auto_backup and os.path.exists(self.filename):
                self._create_backup()

            with open(self.filename, 'w') as f:
                for student in self.students:
                    f.write(student.to_string() + '\n')

            print(f"Saved {len(self.students)} student records to {self.filename}")
            return True

        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def _create_backup(self) -> None:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = os.path.join(self.backup_dir,
                                           f"{os.path.splitext(self.filename)[0]}_{timestamp}.txt")
            shutil.copy2(self.filename, backup_filename)
            print(f"Backup created: {backup_filename}")
        except Exception as e:
            print(f"Warning: Could not create backup - {e}")

    def add_student(self, student: Student) -> bool:

        if self.search_student(student.student_id):
            print(f"Error: Student ID {student.student_id} already exists")
            return False

        # Save state for undo
        self._save_state('add_student', student.student_id)

        self.students.append(student)
        self.save_data()  # Auto-save
        print(f"Student {student.student_name} added successfully")
        return True

    def remove_student(self, student_id: str) -> bool:

        student = self.search_student(student_id)
        if not student:
            print(f"Error: Student ID {student_id} not found")
            return False

        self._save_state('remove_student', student_id, student)

        self.students.remove(student)
        self.save_data()  # Auto-save
        print(f"Student {student.student_name} removed successfully")
        return True

    def search_student(self, student_id: str) -> Optional[Student]:

        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_enrollment(self, student_id: str, subject: str) -> bool:

        student = self.search_student(student_id)
        if not student:
            print(f"Error: Student ID {student_id} not found")
            return False

        if subject in student.subjects_enrolled:
            print(f"Student is already enrolled in {subject}")
            return False

        if subject in student.subjects_completed:
            print(f"Student has already completed {subject}")
            return False

        self._save_state('update_enrollment', student_id,
                         {'subject': subject, 'action': 'add'})

        student.subjects_enrolled.append(subject)
        self.save_data()  # Auto-save
        print(f"Student {student.student_name} enrolled in {subject}")
        return True

    def mark_subject_completed(self, student_id: str, subject: str, mark: int) -> bool:

        student = self.search_student(student_id)
        if not student:
            print(f"Error: Student ID {student_id} not found")
            return False

        if subject not in student.subjects_enrolled:
            print(f"Error: Student is not enrolled in {subject}")
            return False

        if not (0 <= mark <= 100):
            print(f"Error: Mark must be between 0 and 100")
            return False

        self._save_state('mark_completed', student_id,
                         {'subject': subject, 'mark': mark})

        student.subjects_enrolled.remove(subject)
        student.subjects_completed.append(subject)
        student.subjects_marks.append(mark)
        self.save_data()  # Auto-save
        print(f"Subject {subject} marked as completed for {student.student_name} with mark {mark}")
        return True

    def list_all_students(self) -> List[Student]:

        return self.students

    def get_statistics(self) -> Dict:

        stats = {
            'total_students': len(self.students),
            'subjects_enrollment_count': {},
            'students_by_completed_count': {}
        }

        for student in self.students:
            for subject in student.subjects_enrolled:
                stats['subjects_enrollment_count'][subject] = \
                    stats['subjects_enrollment_count'].get(subject, 0) + 1

        for student in self.students:
            completed_count = len(student.subjects_completed)
            name = f"{student.student_name} ({student.student_id})"
            stats['students_by_completed_count'][name] = completed_count

        return stats

    def _save_state(self, action: str, student_id: str, data=None) -> None:

        state = {
            'action': action,
            'student_id': student_id,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.action_history.append(state)

        if len(self.action_history) > 10:
            self.action_history.pop(0)

    def undo_last_action(self) -> bool:

        if not self.action_history:
            print("No actions to undo")
            return False

        last_action = self.action_history.pop()
        action_type = last_action['action']
        student_id = last_action['student_id']
        data = last_action['data']

        try:
            if action_type == 'add_student':
                # Remove the added student
                student = self.search_student(student_id)
                if student:
                    self.students.remove(student)
                    print(f"Undid: Add student {student_id}")

            elif action_type == 'remove_student':
                # Re-add the removed student
                if data:
                    self.students.append(data)
                    print(f"Undid: Remove student {student_id}")

            elif action_type == 'update_enrollment':
                # Remove the enrolled subject
                student = self.search_student(student_id)
                if student and data['subject'] in student.subjects_enrolled:
                    student.subjects_enrolled.remove(data['subject'])
                    print(f"Undid: Enrollment in {data['subject']}")

            elif action_type == 'mark_completed':
                # Move subject back to enrolled
                student = self.search_student(student_id)
                if student:
                    subject = data['subject']
                    if subject in student.subjects_completed:
                        idx = student.subjects_completed.index(subject)
                        student.subjects_completed.pop(idx)
                        student.subjects_marks.pop(idx)
                        student.subjects_enrolled.append(subject)
                        print(f"Undid: Completion of {subject}")

            self.save_data()
            return True

        except Exception as e:
            print(f"Error during undo: {e}")
            return False


# Unit Tests
if __name__ == "__main__":
    print("Running Unit Tests for StudentManager\n")
    print("=" * 50)

    print("\nTest 1: Creating manager and adding students")
    manager = StudentManager("test_students.txt")

    student1 = Student("S001", "John Doe", ["COMP101", "MATH201"], ["PHYS101"], [85])
    student2 = Student("S002", "Jane Smith", ["COMP101", "CHEM101"])

    assert manager.add_student(student1) == True, "Failed to add student1"
    assert manager.add_student(student2) == True, "Failed to add student2"
    assert manager.add_student(student1) == False, "Duplicate student ID should fail"
    print("✓ Add student tests passed")

    print("\nTest 2: Testing search functionality")
    found = manager.search_student("S001")
    assert found is not None, "Failed to find existing student"
    assert found.student_name == "John Doe", "Found wrong student"
    assert manager.search_student("S999") is None, "Found non-existent student"
    print("✓ Search tests passed")

    print("\nTest 3: Testing enrollment updates")
    assert manager.update_enrollment("S001", "ENG201") == True, "Failed to enroll"
    assert manager.update_enrollment("S001", "COMP101") == False, "Enrolled in duplicate subject"
    print("✓ Enrollment tests passed")

    print("\nTest 4: Testing mark subject completed")
    assert manager.mark_subject_completed("S001", "COMP101", 92) == True, "Failed to mark completed"
    assert manager.mark_subject_completed("S001", "COMP101", 92) == False, "Marked non-enrolled subject"
    print("✓ Mark completed tests passed")

    print("\nTest 5: Testing statistics generation")
    stats = manager.get_statistics()
    assert stats['total_students'] == 2, "Wrong student count"
    print("✓ Statistics tests passed")

    print("\nTest 6: Testing undo functionality")
    assert manager.undo_last_action() == True, "Failed to undo"
    print("✓ Undo tests passed")

    if os.path.exists("test_students.txt"):
        os.remove("test_students.txt")
    if os.path.exists("backups"):
        shutil.rmtree("backups")

    print("\n" + "=" * 50)
    print("All unit tests passed successfully! ✓")
