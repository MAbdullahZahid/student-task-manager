
import unittest
import task_manager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        task_manager.tasks.clear()
        task_manager.next_id = 1

    def test_add_task(self):
        task = task_manager.add_task("Complete assignment")

        self.assertEqual(task["title"], "Complete assignment")
        self.assertFalse(task["completed"])
        self.assertEqual(len(task_manager.tasks), 1)

    def test_complete_task(self):
        task = task_manager.add_task("Study Git")

        result = task_manager.complete_task(task["id"])

        self.assertTrue(result)
        self.assertTrue(task["completed"])

    def test_delete_task(self):
        task = task_manager.add_task("Submit lab")

        result = task_manager.delete_task(task["id"])

        self.assertTrue(result)
        self.assertEqual(len(task_manager.tasks), 0)

if __name__ == "__main__":
    unittest.main()