import sys

from typing import Dict, List, Tuple
from pyswip import *


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

    def set_percept_npc(self):
        self.grid[1][0] = '−'
        self.grid[1][2] = '−'

    def set_percept_agent(self, dir: str):
        self.set_percept_npc()

        if dir == "rnorth":
            self.grid[1][1] = '∧'
        if dir == "reast":
            self.grid[1][1] = '>'
        if dir == "rsouth":
            self.grid[1][1] = 'V'
        if dir == "rwest":
            self.grid[1][1] = '<'

    def set_percept_wumpus(self):
        self.set_percept_npc()
        self.grid[1][1] = 'W'

    def set_percept_portal(self):
        self.set_percept_npc()
        self.grid[1][1] = 'O'

    def set_percept_u(self):
        self.set_percept_npc()
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
    scream: bool

    cells: List[List[Cell]]
    wumpus_pos = List[int]

    def __init__(self, N: int, M: int, dir: str) -> None:
        super().__init__()
        self.N = N
        self.M = M
        self.agent_abs_dir = dir
        self.bumped = False
        self.scream = False

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
        self.wumpus_pos = [X, Y]
        cell = self.cells[Y][X]
        cell.elements["wumpus"] = "on"
        self.set_adjacent_element(X, Y, "stench")

    def add_portal(self, X: int, Y: int):
        cell = self.cells[Y][X]
        cell.elements["portal"] = "on"
        self.set_adjacent_element(X, Y, "tingle")

    def clear_transient_indicators(self):
        self.bumped = False
        self.scream = False

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

        elif action == "shoot":
            ax, ay = self.agent_pos
            adir = self.agent_abs_dir
            wx, wy = self.wumpus_pos

            self.scream = (
                ay == wy and ax > wx and adir == "rwest" or
                ay == wy and ax < wx and adir == "reast" or
                ay > wy and ax == wx and adir == "rnorth" or
                ay < wy and ax == wx and adir == "rsouth"
            )

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

    def get_cell_perceptions(self):
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
        if self.scream:
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


class Knawledge():
    AGENT = 0
    VISITED = 1
    WUMPUS = 2
    CONFUNDUS = 3
    TINGLE = 4
    GLITTER = 5
    STENCH = 6
    SAFE = 7
    U = 8
    CONFOUNDED = 9
    WALL = 10
    BUMP = 11

    def __init__(self, prolog: Prolog):
        agent = {
            "data": list(prolog.query("current(X, Y, Dir)")),
            "type": self.AGENT
        }

        visited = {
            "data": list(prolog.query("visited(X, Y)")),
            "type": self.VISITED
        }

        wumpus = {
            "data": list(prolog.query("wumpus(X, Y)")),
            "type": self.WUMPUS
        }

        confundus = {
            "data": list(prolog.query("confundus(X, Y)")),
            "type": self. CONFUNDUS
        }

        tingle = {
            "data": list(prolog.query("tingle(X, Y)")),
            "type": self.TINGLE
        }

        glitter = {
            "data": list(prolog.query("glitter(X, Y)")),
            "type": self.GLITTER
        }

        confounded = {
            "data": list(prolog.query("confounded(X, Y)")),
            "type": self.CONFOUNDED
        }

        stench = {
            "data": list(prolog.query("stench(X, Y)")),
            "type": self.STENCH
        }

        safe = {
            "data": list(prolog.query("safe(X, Y)")),
            "type": self.SAFE
        }

        u = {
            "data": list(prolog.query("wumpus(X, Y), confundus(X, Y)")),
            "type": self.U
        }

        wall = {
            "data": list(prolog.query("wall(X, Y)")),
            "type": self.WALL
        }

        self.kb = [
            wumpus, confundus, u, tingle, glitter, confounded,
            stench, safe, visited, wall, agent
        ]


class Perception():
    CONFOUNDED = 0
    STENCH = 1
    TINGLE = 2
    GLITTER = 3
    BUMP = 4
    SCREAM = 5

    full_printout = ["Confounded", "Stench", "Tingle",
                     "Glitter", "Bump", "Scream"]

    short_printout = ['C', 'S', 'T', 'G', 'B', 'S']

    query_list: List[str]
    sense_printout: List[str]

    def __init__(self):
        self.query_list = ["off", "off", "off", "off", "off", "off"]
        self.sense_printout = ['C', 'S', 'T', 'G', 'B', 'S']

    def enable_perception(self, type: int):
        self.query_list[type] = "on"
        self.sense_printout[type] = self.full_printout[type]

    def disable_perception(self, type: int):
        self.query_list[type] = "off"
        self.sense_printout[type] = self.short_printout[type]

    def get_query_str(self) -> str:
        return ",".join(self.query_list)

    def get_sense_printout(self) -> str:
        return "-".join(self.sense_printout)


