from queue import PriorityQueue
from misc import PathInfo, calc_path_distance


def ucs(source: str, dest: str, dist: dict, g: dict) -> PathInfo:
    """ Super simple UCS, no heuristics or anything. Just using known neighbour distances

    Args:
        source (str): Source node
        dest (str): Destination node
        dist (dict): Dictionary of distances between 2 nodes
        g (dict): Dictionary of neighbours, given a node as its key

    Returns:
        PathInfo: Object containing all information needed to be printed
    """

    # using priority queue for ease of retrieving current shortest path
    prio_queue = PriorityQueue()

    # priority queue item is a such: ( $path_taken: list )
    prio_queue.put((0, [source]))

    # nodes to not revisit accidentally
    visited = set()

    while prio_queue.not_empty:
        pair = prio_queue.get()

        current_path = pair[1]

        # current node will be the last node in the path taken
        current_node = current_path[-1]

        # explore node if it hasn't already been
        if current_node not in visited:
            visited.add(current_node)

            # return path taken if node is the destination
            if current_node == dest:
                path_info = PathInfo()
                path_info.path = "->".join(current_path)
                path_info.dist = calc_path_distance(current_path, dist)
                path_info.energy = "Not considered"
                return path_info

            # add paths for neighbouring nodes into the priority queue
            for neighbour in g[current_node]:
                new_dist = dist[f"{current_node},{neighbour}"]
                score = pair[0] + new_dist

                new_path = list(pair[1])
                new_path.append(neighbour)

                prio_queue.put((score, new_path))

    return PathInfo()
# end_ucs


def bfs(source: str, dest: str, dist: dict, g: dict) -> PathInfo:
    """ Basic BFS. Unused in main code

    Args:
        source (str): Source node
        dest (str): Destination node
        dist (dict): Dictionary of distances between 2 nodes
        g (dict): Dictionary of neighbours, given a node as its key

    Returns:
        PathInfo: Object containing all information needed to be printed
    """

    # queue contains current paths considered
    queue = [[source]]
    visited = set()

    while len(queue) > 0:
        current_path = queue.pop(0)

        current_node = current_path[-1]

        # skip path if latest node has already been visited
        if current_node not in visited:
            visited.add(current_node)

            if current_node == dest:
                path_info = PathInfo()
                path_info.path = "->".join(current_path)
                path_info.dist = calc_path_distance(current_path, dist)
                path_info.energy = "Not considered"
                return path_info

            for neighbour in g[current_node]:
                new_path = current_path + [neighbour]
                queue.append(new_path)

    return PathInfo()
# end_bfs
