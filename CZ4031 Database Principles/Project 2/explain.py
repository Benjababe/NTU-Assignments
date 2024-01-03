from __future__ import annotations
from functools import reduce
from random import randint


intermediate_count = 0

MISC_TYPES = ["Aggregate", "Gather", "Gather Merge",
              "Hash", "Materialize", "Memoize", "Sort"]

# use to prevent duplicate differences
diff_cache = {}


class ReadableNode:
    id: int
    type: str
    name: str
    description: str
    children: list[ReadableNode]
    table_name: str
    real_node: dict

    # returns numbered sequence of steps
    def __str__(self):
        return generate_numbered_list(self.get_query_steps())

    # used for caching
    def __hash__(self) -> int:
        return self.id

    # used for caching
    def __eq__(self, __value: ReadableNode) -> bool:
        if isinstance(__value, ReadableNode):
            return self.id == __value.id
        return False

    def __init__(self, node: dict, is_root=False):
        self.id = randint(0, 1000000000)

        node_type = node["Node Type"]

        self.children = []

        # generates recursively, if node has children, creates and append them to current node
        if "Plans" in node:
            for child_node in node["Plans"]:
                readable_child_node = ReadableNode(child_node)
                self.children.append(readable_child_node)

        if node_type in ["Seq Scan", "Index Scan", "Index Only Scan", "CTE Scan"]:
            self.type = "Scan"
            self.name = node_type
            self.scan_handler(node, node_type)

        elif node_type in ["Nested Loop", "Hash Join", "Merge Join"]:
            self.type = "Join"
            self.name = node_type
            self.join_handler(node, node_type, is_root)

        else:
            self.misc_handler(node, node_type, is_root)

        self.real_node = node

    def scan_handler(self, node: dict, node_type: str):
        """Handles scan operations

        Args:
            node (dict): Current node in the QEP tree
            node_type (str): Type of the current node
        """

        match node_type:
            case "Seq Scan":
                rel_name = node["Relation Name"]
                alias = node["Alias"]

                self.table_name = rel_name
                self.description = (
                    f"Sequential scan done on {rel_name} with alias {alias}"
                )

                if "Filter" in node:
                    self.description += f" using filter {node['Filter']}"

            case "Index Scan":
                rel_name = node["Relation Name"]
                alias = node["Alias"]

                self.table_name = rel_name
                self.description = f"Index scan done on {rel_name} with alias {alias}"

                if "Index Cond" in node:
                    self.description += f" with index condition {node['Index Cond']}"

                if "Filter" in node:
                    self.description += f" using filter {node['Filter']}"

            case "Index Only Scan":
                rel_name = node["Relation Name"]
                alias = node["Alias"]

                self.table_name = rel_name
                self.description = (
                    f"Index only scan done on {rel_name} with alias {alias}"
                )

                if "Index Name" in node:
                    self.description += f" on index name {node['Index Name']}"

            case "CTE Scan":
                cte_name = node["CTE Name"]
                alias = node["Alias"]

                self.table_name = cte_name
                self.description = f"CTE scan done on {cte_name} with alias {alias}"

                if "Filter" in node:
                    self.description += f" using filter {node['Filter']}"

    def join_handler(self, node: dict, node_type: str, is_root: bool):
        """Handles JOIN operations

        Args:
            node (dict): Current node in the QEP tree
            node_type (str): Type of the current node
            is_root (bool): Flag whether the current node is the root
        """

        match node_type:
            case "Nested Loop":
                c1, c2 = self.children[:2]
                self.description = (
                    f"Nested loop join done on {c1.table_name} and {c2.table_name}"
                )

                if not is_root:
                    self.generate_intermediate_table()

            case "Hash Join":
                c1, c2 = self.children[:2]
                self.description = (
                    f"Hash join done on {c1.table_name} and {c2.table_name}"
                )

                if not is_root:
                    self.generate_intermediate_table()

            case "Merge Join":
                c1, c2 = self.children[:2]
                self.description = (
                    f"Merge join done on {c1.table_name} and {c2.table_name}"
                )

                if "Merge Cond" in node:
                    self.description += f" with merge condition {node['Merge Cond']}"

                if "Filter" in node:
                    self.description += f" using filter {node['Filter']}"

                if not is_root:
                    self.generate_intermediate_table()

    def misc_handler(self, node: dict, node_type: str, is_root: bool):
        """Handles operations which are not in a group

        Args:
            node (dict): Current node in the QEP tree
            node_type (str): Type of the current node
            is_root (bool): Flag whether the current node is the root
        """

        self.type = node_type
        self.name = node_type

        match node_type:
            case "Aggregate":
                c1 = self.children[0]
                self.description = f"Aggregated table {c1.table_name}"

                if not is_root:
                    self.generate_intermediate_table()

            case "Gather":
                c1 = self.children[0]
                self.description = f"Gathered table {c1.table_name}"

                if not is_root:
                    self.generate_intermediate_table()

            case "Gather Merge":
                self.table_name = self.children[0].table_name
                self.description = f"Gathered and merged results from {self.table_name}"

            case "Hash":
                self.table_name = self.children[0].table_name
                self.description = f"Hashing done on {self.table_name}"

            case "Materialize":
                c1 = self.children[0]
                self.description = f"Materialized table {c1.table_name}"

                if not is_root:
                    self.generate_intermediate_table()

            case "Memoize":
                self.table_name = self.children[0].table_name
                self.description = f"Memoization done on {self.table_name}"

            # sorting does not create an intermediate table
            case "Sort":
                key = node["Sort Key"]
                self.table_name = self.children[0].table_name
                self.description = (
                    f"Sort done on {self.table_name} using sort key {key}"
                )

            case _:
                # edge case for any node types not handled thus far
                self.description = f"Unhandled node type found ({node_type}), add a handler for this node type!!"
                if len(self.children) > 0:
                    self.table_name = self.children[0].table_name
                else:
                    self.generate_intermediate_table()

    def generate_intermediate_table(self):
        """Creates an intermediate table name for the current node"""

        global intermediate_count
        self.table_name = f"Tmp{intermediate_count}"
        intermediate_count += 1
        self.description += f" which creates intermediate table {self.table_name}"

    def get_query_steps(self) -> list[str]:
        """Retrieves the steps of the query in English

        Returns:
            list[str]: List of steps taken during the query
        """

        steps = []

        # finds earliest steps through DFS
        for child in self.children:
            steps.extend(child.get_query_steps())

        steps.append(self.description)
        return steps


