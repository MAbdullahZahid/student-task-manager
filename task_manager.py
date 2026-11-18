
tasks = []
next_id = 1

def add_task(title):
    global next_id

    title = title.strip()

    if not title:
        raise ValueError("Task title cannot be empty.")

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return task

def display_tasks():
    return tasks