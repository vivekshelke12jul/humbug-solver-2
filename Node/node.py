from Node.State import State


class Node:

    def __init__(self, *args):
        # state, parent, action in order

        if len(args) == 3:
            self.state = args[0]
            self.parent = args[1]
            self.action = args[2]
        elif len(args) == 0:
            self.state = State
            self.parent = None
            self.action = None