def setup_map(N: int, M: int) -> Map:
    a_map = Map(N, M, "rnorth")
    a_map.reposition_agent(3, 3)

    a_map.add_wumpus(5, 4)

    a_map.add_coin(2, 3)
    a_map.add_coin(3, 2)

    a_map.add_portal(2, 1)
    a_map.add_portal(4, 1)
    a_map.add_portal(4, 4)

    return a_map


def setup_prolog(filename: str, a_map: Map) -> Prolog:
    # initialise prolog file
    prolog = Prolog()
    prolog.consult(filename)
    list(prolog.query("reborn"))

    # send initial perceptions to agent
    perceptions = a_map.get_cell_perceptions()
    list(prolog.query(f"reposition([{perceptions.get_query_str()}])"))

    return prolog


def make_action(prolog: Prolog, a_map: Map, action: str = None,
                print_map: bool = True, print_rel: bool = False, print_abs: bool = False):
    # preemptively clears bumps to prevent old bumps from showing
    a_map.clear_transient_indicators()

    # updates map with action
    a_map.do_action(action)

    # get new perceptions from cell after action
    perceptions = a_map.get_cell_perceptions()

    # update agent with new perceptions
    query_str = f"action({action}, [{perceptions.get_query_str()}])"
    print(query_str)
    list(prolog.query(query_str))

    # reposition if stepped on a confundus portal
    if a_map.check_portal():
        print("Agent stepped on a portal")
        a_map.reposition_agent(1, 4)
        perceptions = a_map.get_cell_perceptions()
        list(prolog.query(f"reposition([{perceptions.get_query_str()}])"))

    # print out map and relevant info
    if print_map:
        print(f"[Driver] {perceptions.get_sense_printout()}")
        if print_abs:
            a_map.print_absolute_map(prolog)
        if print_rel:
            a_map.print_relative_map(prolog)


# continues using explore/1 until no safe cells are left
def auto_explore(prolog: Prolog, a_map: Map):
    path_exists = True

    # keep calling explore/1 until there isn't anymore valid paths for it
    # means all safe cells are visited, no gold on the floor and agent is at (0, 0)
    while path_exists:
        L = list(prolog.query("explore(L)"))
        path_exists = handle_explore_result(prolog, a_map, L)

    print("[Driver] Nothing from explore/1 anymore...")
    t = list(prolog.query("safe(X,Y), \+visited(X,Y)"))
    return


def handle_explore_result(prolog: Prolog, a_map: Map, L: List[Dict[str, List[Atom]]]) -> bool:
    if len(L) == 0:
        return False

    # apply actions generated from explore/1
    actions = L[0]['L']
    for action in actions[:-1]:
        make_action(prolog, a_map, action)
    make_action(prolog, a_map, actions[-1])

    return True


def printout_glitter_visited_safe():
    a_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", a_map)

    print("===[Complete Absolute Map]===")
    a_map.print_init_map()

    print("===[Testing glitter/2, safe/2, visited/2 and pickup]===")
    print("Moving agent to (0, 1) first")
    make_action(prolog, a_map, "moveforward", )
    print("Agent now picks up the coin")
    make_action(prolog, a_map, "pickup", )
    print("The glitter indicator on (0, 1) should now be gone")
    print("Now moving agent to (-1, 0), only printing relative map for last action")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "moveforward")
    print("Agent now picks up the second coin")
    make_action(prolog, a_map, "pickup")
    print("The glitter indicator on (-1, 0) should now be gone")

    safe = list(prolog.query("safe(X, Y)"))
    visited = list(prolog.query("visited(X, Y)"))

    safe = [f"({cell['X']}, {cell['Y']})" for cell in safe]
    visited = [f"({cell['X']}, {cell['Y']})" for cell in visited]

    print("safe/2 and visited/2 outputs should match the relative map")
    print(f"Safe cells: {', '.join(safe)}")
    print(f"Visited cells: {', '.join(visited)}")
    print("\n")


def printout_confundus_tingle():
    a_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", a_map)

    print("===[Complete Absolute Map]===")
    a_map.print_init_map()

    print("===[Testing confundus/2 and tingle/2]===")
    print("Moving agent to (-1, 1) first")
    make_action(prolog, a_map, "turnleft")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "moveforward")
    print("Tingle indicator should show and portals should surround the player")
    print("But cells that are safe or visited should not be portals")
    print("Now moving agent to (0, -2)")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "turnleft")
    make_action(prolog, a_map, "moveforward")

    confundus = list(prolog.query("confundus(X, Y)"))
    tingle = list(prolog.query("tingle(X, Y)"))

    confundus = [f"({cell['X']}, {cell['Y']})" for cell in confundus]
    tingle = [f"({cell['X']}, {cell['Y']})" for cell in tingle]

    print("confundus/2 and tingle/2 outputs should match the relative map")
    print(f"Confundus cells: {', '.join(confundus)}")
    print(f"Tingle cells: {', '.join(tingle)}")
    print("\n")


