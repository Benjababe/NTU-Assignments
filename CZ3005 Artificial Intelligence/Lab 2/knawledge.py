from typing import Dict, List, Tuple
from pyswip import Prolog


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

        bump = {
            "data": list(prolog.query("bump(X, Y)")),
            "type": self.BUMP
        }

        self.kb = [
            wumpus, confundus, u, tingle, glitter, confounded,
            stench, safe, visited, wall, bump, agent
        ]
