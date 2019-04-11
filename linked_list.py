
class LinkedList:
    """
    Linked-List.
    """

    class Element:
        """
        Linked-List element.
        """

        def __init__(self, value):
            """
            Generates a linked-list element with
            the given value.
            """
            self.value = value
            self.prev = None
            self.next = None


    def __init__(self):
        """
        Generates an empty linked-list.
        """
        self.head = None
        self.tail = None


    def add(self, value):
        """
        Inserts value into the linked-list.
        """
        if self.tail == None:
            self.head = self.tail = self.Element(value)

        else:
            self.tail.next = self.Element(value)
            self.tail.next.prev = self.tail
            self.tail = self.tail.next


    def moveToFront(self, element):
        """
        Moves element to the front of the linked-list.
        """
        if element is self.head:
            return

        element.prev.next = element.next

        if element is self.tail:
            self.tail = element.prev

        else:
            element.next.prev = element.prev

        self.head.prev = element
        element.next = self.head
        element.prev = None
        self.head = element

