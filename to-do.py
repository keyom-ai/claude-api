import requests

API_KEY = "sk-ant-api03-AABBCC"
API_URL = "https://api.anthropic.com/v1/complete"
TODO_FILE = "todo.txt"

def chat_with_claude(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "model": "claude-v1",
        "max_tokens_to_sample": 100
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["completion"]
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def add_task():
    task = input("Enter a new task: ")
    with open(TODO_FILE, "a") as file:
        file.write(task + "\n")
    print("Task added successfully!")

def view_tasks():
    try:
        with open(TODO_FILE, "r") as file:
            tasks = file.read().strip().split("\n")
            if tasks:
                print("Current tasks:")
                for i, task in enumerate(tasks, start=1):
                    print(f"{i}. {task}")
            else:
                print("No tasks found.")
    except FileNotFoundError:
        print("No tasks found.")

def complete_task():
    view_tasks()
    task_id = int(input("Enter the task number to mark as complete: "))
    try:
        with open(TODO_FILE, "r") as file:
            tasks = file.read().strip().split("\n")
            if 1 <= task_id <= len(tasks):
                completed_task = tasks.pop(task_id - 1)
                with open(TODO_FILE, "w") as file:
                    file.write("\n".join(tasks))
                print(f"Task '{completed_task}' marked as complete.")
            else:
                print("Invalid task number.")
    except FileNotFoundError:
        print("No tasks found.")

def main():
    while True:
        print("\n--- To-Do App ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
