import unittest

from src.tango_data_structures.utils import Queue, Stack, Map, Set, LinkedList


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_enqueue(self):
        self.queue.enqueue(10)
        self.assertEqual(self.queue.size(), 1)

    def test_dequeue(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.size(), 1)

    def test_first_item(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.first_item(), 10)
        self.assertEqual(self.queue.size(), 2)

    def test_last_item(self):
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.last_item(), 20)
        self.assertEqual(self.queue.size(), 2)

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(10)
        self.assertFalse(self.queue.is_empty())

    def test_size(self):
        self.assertEqual(self.queue.size(), 0)
        self.queue.enqueue(10)
        self.assertEqual(self.queue.size(), 1)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.size(), 2)

    def test_dequeue_empty(self):
        with self.assertRaises(Exception):
            self.queue.dequeue()

    def test_first_item_empty(self):
        with self.assertRaises(Exception):
            self.queue.first_item()

    def test_last_item_empty(self):
        with self.assertRaises(Exception):
            self.queue.last_item()


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_push(self):
        self.stack.push(10)
        self.assertEqual(self.stack.size(), 1)

    def test_pop(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.size(), 1)

    def test_peek(self):
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.peek(), 20)
        self.assertEqual(self.stack.size(), 2)

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())

    def test_size(self):
        self.assertEqual(self.stack.size(), 0)
        self.stack.push(10)
        self.assertEqual(self.stack.size(), 1)
        self.stack.push(20)
        self.assertEqual(self.stack.size(), 2)

    def test_pop_empty(self):
        with self.assertRaises(Exception):
            self.stack.pop()

    def test_peek_empty(self):
        with self.assertRaises(Exception):
            self.stack.peek()


class TestMap(unittest.TestCase):
    def setUp(self):
        self.map = Map()

    def test_put(self):
        self.map.put("key1", "value1")
        self.assertEqual(self.map.get("key1"), "value1")

    def test_update_existing(self):
        self.map.put("key1", "value1")
        self.map.put("key1", "new_value")
        self.assertEqual(self.map.get("key1"), "new_value")

    def test_get_nonexistent(self):
        self.assertIsNone(self.map.get("nonexistent_key"))

    def test_remove(self):
        self.map.put("key1", "value1")
        self.map.remove("key1")
        self.assertIsNone(self.map.get("key1"))

    def test_display(self):
        self.map.put("key1", "value1")
        self.map.put("key2", "value2")
        self.map.put("key3", "value3")
        expected_output = "key1: value1\nkey2: value2\nkey3: value3\n"

        # Redirect stdout to capture the printed output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.map.display()
        sys.stdout = sys.__stdout__  # Restore the original stdout

        self.assertEqual(captured_output.getvalue(), expected_output)


class TestSet(unittest.TestCase):
    def setUp(self):
        self.my_set = Set()

    def test_add_element(self):
        self.my_set.add(10)
        self.assertTrue(self.my_set.contains(10))
        self.assertEqual(self.my_set.size(), 1)

    def test_add_duplicate_element(self):
        self.my_set.add(10)
        self.my_set.add(20)
        self.my_set.add(10)  # Adding a duplicate
        self.assertEqual(self.my_set.size(), 2)

    def test_remove_element(self):
        self.my_set.add(10)
        self.my_set.remove(10)
        self.assertFalse(self.my_set.contains(10))
        self.assertEqual(self.my_set.size(), 0)

    def test_remove_nonexistent_element(self):
        self.my_set.add(10)
        self.my_set.remove(20)  # Removing a nonexistent element
        self.assertTrue(self.my_set.contains(10))
        self.assertEqual(self.my_set.size(), 1)

    def test_contains(self):
        self.my_set.add(10)
        self.assertTrue(self.my_set.contains(10))
        self.assertFalse(self.my_set.contains(20))

    def test_size(self):
        self.assertEqual(self.my_set.size(), 0)
        self.my_set.add(10)
        self.assertEqual(self.my_set.size(), 1)
        self.my_set.add(20)
        self.assertEqual(self.my_set.size(), 2)

    def test_display(self):
        expected_output = "[10, 20, 30]\n"
        self.my_set.add(10)
        self.my_set.add(20)
        self.my_set.add(30)

        # Redirect stdout to capture the printed output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.my_set.display()
        sys.stdout = sys.__stdout__  # Restore the original stdout

        self.assertEqual(captured_output.getvalue(), expected_output)


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.linked_list = LinkedList()

    def test_append(self):
        self.linked_list.append(10)
        self.assertTrue(self.linked_list.contains(10))
        self.assertEqual(len(self.linked_list), 1)  # Test size using len()

    def test_append_multiple_elements(self):
        self.linked_list.append(10)
        self.linked_list.append(20)
        self.linked_list.append(30)
        self.assertTrue(self.linked_list.contains(20))
        self.assertFalse(self.linked_list.contains(40))
        self.assertEqual(len(self.linked_list), 3)  # Test size using len()

    def test_remove_element(self):
        self.linked_list.append(10)
        self.linked_list.remove(10)
        self.assertFalse(self.linked_list.contains(10))
        self.assertEqual(len(self.linked_list), 0)  # Test size using len()

    def test_remove_nonexistent_element(self):
        self.linked_list.append(10)
        original_size = len(self.linked_list)
        self.linked_list.remove(20)  # Attempting to remove a nonexistent element
        self.assertTrue(self.linked_list.contains(10))
        self.assertEqual(len(self.linked_list), original_size)

    def test_contains(self):
        self.linked_list.append(10)
        self.assertTrue(self.linked_list.contains(10))
        self.assertFalse(self.linked_list.contains(20))

    def test_display(self):
        expected_output = "10 -> 20 -> 30 -> None\n"
        self.linked_list.append(10)
        self.linked_list.append(20)
        self.linked_list.append(30)

        # Redirect stdout to capture the printed output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.linked_list.display()
        sys.stdout = sys.__stdout__  # Restore the original stdout

        self.assertEqual(captured_output.getvalue(), expected_output)