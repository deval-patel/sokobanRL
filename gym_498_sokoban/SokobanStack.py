from typing import List


class SokobanStack:
    """
    A stack implementation to store SokobanBoards.
    """
    stack: List[List[List[str]]]

    def __init__(self) -> None:
        """
        Initialize this SokobanStack.
        """
        self.stack = []

    def push(self, board: List[List[str]]) -> None:
        """
        Add an element to this SokobanStack.
        """
        self.stack.append(board)

    def pop(self) -> List[List[str]]:
        """
        Pops and returns the element at the top of this SokobanStack if it is not empty.

        @return the board at the top of this SokobanStack if the SokobanStack is not empty, None otherwise.
        """
        if self.empty():
            return None
        return self.stack.pop()

    def empty(self) -> bool:
        """
        Returns whether this SokobanStack is empty or not.

        @return true if it is empty, false otherwise.
        """
        return len(self.stack) == 0

    def size(self) -> int:
        """
        Returns the size of this SokobanStack.

        @return the size of this SokobanStack.
        """
        return len(self.stack)

    def top(self) -> List[List[str]]:
        """
        Returns the element at the top of this SokobanStack.

        @return the element at the top of this SokobanStack.
        """
        if self.empty():
            return None
        return self.stack[self.size() - 1]
