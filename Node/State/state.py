import copy

class State:
    rows: int
    columns: int
    grid: list
    bugs: set

    def __init__(self, rows=None, columns=None, grid=None, bugs=None):

        """
        Initialize the State.

        :param rows: Number of rows in the grid.
        :param columns: Number of columns in the grid.
        :param grid: The grid representing the state.
        :param bugs: List of bug positions.
        """
        if rows is not None and columns is not None and grid is not None and bugs is not None:
            self.rows = rows
            self.columns = columns
            self.grid = grid
            self.bugs = bugs
        else:
            # self.rows, self.columns, self.grid, self.bugs = self.get_state_info()
            self.rows, self.columns, self.grid, self.bugs = self.get_state_info_json()

    def __eq__(self, other):
        if isinstance(other, State):
            return (
                    self.rows == other.rows and
                    self.columns == other.columns and
                    self.grid == other.grid and
                    self.bugs == other.bugs
            )
        return False

    def __hash__(self):
        return hash((self.rows, self.columns, tuple(tuple(row) for row in self.grid), frozenset(self.bugs)))

    def get_state_info(self):
        """
        Get state information from user input.
        """
        try:
            rows = int(input("Enter rows: "))
            columns = int(input("Enter columns: "))
            grid = []

            print('Enter the grid rows from top to bottom:')
            for i in range(rows):
                print(f"Row {i + 1}: ")
                grid.append(list(input()))

            bugs = self.parse_grid(grid)
            return rows, columns, grid, bugs
        except Exception as e:
            print(f"Error in input: {e}")
            return self.get_state_info()

    def get_state_info_json(self):
        import json
        with open('level.json') as f:
            data = json.load(f)
            sgrid = data['grid']
            grid = [list(row) for row in sgrid]
            # print(grid)
            rows = len(grid)
            columns = len(grid[0])
            bugs = self.parse_grid(grid)
        return rows, columns, grid, bugs

    def parse_grid(self, grid):
        """
        Parse the grid to find bug positions.
        """
        bugs = set()
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 'B':
                    bugs.add((i, j))
        return bugs

    def print_grid(self):
        """
        Print the grid.
        █▄▀░
        """

        print('grid:\n')
        for row in self.grid:
            # print(row)
            for cell in row:
                # print(cell)
                if cell == '#':
                    print('█', end='')
                elif cell == ' ':
                    print('░', end='')
                elif cell == '*':
                    print('*', end='')
                else:
                    print('©', end='')
            print('')

        print('\n bugs:\n')
        print(self.bugs)
        print('\n----')

    def is_goal_state(self):
        """
        Check if the current state is the goal state.
        """
        return not any('*' in row for row in self.grid)

    def calculate_next_state(self, bug, target):
        """
        Calculate the next state after moving a bug to the target position.
        """
        r, c = bug
        tr, tc = target

        # Create a new cloned state
        new_state = copy.deepcopy(self)

        # Remove bug from initial position
        new_state.grid[r][c] = ' '
        new_state.bugs.remove(bug)

        # Put bug on target location
        if new_state.grid[tr][tc] == '*':
            new_state.grid[tr][tc] = ' '

        else:
            new_state.grid[tr][tc] = 'B'
            new_state.bugs.add((tr, tc))

        return new_state

    def get_neighbouring_states(self):
        """
        Get neighbouring states by moving each bug in possible directions.
        """
        neighbours = []

        for bug in self.bugs:
            # Directions: up, down, left, right
            candidates = [
                ('up', (bug[0] - 1, bug[1])),
                ('down', (bug[0] + 1, bug[1])),
                ('left', (bug[0], bug[1] - 1)),
                ('right', (bug[0], bug[1] + 1))
            ]
            for direction, (r, c) in candidates:
                if 0 <= r < self.rows and 0 <= c < self.columns:
                    if self.grid[r][c] == '*' or self.grid[r][c] == ' ':
                        action = (bug, direction)
                        new_state = self.calculate_next_state(bug, (r, c))
                        neighbours.append((action, new_state))

        return neighbours
