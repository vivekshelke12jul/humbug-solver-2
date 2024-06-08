import sys
import logging
from collections import deque
from Node.node import Node
from Node.State.state import State


def neighbours(state):
    return state.get_neighbouring_states()


class Solver:
    def __init__(self, start_node):
        self.start_node = start_node
        self.queue = deque([self.start_node])
        self.explored_states = set()
        self.explored_states_count = 0
        self.solution = None

    def solve(self):
        print("Inside solve")
        while self.queue:

            node = self.queue.popleft()
            print(f"depth={node.depth}")

            node.state.print_grid()
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
                if state not in self.explored_states:
                    child = Node(state=state, parent=node, action=action, depth=node.depth + 1)
                    self.explored_states.add(child.state)
                    self.queue.append(child)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, filename='root.log', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s')
    logging.info('from root logger')

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s')
    handler = logging.FileHandler(f"{__name__}.log", mode='w')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info("from child logger")

    #for logging: https://www.youtube.com/watch?v=urrfJgHwIJA


    initial_state = State()  # Get initial state from user input
    start_node = Node(state=initial_state)

    solver = Solver(start_node)
    try:
        solver.solve()
        for i, state in enumerate(solver.explored_states):
            print(f"explored_state_no: {i}")
            state.print_grid()
        if solver.solution:
            actions, states = solver.solution
            print("Solution found:")
            print("Actions:", actions)
            print("States:")
            for state in states:
                state.print_grid()
        else:
            print("No solution found")
    except Exception as e:
        print(str(e))
