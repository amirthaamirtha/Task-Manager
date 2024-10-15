import json
import os

# Task Class Definition
class Task:
    def _init_(self, task_id, title, completed=False):
        self.id = task_id
        self.title = title
        self.completed = completed

    def to_dict(self):
        """Converts the Task object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        """Creates a Task object from a dictionary."""
        return Task(task_id=data['id'], title=data['title'], completed=data['completed'])

# File handling for loading and saving tasks
def load_tasks():
    """Loads tasks from the tasks.json file."""
    if os.path.exists('tasks.json'):
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task) for task in tasks_data]
        except (json.JSONDecodeError, ValueError):
            # Handle case where tasks.json is empty or contains invalid JSON
            print("Warning: tasks.json is empty or contains invalid data. Starting with an empty task list.")
            return []
    return []

def save_tasks(tasks):
    """Saves tasks to the tasks.json file."""
    with open('tasks.json', 'w') as file:
        tasks_data = [task.to_dict() for task in tasks]
        json.dump(tasks_data, file, indent=4)

# Task Management Functions
def add_task(tasks, title):
    """Adds a new task to the list."""
    task_id = len(tasks) + 1 if tasks else 1
    new_task = Task(task_id, title)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{title}' has been added with ID {task_id}.")

def view_tasks(tasks):
    """Displays all tasks with their status."""
    if not tasks:
        print("No tasks available.")
    else:
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            print(f"ID: {task.id}, Title: {task.title}, Status: {status}")

def delete_task(tasks, task_id):
    """Deletes a task by its ID."""
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task ID {task_id} has been deleted.")
            return
    print(f"Task with ID {task_id} not found.")

def complete_task(tasks, task_id):
    """Marks a task as completed."""
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            save_tasks(tasks)
            print(f"Task ID {task_id} has been marked as completed.")
            return
    print(f"Task with ID {task_id} not found.")

# Command-Line Interface (CLI)
def main():
    tasks = load_tasks()

    while True:
        print("\nTask Manager:")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Delete a task")
        print("4. Mark a task as completed")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            title = input("Enter the task title: ")
            add_task(tasks, title)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            try:
                task_id = int(input("Enter the task ID to delete: "))
                delete_task(tasks, task_id)
            except ValueError:
                print("Please enter a valid task ID.")
        elif choice == '4':
            try:
                task_id = int(input("Enter the task ID to mark as completed: "))
                complete_task(tasks, task_id)
            except ValueError:
                print("Please enter a valid task ID.")
        elif choice == '5':
            print("Exiting the Task Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()
