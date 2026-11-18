
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

def delete_task(task_id):
    """Delete a task using its ID."""

    if not isinstance(task_id, int) or isinstance(task_id, bool):
        return False

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            del tasks[index]
            return True

    return False

def display_tasks():
    return tasks