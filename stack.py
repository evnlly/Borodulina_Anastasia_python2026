class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise ValueError("Empty")
        return self.items.pop()

    def peek(self):
        if not self.items:
            raise ValueError("Empty")
        return self.items[-1]

    def __len__(self):
        return len(self.items)

    def __bool__(self):
        return len(self.items) != 0

    def __contains__(self, item):
        return item in self.items

    def __repr__(self):
        return f"Stack({self.items})"