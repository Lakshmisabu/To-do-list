import os
import datetime

class TodoList:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filename):
            return []
        
        tasks = []
        with open(self.filename, 'r') as file:
            for line in file:
                task, due_date_str, status = line.strip().split(' | ')
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                tasks.append({"task": task, "due_date": due_date, "completed": status == "True"})
        return tasks

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            for task in self.tasks:
                file.write(f'{task["task"]} | {task["due_date"]} | {task["completed"]}\n')

    def add_task(self, task, due_date):
        due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
        self.tasks.append({"task": task, "due_date": due_date, "completed": False})
        self.save_tasks()
        print(f'Added task: "{task}" with due date {due_date}')

    def view_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
        else:
            for i, task in enumerate(self.tasks, 1):
                status = "✓" if task["completed"] else "✗"
                print(f"{i}. [{status}] {task['task']} (Due: {task['due_date']})")

    def complete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]["completed"] = True
            self.save_tasks()
            print(f'Task {task_number} marked as completed.')
        else:
            print("Invalid task number.")

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            removed_task = self.tasks.pop(task_number - 1)
            self.save_tasks()
            print(f'Deleted task: "{removed_task["task"]}"')
        else:
            print("Invalid task number.")

    def check_due_tasks(self):
        today = datetime.date.today()
        overdue_tasks = [task for task in self.tasks if task['due_date'] < today and not task['completed']]
        due_today_tasks = [task for task in self.tasks if task['due_date'] == today and not task['completed']]
        
        if overdue_tasks:
            print("\nOverdue Tasks:")
            for task in overdue_tasks:
                print(f"- {task['task']} (Due: {task['due_date']})")
        else:
            print("\nNo overdue tasks.")

        if due_today_tasks:
            print("\nTasks Due Today:")
            for task in due_today_tasks:
                print(f"- {task['task']} (Due: {task['due_date']})")
        else:
            print("No tasks due today.")

    def display_reminders(self):
        print("Checking for due tasks...")
        self.check_due_tasks()

    def run(self):
        # Display reminders at the start
        self.display_reminders()
        
        while True:
            print("\nOptions:")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Complete Task")
            print("4. Delete Task")
            print("5. Check Due Tasks")
            print("6. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                print("\nTo-Do List:")
                self.view_tasks()
            elif choice == "2":
                task = input("Enter the task: ")
                due_date = input("Enter the due date (YYYY-MM-DD): ")
                self.add_task(task, due_date)
            elif choice == "3":
                task_number = int(input("Enter task number to complete: "))
                self.complete_task(task_number)
            elif choice == "4":
                task_number = int(input("Enter task number to delete: "))
                self.delete_task(task_number)
            elif choice == "5":
                self.check_due_tasks()
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    todo_list = TodoList()
    todo_list.run()
