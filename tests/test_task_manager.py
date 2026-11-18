
import unittest
import task_manager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        task_manager.clear_tasks()

    def test_add_task(self):
        task = task_manager.add_task("Complete DevOps assignment")

        self.assertIsNotNone(task)
        self.assertEqual(task["description"], "Complete DevOps assignment")
        self.assertFalse(task["completed"])

    def test_complete_task(self):
        task = task_manager.add_task("Complete DevOps assignment")

        result = task_manager.complete_task(task["id"])

        self.assertTrue(result)
        self.assertTrue(task["completed"])

    def test_delete_task(self):
        task = task_manager.add_task("Complete DevOps assignment")

        result = task_manager.delete_task(task["id"])

        self.assertTrue(result)
        self.assertEqual(len(task_manager.display_tasks()), 0)


if __name__ == "__main__":
    unittest.main()
