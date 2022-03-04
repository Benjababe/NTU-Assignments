import json
from math import sqrt
from typing import Tuple

ENERGY_BUDGET = 287932


class PathInfo:
    """ PathInfo object contains information of the path found
    """

    def __init__(self, path="No path found", dist=-1, energy=-1):
        """ Constructor for PathInfo

        Args:
            path (str, optional): String path joined with '->'. Defaults to "No path found".
            dist (int, optional): Path distance. Defaults to -1.
            energy (int, optional): Energy cost to traverse path. Defaults to -1.
        """
        self.path = path
        self.dist = dist
        self.energy = energy


def load_json_files() -> Tuple[dict, dict, dict, dict]:
    """ Loads json files into program memory as dicts

    Returns:
        dict: Dictionary of coordinates of nodes
        dict: Dictionary of power cost to travel between 2 nodes
        dict: Dictionary of distances between 2 nodes
        dict: Dictionary of neighbours, given a node as its key
    """

    with open("Coord.json", "r") as f:
        coord = json.load(f)
        f.close()

    with open("Cost.json", "r") as f:
        cost = json.load(f)
        f.close()

    with open("Dist.json", "r") as f:
        dist = json.load(f)
        f.close()

    with open("G.json", "r") as f:
        g = json.load(f)
        f.close()

    return coord, cost, dist, g


def h(source: str, dest: str, coord: dict) -> int:
    """ Calculates heuristic value for the a* search for task 3

    Args:
        source (str): Source node
        dest (str): Destination node
        coord (dict): Dictionary of coordinates of nodes

    Returns:
        int: Distance between source and destination node
    """

    source_coord = coord[source]
    dest_coord = coord[dest]

    dx = abs(source_coord[0] - dest_coord[0])
    dy = abs(source_coord[1] - dest_coord[1])

    return sqrt(dx**2 + dy**2)


def calc_path_distance(path: list, dist: dict) -> int:
    """ Calculates distance of the path taken

    Args:
        path (list): Path taken to get to destination node
        dist (dict): Dictionary of distances between 2 nodes

    Returns:
        int: Distance taken for the path
    """

    dist_taken = 0

    for i in range(len(path) - 1):
        dist_taken += dist[f"{path[i]},{path[i+1]}"]

    return dist_taken


def calc_path_energy(path: list, cost: dict) -> int:
    """ Calculates energy used for the taken path

    Args:
        path (list): Path taken to get to destination node
        cost (dict): Dictionary of power cost to travel between 2 nodes

    Returns:
        int: Energy used for the path
    """

    energy_used = 0

    for i in range(len(path) - 1):
        energy_used += cost[f"{path[i]},{path[i+1]}"]

    return energy_used
