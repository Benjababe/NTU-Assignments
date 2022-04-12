from typing import List
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
