import sys
from collections import deque
from Node import Node

'''

    1) Initial state
    2) Goal State
    3) Actions
    4) Transition Model
    5) Path Cost Function

'''


def neighbours(state):
    return state.get_neighbouring_states()


class Solver:

    def __init__(self, start_node):
        self.start_node = start_node

        # currently not making queue into another class, but later I can.
        # to make custom functions like - contains_state() etc
        self.queue = deque()
        self.queue.append(self.start_node)

        self.explored_states = set()
        self.explored_states_count = 0
        self.solution = None

    def solve(self):
        print("inside solve ")
        while True:
            if len(self.queue) == 0:
                raise Exception("no solution")

            node = self.queue.popleft()
            self.explored_states_count += 1

            if node.state.is_goal_state():
                actions = []
                states = []

                while node != self.start_node:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)
                return

            self.explored_states.add(node.state)
            for action, state in neighbours(node.state):
                child = Node(state=state, parent=node, action=action)
                self.queue.append(child)


if __name__ == '__main__':
    # print(sys.argv)
    start_node = Node
    Solver(start_node)
