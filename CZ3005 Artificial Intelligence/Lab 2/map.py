from typing import List, Tuple
from pyswip import Prolog

from knawledge import Knawledge, Perception


class Cell():
    coordinates: Tuple[int, int]
    grid: List[List[str]]

    def __init__(self) -> None:
        super().__init__()
        self.known_wall: bool = False
        self.elements: dict = {
            "glitter": "off",
            "wumpus": "off",
            "stench": "off",
            "confounded": "off",
            "portal": "off",
            "tingle": "off",
            "bump": "off",
            "scream": "off",
            "wall": "off",
        }
        self.set_empty_cell()
        pass

    def set_empty_cell(self, char=None):
        self.grid = [['.', '.', '.'], [' ', '?', ' '], ['.', '.', '.']]

    def clear_dynamic_perceptions(self):
        """Clears only parts of the cell that changes every update
        """
        self.grid[1] = [' ', '?', ' ']
        self.grid[2][0] = '.'
        self.grid[2][1] = '.'

    def set_wall(self):
        self.grid = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]
        self.elements["wall"] = "on"

    def set_percept_confounded(self):
        self.grid[0][0] = '%'

    def set_percept_stench(self):
        self.grid[0][1] = '='

    def set_percept_tingle(self):
        self.grid[0][2] = 'T'

    def set_percept_agent(self, dir: str):
        self.grid[1][0] = '−'
        self.grid[1][2] = '−'

        if dir == "rnorth":
            self.grid[1][1] = '∧'
        if dir == "reast":
            self.grid[1][1] = '>'
        if dir == "rsouth":
            self.grid[1][1] = 'V'
        if dir == "rwest":
            self.grid[1][1] = '<'

    def set_percept_wumpus(self):
        self.grid[1][1] = 'W'

    def set_percept_portal(self):
        self.grid[1][1] = 'O'

    def set_percept_u(self):
        self.grid[1][1] = 'U'

    def set_percept_safe(self):
        self.grid[1][1] = 's'

    def set_percept_visited(self):
        self.grid[1][1] = 'S'

    def set_percept_glitter(self):
        self.grid[2][0] = '*'

    def set_percept_bump(self):
        self.known_wall = True
        self.grid[2][1] = 'B'

    def clear_percept_bump(self):
        self.grid[2][1] = '.'

    def set_percept_scream(self):
        self.grid[2][2] = '@'

    def pickup(self):
        self.grid[2][0] = '.'
        self.elements["glitter"] = "off"

    def get_line(self, i: int):
        return self.grid[i]


