class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return isinstance(other, Node) and self.position == other.position

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f