class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.length += 1  # Increment the length when appending

    def remove(self, data):
        if not self.head:
            return

        if self.head.data == data:
            self.head = self.head.next
            self.length -= 1  # Decrement the length when removing
            return

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.length -= 1  # Decrement the length when removing
                return
            current = current.next

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def contains(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def __len__(self):
        return self.length


class Set:
    def __init__(self):
        self.elements = []

    def add(self, element):
        if element not in self.elements:
            self.elements.append(element)

    def remove(self, element):
        if element in self.elements:
            self.elements.remove(element)

    def contains(self, element):
        return element in self.elements

    def size(self):
        return len(self.elements)

    def display(self):
        print(self.elements)


class Map:
    def __init__(self):
        self.entries = []

    def put(self, key, value):
        # Check if the key already exists, and update the value if it does
        for i, (existing_key, existing_value) in enumerate(self.entries):
            if existing_key == key:
                self.entries[i] = (key, value)
                return
        # Key doesn't exist, so add a new key-value pair
        self.entries.append((key, value))

    def get(self, key):
        for existing_key, existing_value in self.entries:
            if existing_key == key:
                return existing_value
        return None  # Key not found

    def remove(self, key):
        for i, (existing_key, existing_value) in enumerate(self.entries):
            if existing_key == key:
                del self.entries[i]
                return
        # Key not found, raise an exception or handle it in your desired way

    def display(self):
        for key, value in self.entries:
            print(f"{key}: {value}")


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise Exception("Stack is empty")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise Exception("Stack is empty")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise Exception("Queue is empty")

    def first_item(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise Exception("Queue is empty")

    def last_item(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise Exception("Queue is empty")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


