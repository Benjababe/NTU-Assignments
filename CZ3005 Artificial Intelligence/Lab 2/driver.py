from typing import Dict, List
from pyswip import *
from random import choice

from map import Map


def setup_map(N: int, M: int) -> Map:
    w_map = Map(N, M)
    w_map.agent_start = [3, 3]
    w_map.agent_pos = [3, 3]
    w_map.agent_rel_dir = "rnorth"
    w_map.agent_abs_dir = "rnorth"
    w_map.reposition_agent(3, 2, "rnorth")

    w_map.add_wumpus(5, 4)

    w_map.add_coin(1, 1)
    w_map.add_coin(3, 2)

    w_map.add_portal(1, 3)
    w_map.add_portal(2, 1)
    w_map.add_portal(3, 4)

    return w_map


def setup_prolog(filename: str, w_map: Map) -> Prolog:
    prolog = Prolog()
    prolog.consult(filename)
    list(prolog.query("init"))

    perceptions = w_map.get_cell_perceptions()
    list(prolog.query(f"reposition([{','.join(perceptions)}])"))
    return prolog


def get_action(action: str = None) -> str:
    if action:
        return action
    return choice(["moveforward", "turnleft", "turnright"])


def make_action(prolog: Prolog, w_map: Map, action: str = None, print_map: bool = True):
    action = get_action(action=action)
    w_map.do_action(action)
    perceptions = w_map.get_cell_perceptions()

    query_str = f"action({action}, [{','.join(perceptions)}])"
    list(prolog.query(query_str))
    print(query_str)

    if w_map.check_portal():
        print("Stepped on a portal lol")
        w_map.reposition_agent(3, 3, "rnorth")
        perceptions = w_map.get_cell_perceptions()
        list(prolog.query(f"reposition([{','.join(perceptions)}])"))

    sense_printout = [
        "Confounded" if perceptions[0] == "on" else "C",
        "Stench" if perceptions[1] == "on" else "S",
        "Tingle" if perceptions[2] == "on" else "T",
        "Glitter" if perceptions[3] == "on" else "G",
        "Bump" if perceptions[4] == "on" else "B",
        "Scream" if perceptions[5] == "on" else "S"
    ]

    if print_map:
        print('-'.join(sense_printout))
        # w_map.print_absolute_map(prolog)
        w_map.print_relative_map(prolog)


# continues using explore(L) until no safe cells are left
def auto_explore(prolog: Prolog, w_map: Map):
    path_exists = True
    while path_exists:
        L = list(prolog.query("explore(L)"))
        path_exists = handle_explore_result(prolog, w_map, L)


def handle_explore_result(prolog: Prolog, w_map: Map, L: List[Dict[str, List[Atom]]]) -> bool:
    if len(L) == 0:
        print("Out of explorable space...")
        return False

    actions = L[0]["L"]
    for action in actions:
        make_action(prolog, w_map, action=action.value, print_map=True)

    return True


def main():
    w_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", w_map)

    w_map.print_init_map()
    w_map.reset_absolute_map(full_clear=True)
    w_map.print_relative_map(prolog)

    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "turnright")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "turnright")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "turnleft")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "turnleft")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "turnleft")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "moveforward")
    # make_action(prolog, w_map, "moveforward")

    auto_explore(prolog, w_map)


if __name__ == "__main__":
    main()