def build_readable_tree(qep: dict) -> ReadableNode:
    """Parses the JSON output from postgres to a tree structure

    Args:
        qep (dict): EXPLAIN formatted as JSON from postgres

    Returns:
        ReadableNode: Root node of the QEP
    """

    global intermediate_count
    intermediate_count = 0

    readable_node = ReadableNode(qep, is_root=True)
    return readable_node


def generate_numbered_list(l: list[str]) -> str:
    """Returns a joined string of the list with numbering

    Args:
        l (list[str]): List of strings for plans or changes

    Returns:
        str: All strings numbered and joined
    """

    return reduce(
        lambda acc, step: acc +
        f"{step[0]}. {step[1]}\n", enumerate(l, start=1), ""
    )


def get_qep_difference(
    n1: ReadableNode, n2: ReadableNode,
    diff_count: int = 0, use_note: bool = False
) -> list[str]:
    """Generates a list of differences between n1 (old) and n2 (new)

    Args:
        n1 (ReadableNode): Node in the old QEP
        n2 (ReadableNode): Node in the new QEP
        diff_count (int, optional): Number of current differences. Defaults to 0.
        use_note (bool, optional): Flag whether to include trivial operations. Defaults to False

    Returns:
        list[str]: List of differences
    """

    differences = []

    # if both nodes are exactly the same, go to their children
    if n1.name == n2.name and len(n1.children) == len(n2.children):
        # exception for seq scans as one may contain a filter
        if n1.name == "Seq Scan" and n2.name == "Seq Scan":
            diff = get_diff_reason(n1, n2)
            if diff != None:
                differences.append(diff)

        for i in range(len(n1.children)):
            diff = get_qep_difference(
                n1.children[i], n2.children[i], diff_count)
            differences.extend(diff)

    else:
        # uncomparable operation for node 1, skipping it
        if n1.name in MISC_TYPES:
            # add note if available
            if use_note:
                note = get_uncomparable_note(n1, n2)
                if note is not None:
                    differences.append(note)

            diff = get_qep_difference(n1.children[0], n2, diff_count)
            differences.extend(diff)

        # uncomparable operation for node 2, skipping it
        elif n2.name in MISC_TYPES:
            # add note if available
            if use_note:
                note = get_uncomparable_note(n1, n2)
                if note is not None:
                    differences.append(note)

            diff = get_qep_difference(n1, n2.children[0], diff_count)
            differences.extend(diff)

        else:
            if (n1, n2) in diff_cache:
                diff = diff_cache[(n1, n2)]

            else:
                diff_count += 1
                diff = f"{n1.description} has been changed to {n2.description}"
                diff += f", {get_diff_reason(n1, n2)}"

                diff_cache[(n1, n2)] = diff
                differences.append(diff)

        if len(n1.children) == len(n2.children):
            for i in range(len(n1.children)):
                diff = get_qep_difference(
                    n1.children[i], n2.children[i], diff_count)
                differences.extend(diff)

    return differences


