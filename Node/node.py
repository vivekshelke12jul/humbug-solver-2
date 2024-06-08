from Node.State.state import State

class Node:
    def __init__(self, state=None, parent=None, action=None, depth=0):
        """
        Initialize a Node.

        :param state: The state associated with this node.
        :param parent: The parent node.
        :param action: The action taken to reach this node from the parent.
        """
        self.state = state if state is not None else State()
        self.parent = parent
        self.action = action
        self.depth = depth

    def __repr__(self):
        return f"Node(state={self.state}, action={self.action}, parent={self.parent}, depth={self.depth})"
