class DoubleLinkedList():
    def __init__(self, data):
        self.next = None
        self.prev = None
        self.data = data
    def insert_middle(self, prev_node, data):
        if prev_node is None:
            return
        new_node = DoubleLinkedList(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node
        if new_node.next is not None:
            new_node.next.prev = new_node
