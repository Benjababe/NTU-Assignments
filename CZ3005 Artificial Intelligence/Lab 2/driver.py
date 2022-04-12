from typing import Dict, List
from pyswip import *

from map import Map


def setup_map(N: int, M: int) -> Map:
    a_map = Map(N, M, "rnorth")
    a_map.reposition_agent(3, 2)

    a_map.add_wumpus(5, 4)

    a_map.add_coin(1, 1)
    a_map.add_coin(3, 2)

    a_map.add_portal(2, 1)
    a_map.add_portal(4, 1)
    a_map.add_portal(4, 4)

    return a_map


def setup_prolog(filename: str, a_map: Map) -> Prolog:
    # initialise prolog file
    prolog = Prolog()
    prolog.consult(filename)
    list(prolog.query("init"))

    # send initial perceptions to agent
    perceptions = a_map.get_cell_perceptions()
    list(prolog.query(f"reposition([{perceptions.get_query_str()}])"))
    return prolog


def make_action(prolog: Prolog, a_map: Map, action: str = None, print_map: bool = True):
    # preemptively clears bumps to prevent old bumps from showing
    a_map.clear_bumps()

    # updates map with action
    a_map.do_action(action)

    # get new perceptions from cell after action
    perceptions = a_map.get_cell_perceptions()

    # update agent with new perceptions
    query_str = f"action({action}, [{perceptions.get_query_str()}])"
    list(prolog.query(query_str))

    # reposition if stepped on a confundus portal
    if a_map.check_portal():
        a_map.reposition_agent(2, 3)
        perceptions = a_map.get_cell_perceptions()
        list(prolog.query(f"reposition([{perceptions.get_query_str()}])"))

    # print out map and relevant info
    if print_map:
        print(f"[Driver] {perceptions.get_sense_printout()}")
        a_map.print_absolute_map(prolog)
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
    return


def handle_explore_result(prolog: Prolog, a_map: Map, L: List[Dict[str, List[Atom]]]) -> bool:
    if len(L) == 0:
        return False

    # apply actions generated from explore/1
    actions = L[0]['L']
    for action in actions:
        make_action(prolog, a_map, action=action, print_map=True)

    return True


def main():
    a_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", a_map)

    a_map.print_init_map()
    a_map.reset_absolute_map(full_clear=True)
    a_map.print_relative_map(prolog)

    auto_explore(prolog, a_map)


if __name__ == "__main__":
    main()
