import copy


class State:

    def __init__(self, *args):

        # rows, columns, grid, bugs in order

        if len(args) == 5:
            self.rows = args[0]
            self.columns = args[1]
            self.grid = args[2]
            self.bugs = args[3]

        elif len(args) == 0:
            self.rows, self.columns, self.grid, self.bugs = self.get_state_info()

    def get_state_info(self):
        rows = int(input("enter rows:"))
        columns = int(input("enter columns:"))
        grid = []

        print('enter the grid rows from top to bottom:')
        for i in range(rows):
            print(f"row {i + 1}:      ")
            grid.append(input())

        bugs = self.parse_grid(grid)
        return rows, columns, grid, bugs

    def parse_grid(self, grid):

        bugs = []
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 'B':
                    bug = i, j
                    bugs.append(bug)

        return bugs

    def print_grid(self):

        for row in self.grid:
            print(row)
        print()

    def is_goal_state(self):
        return not any('*' in row for row in self.grid)

    def calculate_next_state(self, bug, target):
        r, c = bug
        tr, tc = target

        # create a new clone state
        new_state = copy.deepcopy(self)

        # remove bug from initial position
        new_state.grid[r][c] = ' '

        # put bug on target location
        if new_state.grid[tr][tc] == '*':
            new_state.grid[tr][tc] = ' '
        else:
            new_state.grid[tr][tc] = 'B'

        return new_state

    def get_neighbouring_states(self):

        # list of (action, state)
        neighbours = []

        for bug in self.bugs:
            # remove everything other than up down right left, because later we need to do this for bugs like spiders
            candidates = [
                'up', (bug[0] - 1, bug[1]),
                'down', (bug[0] + 1, bug[1]),
                'left', (bug[0], bug[1] - 1),
                'right', (bug[0], bug[1] + 1)
            ]
            for dir, (r, c) in candidates:
                if self.grid[r][c] == '*' or self.grid[r][c] == ' ':
                    action = bug, dir
                    new_state = self.calculate_next_state(bug, (r, c))
                    neighbour = action, new_state
                    neighbours.append(neighbour)

        return neighbours
