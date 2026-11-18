
tasks = []
next_id = 1

def add_task(title):
    global next_id

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return task

def complete_task(task_id):
    """Mark a task as completed using its ID."""

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return True

    return False

def display_tasks():
    return tasks