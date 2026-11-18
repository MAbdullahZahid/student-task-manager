
tasks = []
next_task_id = 1


def add_task(description):
    """Add a new task and return its details."""
    global next_task_id

    if not description or not description.strip():
        return None

    task = {
        "id": next_task_id,
        "description": description.strip(),
        "completed": False
    }

    tasks.append(task)
    next_task_id += 1

    return task


def display_tasks():
    """Return all tasks."""
    return tasks


def complete_task(task_id):
    """Mark a task as completed."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return True

    return False


def delete_task(task_id):
    """Delete a task using its ID."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True

    return False


def clear_tasks():
    """Reset tasks and IDs. Mainly useful for testing."""
    global next_task_id
    tasks.clear()
    next_task_id = 1