def printout_wumpus_stench_bump_current():
    a_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", a_map)

    print("===[Complete Absolute Map]===")
    a_map.print_init_map()

    print("===[Testing wumpus/2, stench/2, wall/2, bump, scream and shoot]===")
    print("Now moving agent to (2, 0)")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "moveforward")
    print("Stench indicator should show and wumpus should surround the player")
    print("But cells that are safe or visited should not be wumpuses (wumpi?)")
    print("Now we move the agent to (3, 0) which is a wall")
    make_action(prolog, a_map, "moveforward")
    print("The bump indicator should show and (3, 0) should update to be a wall")

    wumpus = list(prolog.query("wumpus(X, Y)"))
    stench = list(prolog.query("stench(X, Y)"))
    wall = list(prolog.query("wall(X, Y)"))

    wumpus = [f"({cell['X']}, {cell['Y']})" for cell in wumpus]
    stench = [f"({cell['X']}, {cell['Y']})" for cell in stench]
    wall = [f"({cell['X']}, {cell['Y']})" for cell in wall]

    print("wumpus/2, stench/2 and wall/2 outputs should match the relative map")
    print(f"Wumpus cells: {', '.join(wumpus)}")
    print(f"Stench cells: {', '.join(stench)}")
    print(f"Wall cells: {', '.join(wall)}")

    print("We now want to check if our agent has the arrow")
    arrow = list(prolog.query("hasarrow"))
    print("Agent has arrow: ", len(arrow) > 0)

    print("Since we know the wumpus' location beforehand, let's shoot it")
    make_action(prolog, a_map, "turnright")
    make_action(prolog, a_map, "shoot")
    print("The wumpus should now be dead and all wumpus cells should be removed")
    print("And we check again if the agent has the arrow")
    arrow = list(prolog.query("hasarrow"))
    print("Agent has arrow: ", len(arrow) > 0)

    print("Finally we check the agent's current relative position")
    current = list(prolog.query("current(X, Y, Dir)"))[0]
    print(f"Current: [{current['X']}, {current['Y']}, {current['Dir']}]")
    print("It should be [2, 0, rsouth]")
    print("\n")


def printout_reposition():
    a_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", a_map)

    print("===[Complete Absolute Map]===")
    a_map.print_init_map()

    print("===[Testing reposition/1]===")
    print("Moving agent to (0, 2) first")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "turnright")
    print("If we take a portal from any direction, the absolute direction should stay the same")
    print("But the relative direction should reset to north")
    print("In this case, we teleport the agent to (1, 4) on the absolute map")
    make_action(prolog, a_map, "moveforward")

    print("Any movement we make should update accordingly")
    print("Let's move the agent to relative (-1, 1)")
    make_action(prolog, a_map, "moveforward")
    make_action(prolog, a_map, "turnleft")
    make_action(prolog, a_map, "moveforward")
    print("On the absolute map, the agent should move east then north")
    print("But on the relative map, north then west")

    print("\n")


def printout_explore():
    a_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", a_map)

    print("===[Complete Absolute Map]===")
    a_map.print_init_map()

    print("===[Testing explore/1]===")
    print("Driver will just keep repeatedly calling explore/1 and running all actions provided")
    print("Relative map will only be printed for the last action for each explore/1 call to make it easier to follow")
    print("action/2 queries will still be printed for each action")
    print("See you at the end of the printout :)")
    print("\n")

    auto_explore(prolog, a_map)
    make_action(prolog, a_map, "none")
    print("Agent should now be at relative (0, 0) and all possible safe cells are visited")
    print("All available coins should also have been picked up")
    print("All the 'border' cells should either be wumpus, confundus portals or walls")

    print("\n")


# tests correctness of agent's localisation, mapping and sensory inference
def printout_loc_map_sensory():
    printout_glitter_visited_safe()
    printout_confundus_tingle()
    printout_wumpus_stench_bump_current()
    printout_reposition()
    printout_explore()


def main():
    filename = "Benjababe-testPrintout-Self-Self.txt"
    sys.stdout = open(file=filename, mode="w+", encoding="utf8")
    printout_loc_map_sensory()


if __name__ == "__main__":
    main()