class Map():
    N: int
    M: int
    rel_map_size: List[int] = [3, 3]
    agent_start: List[int]
    agent_pos: List[int]
    agent_abs_dir: str
    agent_angle_offset: int = 0
    bumped: bool

    cells: List[List[Cell]]

    def __init__(self, N: int, M: int, dir: str) -> None:
        super().__init__()
        self.N = N
        self.M = M
        self.agent_abs_dir = dir
        self.bumped = False

        self.init_map()

    def init_map(self):
        self.create_map()
        self.draw_walls()

    def create_map(self):
        self.cells = []

        for y in range(self.M):
            row = []
            for x in range(self.N):
                cell = Cell()
                cell.coordinates = (x, y)
                row.append(cell)
            self.cells.append(row)

    def draw_walls(self):
        for row in range(self.M):
            for col in range(self.N):
                if row == 0 or row == (self.M-1):
                    self.cells[row][col].set_wall()
                if col == 0 or col == (self.N-1):
                    self.cells[row][col].set_wall()

    def reset_map(self):
        for row in range(self.M):
            for col in range(self.N):
                cell = self.cells[row][col]
                if cell.elements["wall"] != "on":
                    cell.elements["confounded"] = "off"
                    cell.set_empty_cell()

    def reposition_agent(self, X: int, Y: int):
        self.reset_map()
        self.rel_map_size = [3, 3]
        self.agent_start = [X, Y]
        self.agent_pos = [X, Y]
        self.cells[Y][X].elements["confounded"] = "on"

        # angle offset is based on clockwise direction
        # so if currently facing east and enter a portal,
        # offset of relative to absolute direction is 90 degrees after repositioning
        dirs = ["rnorth", "reast", "rsouth", "rwest"]
        self.agent_angle_offset += dirs.index(self.agent_abs_dir) * 90
        self.agent_angle_offset %= 360

    def add_coin(self, X: int, Y: int):
        cell = self.cells[Y][X]
        cell.elements["glitter"] = "on"

    def add_wall(self, X: int, Y: int):
        cell = self.cells[Y][X]
        cell.set_wall()

    def add_wumpus(self, X: int, Y: int):
        cell = self.cells[Y][X]
        cell.elements["wumpus"] = "on"
        self.set_adjacent_element(X, Y, "stench")

    def add_portal(self, X: int, Y: int):
        cell = self.cells[Y][X]
        cell.elements["portal"] = "on"
        self.set_adjacent_element(X, Y, "tingle")

    def clear_bumps(self):
        self.bumped = False

    def set_adjacent_element(self, X: int, Y: int, element):
        self.cells[Y-1][X].elements[element] = "on"
        self.cells[Y][X-1].elements[element] = "on"
        self.cells[Y][X+1].elements[element] = "on"
        self.cells[Y+1][X].elements[element] = "on"

    def do_action(self, action: str):
        """Updates map according to action generated

        Args:
            action (str): Action the agent will take
        """

        if action == "pickup":
            cell = self.cells[self.agent_pos[1]][self.agent_pos[0]]
            cell.pickup()

        elif action == "moveforward":
            prev_pos = self.agent_pos.copy()

            if self.agent_abs_dir == "rnorth":
                self.agent_pos[1] -= 1
            elif self.agent_abs_dir == "reast":
                self.agent_pos[0] += 1
            elif self.agent_abs_dir == "rsouth":
                self.agent_pos[1] += 1
            elif self.agent_abs_dir == "rwest":
                self.agent_pos[0] -= 1

            # checks for wall collision
            cell = self.cells[self.agent_pos[1]][self.agent_pos[0]]
            if cell.elements["wall"] == "on":
                self.agent_pos = prev_pos
                self.bumped = True
                cell = self.cells[self.agent_pos[1]][self.agent_pos[0]]
                cell.set_percept_bump()

            # check if relative map needs resizing
            dx = abs(abs(self.agent_pos[0]) - self.agent_start[0])
            dy = abs(abs(self.agent_pos[1]) - self.agent_start[1])

            # because expansion of relative map depends on relative x/y width explored
            if self.agent_angle_offset % 180 == 0:
                self.rel_map_size[0] = max(dx*2 + 3, self.rel_map_size[0])
                self.rel_map_size[1] = max(dy*2 + 3, self.rel_map_size[1])
            else:
                self.rel_map_size[1] = max(dx*2 + 3, self.rel_map_size[1])
                self.rel_map_size[0] = max(dy*2 + 3, self.rel_map_size[0])

        elif action == "turnleft":
            if self.agent_abs_dir == "rnorth":
                self.agent_abs_dir = "rwest"
            elif self.agent_abs_dir == "reast":
                self.agent_abs_dir = "rnorth"
            elif self.agent_abs_dir == "rsouth":
                self.agent_abs_dir = "reast"
            elif self.agent_abs_dir == "rwest":
                self.agent_abs_dir = "rsouth"

        elif action == "turnright":
            if self.agent_abs_dir == "rnorth":
                self.agent_abs_dir = "reast"
            elif self.agent_abs_dir == "reast":
                self.agent_abs_dir = "rsouth"
            elif self.agent_abs_dir == "rsouth":
                self.agent_abs_dir = "rwest"
            elif self.agent_abs_dir == "rwest":
                self.agent_abs_dir = "rnorth"

    def check_portal(self) -> bool:
        cell = self.cells[self.agent_pos[1]][self.agent_pos[0]]
        return cell.elements["portal"] == "on"

    def get_cell_perceptions(self) -> Perception:
        """Retrives current perceptions L of the agent
        """

        cell = self.cells[self.agent_pos[1]][self.agent_pos[0]]
        perception = Perception()

        if cell.elements["confounded"] == "on":
            perception.enable_perception(Perception.CONFOUNDED)
        if cell.elements["stench"] == "on":
            perception.enable_perception(Perception.STENCH)
        if cell.elements["tingle"] == "on":
            perception.enable_perception(Perception.TINGLE)
        if cell.elements["glitter"] == "on":
            perception.enable_perception(Perception.GLITTER)
        if self.bumped:
            perception.enable_perception(Perception.BUMP)
        if cell.elements["scream"] == "on":
            perception.enable_perception(Perception.SCREAM)

        return perception

    def update_map_with_perceptions(self, prolog: Prolog, ref: List[int], abs_dir: bool):
        """Adds to the map the current perceptions of the agent

        Args:
            prolog (Prolog): The initialised prolog file of agent
            ref (List[int]): Reference coordinate that the X and Y offsets are based off of
                             Eg (ref = [3, 3] means that a relative coordinate of (1, 3) is (4, 6) 
                             if initial relative and absolute direction are the same)
        """

        knawledge = Knawledge(prolog)

        for kb in knawledge.kb:
            for data in kb["data"]:
                # relative X and Y positions may not correspond with absolute X and Y positions
                # so adjust accordingly

                # both directions are the same
                if self.agent_angle_offset == 0:
                    X = ref[0] + data['X']
                    Y = ref[1] - data['Y']

                # eg. relative = rnorth, absolute = rsouth
                elif self.agent_angle_offset == 180:
                    X = ref[0] - data['X']
                    Y = ref[1] + data['Y']

                # eg. relative = rnorth, absolute = reast
                elif self.agent_angle_offset == 90:
                    X = ref[0] + data['Y']
                    Y = ref[1] + data['X']

                # eg. relative = rnorth, absolute = rwest
                elif self.agent_angle_offset == 270:
                    X = ref[0] - data['Y']
                    Y = ref[1] - data['X']

                cell = self.cells[Y][X]

                # no need to update walls
                if cell.elements["wall"] == "on":
                    continue

                if kb["type"] == Knawledge.VISITED:
                    cell.set_percept_visited()
                elif kb["type"] == Knawledge.SAFE:
                    cell.set_percept_safe()
                elif kb["type"] == Knawledge.WUMPUS:
                    cell.set_percept_wumpus()
                elif kb["type"] == Knawledge.STENCH:
                    cell.set_percept_stench()
                elif kb["type"] == Knawledge.CONFOUNDED:
                    cell.set_percept_confounded()
                elif kb["type"] == Knawledge.CONFUNDUS:
                    cell.set_percept_portal()
                elif kb["type"] == Knawledge.TINGLE:
                    cell.set_percept_tingle()
                elif kb["type"] == Knawledge.GLITTER:
                    cell.set_percept_glitter()
                elif kb["type"] == Knawledge.U:
                    cell.set_percept_u()
                elif kb["type"] == Knawledge.WALL:
                    cell.set_wall()
                elif kb["type"] == Knawledge.AGENT:
                    if abs_dir:
                        cell.set_percept_agent(self.agent_abs_dir)
                    else:
                        cell.set_percept_agent(data["Dir"])
                    if self.bumped:
                        cell.set_percept_bump()

    def reset_absolute_map(self, full_clear: bool = False):
        """Clears all of the cell drawing back to an empty map
        """
        for row in self.cells:
            for cell in row:
                if cell.elements["wall"] == "on":
                    cell.set_wall()
                else:
                    if full_clear:
                        cell.set_empty_cell()
                    else:
                        cell.clear_dynamic_perceptions()

    def generate_relative_map(self, prolog: Prolog):
        """Creates a relative map based on agent perceptions

        Args:
            prolog (Prolog): The initialised prolog file of agentv

        Returns:
            RelativeMap: The relative map with drawn cells
        """

        r_map = RelativeMap(*self.rel_map_size, self.bumped)
        r_map.update_map_with_perceptions(prolog, r_map.center, False)
        return r_map

    def print_relative_map(self, prolog: Prolog):
        r_map = self.generate_relative_map(prolog)
        r_map.print_map()

    def print_absolute_map(self, prolog: Prolog):
        self.reset_absolute_map(full_clear=False)
        self.update_map_with_perceptions(prolog, self.agent_start, True)
        self.print_map()

    def update_map_with_data(self):
        """Draws map with absolute data
        """
        for row in self.cells:
            for cell in row:
                # don't update if it's a wall
                if cell.elements["wall"] == "on":
                    continue

                if cell.elements["wumpus"] == "on":
                    cell.set_percept_wumpus()
                if cell.elements["stench"] == "on":
                    cell.set_percept_stench()
                if cell.elements["portal"] == "on":
                    cell.set_percept_portal()
                if cell.elements["tingle"] == "on":
                    cell.set_percept_tingle()
                if cell.elements["glitter"] == "on":
                    cell.set_percept_glitter()

    def draw_agent(self):
        cell = self.cells[self.agent_pos[1]][self.agent_pos[0]]
        cell.set_percept_agent(self.agent_abs_dir)

    def print_init_map(self):
        """Prints initial absolute map
        """
        self.reset_absolute_map(full_clear=True)
        self.update_map_with_data()
        self.draw_agent()
        self.print_map()

    def print_map(self):
        print('-' * (6*self.N+1))
        for row in self.cells:
            line_0 = [cell.get_line(0) for cell in row]
            line_1 = [cell.get_line(1) for cell in row]
            line_2 = [cell.get_line(2) for cell in row]

            print('|', end='')
            for cell in line_0:
                print(" ".join(cell), end='|')
            print("\n|", end='')
            for cell in line_1:
                print(" ".join(cell), end='|')
            print("\n|", end='')
            for cell in line_2:
                print(" ".join(cell), end='|')
            print('')
            print('-' * (6*self.N+1))


class RelativeMap(Map):
    center: List[int]

    def __init__(self, N, M, bumped):
        self.N = N
        self.M = M
        self.agent_angle_offset = 0
        self.center = [N//2, M//2]
        self.bumped = bumped

        self.create_map()

    def create_map(self):
        self.cells = []
        for y in range(self.M):
            row = []
            for x in range(self.N):
                cell = Cell()
                cell.coordinates = (x, y)
                row.append(cell)
            self.cells.append(row)
