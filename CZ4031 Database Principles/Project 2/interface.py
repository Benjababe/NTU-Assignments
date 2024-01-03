import PySimpleGUI as sg
import os
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

from explain import build_readable_tree, get_qep_difference, generate_numbered_list


class Interface:
    def __init__(self, connection):
        self.connection = connection

        self.tables = [
            "customer",
            "lineitem",
            "nation",
            "orders",
            "part",
            "partsupp",
            "region",
            "supplier",
        ]

        self.window2Active = False
        self.window3Active = False
        self.n1 = None
        self.n2 = None
        self.notice = True

        self.createUIlayout()

    def createUIlayout(self):
        sg.theme("SandyBeach")
        sg.set_options(dpi_awareness=True)
        font = "Helvetica 14 bold"
        multilineSize = (50, 15)
        buttonSize = (20, 2)

        # Define the layout of the interface
        leftColumn = [
            [
                sg.Text("Query 1:", font=font),
                sg.Multiline(size=multilineSize, key="query1"),
            ],
            [
                sg.Text("Query 2:", font=font),
                sg.Multiline(size=multilineSize, key="query2"),
            ],
            [
                sg.Button("Compare", size=buttonSize, font=font),
                sg.Button("Exit", size=buttonSize, font=font),
            ],
        ]

        centerColumn = [
            [
                sg.Text("QEP P1:", font=font),
                sg.Multiline(size=multilineSize, disabled=True, key="qepP1"),
            ],
            [
                sg.Text("QEP P2:", font=font),
                sg.Multiline(size=multilineSize, disabled=True, key="qepP2"),
            ],
            [
                sg.Button("View as graph", size=buttonSize,font=font, key="graph")
            ],
        ]

        rightColumn = [
            [
                sg.Text("Difference:", font=font),
                sg.Multiline(size=multilineSize, disabled=True, key="qepDiff"),
            ],
            [
                sg.Checkbox(
                    "Include trivial operations (Experimental)", key="chkTrivial"
                ),
            ],
        ]

        layout = [
            [
                sg.Column(leftColumn),
                sg.VerticalSeparator(),
                sg.Column(centerColumn),
                sg.VerticalSeparator(),
                sg.Column(rightColumn),
            ]
        ]

        # Create the window
        self.window = sg.Window("Project 2: QEP", layout, finalize=True)

    def get_query_execution_plan(self, query: str):
        with self.connection as conn:  # handles exceptions
            with conn.cursor() as cursor:
                cursor.execute(f"EXPLAIN (FORMAT JSON) {query}")
                result = cursor.fetchone()
                return result[0][0]["Plan"]

    def createGraphElements(self, node, parentIndex, edgeList, label, colorMap):
        """
        create edgelist, labels and colors for nodes in qep
        """
        label[parentIndex] = node.name
        colorMap.append("#33A8FF")
        if len(node.children) == 0:
            if "Scan" in node.name:
                edgeList.append((parentIndex, parentIndex * 2 + 1))
                label[parentIndex * 2 + 1] = node.table_name
                colorMap.append("green")
            return
        for index, child in enumerate(node.children):
            edgeList.append((parentIndex, parentIndex * 2 + index + 1))
            self.createGraphElements(
                child, parentIndex * 2 + index + 1, edgeList, label, colorMap
            )
        return edgeList, label, colorMap

    def convertToGraph(self, edgeList, name, labels, colorMap):
        """
        create graph of qep
        """
        G = nx.Graph()
        G.add_edges_from(edgeList)
        pos = graphviz_layout(G, prog="dot")
        plt.figure(
            figsize=(8, 8) if len(edgeList) < 11 else (len(edgeList), len(edgeList))
        )
        nx.draw(
            G,
            pos=pos,
            labels=labels,
            node_color=colorMap,
            with_labels=True,
            font_size=10,
            node_size=4000,
        )
        plt.savefig(f"{name}.png")

    def clean(self):
        directory = os.getcwd()
        if os.path.exists(directory + "\\n1.png"):
            os.remove("n1.png")
            os.remove("n2.png")
        self.connection.close()

    # Event loop to process events and get inputs
    def start(self):
        self.window["query1"].update(
            """ select
                    n_name,
                    sum(l_extendedprice * (1 - l_discount)) as revenue
                from
                    customer,
                    orders,
                    lineitem,
                    supplier,
                    nation,
                    region
                where
                    c_custkey = o_custkey
                    and l_orderkey = o_orderkey
                    and l_suppkey = s_suppkey
                    and c_nationkey = s_nationkey
                    and s_nationkey = n_nationkey
                    and n_regionkey = r_regionkey
                group by
                    n_name
      """
        )
        self.window["query2"].update(
            """
            select
                n_name,
                sum(l_extendedprice * (1 - l_discount)) as revenue
            from
                customer,
                orders,
                lineitem,
                supplier,
                nation,
                region
            where
                c_custkey = o_custkey
                and l_orderkey = o_orderkey
                and l_suppkey = s_suppkey
                and c_nationkey = s_nationkey
                and s_nationkey = n_nationkey
                and n_regionkey = r_regionkey
                and r_name = 'ASIA'
                and o_orderdate >= '1994-01-01'
                and o_orderdate < '1995-01-01'
                and c_acctbal > 10
                and s_acctbal > 20
            group by
                n_name
            order by
                revenue desc;
        """
        )
        while True:
            event, values = self.window.read()

            # If the user closes the window or clicks the Exit button
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break

            # If the user clicks the Compare button
            if event == "Compare":
                # Get the input from the textboxes
                query1 = values["query1"]
                query2 = values["query2"]

                # Check if the textboxes are empty or contains whitespaces
                if not query1.strip() or not query2.strip():
                    sg.popup_error("Please enter queries in both boxes.", title="Error")
                else:
                    try:
                        # Flag whether to show trivial operations in difference output
                        use_note = values["chkTrivial"]

                        # Compare the queries and display the QEPs in the displayboxes
                        qep1 = self.get_query_execution_plan(query1)
                        qep2 = self.get_query_execution_plan(query2)
                        self.n1 = build_readable_tree(qep1)
                        self.n2 = build_readable_tree(qep2)
                        diff = get_qep_difference(self.n1, self.n2, use_note=use_note)

                        self.window["qepP1"].update(self.n1)
                        self.window["qepP2"].update(self.n2)
                        self.window["qepDiff"].update(generate_numbered_list(diff))
                    except Exception as e:
                        sg.popup_error(
                            f"Error: {e}", title="Error", font="Helvetica 14 bold"
                        )

            # If the user clicks the view graph button
            if event == "graph":
                if (
                    self.n1
                    and self.n2
                    and "Unhandled node type" not in self.n1.description
                    and "Unhandled node type" not in self.n2.description
                ):
                    # show popup to inform users
                    if self.notice:
                        sg.popup_ok(
                            "Images must be closed before submitting new query",
                            title="Notice",
                            font="Helvetica 14 bold",
                        )
                        self.notice = False

                    # create new window for graph of QEP1
                    if not self.window2Active:
                        self.window2Active = True
                        layout2 = [
                            [
                                sg.Column(
                                    [
                                        [
                                            sg.Image(
                                                background_color="white",
                                                key="qepGraph1",
                                            )
                                        ]
                                    ],
                                    size=(800, 800),
                                    scrollable=True,
                                    key="qepGraph1Column",
                                )
                            ]
                        ]
                        window2 = sg.Window(
                            "QEP1 Graph View",
                            layout2,
                            grab_anywhere=True,
                            finalize=True,
                        )

                        n1EdgeList = []
                        n1Labels = {}
                        n1ColorMap = []
                        self.createGraphElements(
                            self.n1, 0, n1EdgeList, n1Labels, n1ColorMap
                        )
                        self.convertToGraph(n1EdgeList, "n1", n1Labels, n1ColorMap)
                        window2.move(200, 250)
                        window2["qepGraph1"].update(filename="n1.png")
                        window2.refresh()
                        window2["qepGraph1Column"].contents_changed()

                    # create new window for graph of QEP2
                    if not self.window3Active:
                        self.window3Active = True
                        layout3 = [
                            [
                                sg.Column(
                                    [
                                        [
                                            sg.Image(
                                                background_color="white",
                                                key="qepGraph2",
                                            )
                                        ]
                                    ],
                                    size=(800, 800),
                                    scrollable=True,
                                    key="qepGraph2Column",
                                )
                            ]
                        ]
                        window3 = sg.Window(
                            "QEP2 Graph View",
                            layout3,
                            grab_anywhere=True,
                            finalize=True,
                        )

                        n2EdgeList = []
                        n2Labels = {}
                        n2ColorMap = []
                        self.createGraphElements(
                            self.n2, 0, n2EdgeList, n2Labels, n2ColorMap
                        )
                        self.convertToGraph(n2EdgeList, "n2", n2Labels, n2ColorMap)
                        window3.move(1250, 250)
                        window3["qepGraph2"].update(filename="n2.png")
                        window3.refresh()
                        window3["qepGraph2Column"].contents_changed()

            # check when user closes the graph of QEP1
            if self.window2Active:
                event2, values2 = window2.read()
                if event2 == sg.WIN_CLOSED:
                    self.window2Active = False
                    window2.close()

            # check when user closes the graph of QEP2
            if self.window3Active:
                event3, values3 = window3.read()
                if event3 == sg.WIN_CLOSED:
                    self.window3Active = False
                    window3.close()

        # Close the window
        self.window.close()