def get_uncomparable_note(n1: ReadableNode, n2: ReadableNode) -> str | None:
    note = None

    if (n1, n2) in diff_cache:
        return note

    if n1.name == "Sort" and n2.name != "Sort":
        note = f"[NOTE] P1 has a sort on {n1.real_node['Sort Key']} which P2 does not"

    if n1.name != "Sort" and n2.name == "Sort":
        note = f"[NOTE] P2 has a sort on {n2.real_node['Sort Key']} which P1 does not"

    if n1.name == "Gather Merge" and n2.name != "Gather Merge":
        note = f"[NOTE] P1 has a gather merge which utilises parallelisation which P2 does not"

    if n1.name != "Gather Merge" and n2.name == "Gather Merge":
        note = f"[NOTE] P2 has a gather merge which utilises parallelisation which P1 does not"

    diff_cache[(n1, n2)] = note
    return note


def get_diff_reason(n1: ReadableNode, n2: ReadableNode) -> str:
    reason = ""

    if n1.type == "Join" and n2.type == "Join":
        if n2.name == "Nested Loop":
            reason += "swtiching to nested loop for P2 has a lower estimated rows processed, possibly because one relation has very few rows to join "

        elif n2.name == "Hash Join":
            if '=' in n2.real_node['Hash Cond']:
                reason += f"due to the join condition based on equality of {n2.real_node['Hash Cond']}, "
            reason += "both tables being very large and the data is unevenly distributed "

        elif n2.name == "Merge Join":
            if '=' in n2.real_node['Merge Cond']:
                reason += f"due to the merge condition based on equality of {n2.real_node['Merge Cond']}, "
            reason += "the joined columns are sorted or memory is a limiting factor"

    if n1.type == "Scan" and n2.type == "Scan":
        if n1.name == "Seq Scan" and n2.name == "Seq Scan":
            if 'Filter' in n1.real_node and 'Filter' not in n2.real_node:
                reason += f"P2 does not have the filter {n1.real_node['Filter']} which P1 has "
            elif 'Filter' not in n1.real_node and 'Filter' in n2.real_node:
                reason += f"P2 has the filter {n2.real_node['Filter']} which P1 does not have "
            else:
                return None

        if n1.name == "Seq Scan" and n2.name == "Index Scan":
            if not 'Index Name' in n1.real_node:
                reason += f"P2 uses an index {n2.real_node['Index Name']} "
            else:
                reason += "P2 has a more selective filter which results in a smaller result set "

        if n1.name == "Index Scan" and n2.name == "Seq Scan":
            reason += "a large number of rows is required for P2 compared to P1 "

    # if number of children are different, assume core structure of query is different
    if len(n1.children) != len(n2.children):
        reason += f"possibly due to P1 having a different data output from P2 "

    if n1.real_node['Plan Rows'] > n2.real_node['Plan Rows']:
        reason += f"reducing rows processed from {n1.real_node['Plan Rows']} to {n2.real_node['Plan Rows']} "
    elif n1.real_node['Plan Rows'] < n2.real_node['Plan Rows']:
        reason += f"increasing rows processed from {n1.real_node['Plan Rows']} to {n2.real_node['Plan Rows']} "

    if n1.real_node['Total Cost'] > n2.real_node['Total Cost']:
        reason += f"reducing total cost from {n1.real_node['Total Cost']} to {n2.real_node['Total Cost']} "

    return reason
