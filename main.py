
from task_manager import add_task, display_tasks

def main():
    while True:
        print("\n==============================")
        print("     STUDENT TASK MANAGER")
        print("==============================")
        print("1. Add Task")
        print("2. Display Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            add_task(title)
            print("Task added successfully!")

        elif choice == "2":
            all_tasks = display_tasks()

            if not all_tasks:
                print("No tasks found.")
            else:
                for task in all_tasks:
                    status = "Completed" if task["completed"] else "Pending"
                    print(
                        f'ID: {task["id"]} | '
                        f'Title: {task["title"]} | '
                        f'Status: {status}'
                    )

        elif choice == "3":
            print("Complete functionality will be added.")

        elif choice == "4":
            print("Delete functionality will be added.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()