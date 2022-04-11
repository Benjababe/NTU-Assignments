from pyswip import Prolog

from map import Map


# wumpus is at (0, 1)
def test_wumpus_detection(prolog: Prolog, w_map: Map):
    list(prolog.query("action(turnleft,    [on, on, off, off, off, off])"))
    c = list(prolog.query("wumpus(X,Y)"))
    list(prolog.query("action(moveforward, [off, off, off, off, off, off])"))
    c = list(prolog.query("wumpus(X,Y)"))
    list(prolog.query("action(turnright,   [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, on, off, off, off, off])"))
    c = list(prolog.query("wumpus(X,Y)"))
    list(prolog.query("action(turnright,   [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, off, off, off, off])"))
    list(prolog.query("action(none,        [off, on, off, off, off, off])"))
    c = list(prolog.query("wumpus(X,Y)"))
    print("[Python] Wumpus is at:", list(prolog.query("wumpus(X,Y)")))


# portal is at (1, 2)
def test_portal(prolog: Prolog, w_map: Map):
    list(prolog.query("action(moveforward, [on, off, off, off, off, off])"))
    list(prolog.query("action(turnright,   [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, on, off, off, off])"))
    c = list(prolog.query("confundus(X,Y)"))
    list(prolog.query("action(turnleft,    [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, on, off, off, off])"))
    c = list(prolog.query("confundus(X,Y)"))
    list(prolog.query("action(turnleft,    [off, off, off, off, off, off])"))
    list(prolog.query("action(moveforward, [off, off, off, off, off, off])"))
    list(prolog.query("action(none,        [off, off, on, off, off, off])"))
    c = list(prolog.query("confundus(X,Y)"))
    print("[Python] Agent is at:", list(prolog.query("current(X, Y, Dir)")))


def test_gold(prolog: Prolog):
    list(prolog.query("action(none, [on, off, off, on, off, off])"))
    rcoords = list(prolog.query("current(X, Y, _)"))[0]
    print(bool(list(prolog.query(f"glitter({rcoords['X']},{rcoords['Y']})"))))
    list(prolog.query("action(pickup, [off, off, off, on, off, off])"))
    print(bool(list(prolog.query(f"glitter({rcoords['X']},{rcoords['Y']})"))))
