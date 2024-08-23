import networkx as nx
import hvplot.networkx as hvnx
import matplotlib.pyplot as plt


class Node:
    def __init__(self,
                 node_name: str):
        self.node_name = node_name
        self.connected_nodes = []

    def __repr__(self):
        return f"Node Name: {self.node_name}\tConnected Nodes: {self.connected_nodes}\n"


class WholeStation:
    def __init__(self):
        b1 = B1()
        concourse = Concourse()

        concourse.ALL_NODES[-1].connected_nodes.append(b1.ALL_NODES[-1])

        self.ALL_NODES = b1.ALL_NODES + concourse.ALL_NODES
        self.ALL_NODES_LOCATION = {}
        self.ALL_NODES_LOCATION.update(b1.ALL_NODES_LOCATION)
        self.ALL_NODES_LOCATION.update(concourse.ALL_NODES_LOCATION)

    def visualize_graph(self):
        G = nx.Graph()
        for node in self.ALL_NODES:
            G.add_node(node.node_name)
        for node in self.ALL_NODES:
            for connected_node in node.connected_nodes:
                G.add_edge(node.node_name, connected_node.node_name)
        return G, self.ALL_NODES_LOCATION



class B1:
    def __init__(self):
        self.ALL_NODES = self.initialize_nodes()

    def initialize_nodes(self):
        D_NODES = [Node(node_name=f"D{i}") for i in range(1, 13)]
        H_NODES = [Node(node_name=f"H{i}") for i in range(1, 13)]
        L_NODES = [Node(node_name=f"L{i}") for i in range(1, 6)]
        L_NODES.append(Node(node_name="LIFT_B1"))

        L_NODES[-1].connected_nodes.append(L_NODES[2])

        D_NODES_LOCATION = [(i, 0) for i in range(1, len(D_NODES))]
        H_NODES_LOCATION = [(i, 5) for i in range(1, len(H_NODES))]

        self.ALL_NODES_LOCATION = dict(zip([node.node_name for node in D_NODES], D_NODES_LOCATION))
        self.ALL_NODES_LOCATION.update(dict(zip([node.node_name for node in H_NODES], H_NODES_LOCATION)))
        self.ALL_NODES_LOCATION.update(dict(zip([node.node_name for node in L_NODES], [(4,1), (4,3), (6.5,3), (9, 3), (9,1), (6.5, 2)])))



        for index, D_NODE in enumerate(D_NODES):
            if index == 0:
                D_NODE.connected_nodes.append(D_NODES[index + 1])
            elif index == len(D_NODES) - 1:
                D_NODE.connected_nodes.append(D_NODES[index - 1])
            else:
                D_NODE.connected_nodes.extend([D_NODES[index - 1], D_NODES[index + 1]])
                if D_NODE.node_name == 'D4':
                    D_NODE.connected_nodes.append(L_NODES[0])
                elif D_NODE.node_name == 'D9':
                    D_NODE.connected_nodes.append(L_NODES[-2])

        for index, H_NODE in enumerate(H_NODES):
            if index == 0:
                H_NODE.connected_nodes.append(H_NODES[index + 1])
            elif index == len(H_NODES) - 1:
                H_NODE.connected_nodes.append(H_NODES[index - 1])
            else:
                H_NODE.connected_nodes.extend([H_NODES[index - 1], H_NODES[index + 1]])
                if H_NODE.node_name == 'H4':
                    H_NODE.connected_nodes.append(L_NODES[1])
                elif H_NODE.node_name == 'H9':
                    H_NODE.connected_nodes.append(L_NODES[-3])

        for index, L_NODE in enumerate(L_NODES):
            if index == 0:
                L_NODE.connected_nodes.append(L_NODES[index + 1])
            elif index == len(L_NODES) - 2:
                L_NODE.connected_nodes.append(L_NODES[index - 1])

            elif L_NODE.node_name != 'LIFT_B1':
                L_NODE.connected_nodes.append(L_NODES[index - 1])
                L_NODE.connected_nodes.append(L_NODES[index + 1])

        return H_NODES + D_NODES + L_NODES

    def visualize_graph(self):
        G = nx.Graph()
        for node in self.ALL_NODES:
            G.add_node(node.node_name)
        for node in self.ALL_NODES:
            for connected_node in node.connected_nodes:
                G.add_edge(node.node_name, connected_node.node_name)
        return G, self.ALL_NODES_LOCATION

class Concourse:
    def __init__(self):
        self.ALL_NODES = self.initialize_nodes()
        self.ALL_NODES_LOCATION = {
            'EXIT A'    : (1,1),
            'EXIT B'    : (1,5),
            'INT 1'     : (1,3),

            'GANTRY 1'  : (2,3),

            'L11'       : (3,3),
            'L12'       : (3,4),
            'L13'       : (4,4),
            'LIFT'      : (4,3),
            'L14'       : (5,4),
            'L15'       : (5,3),

            'GANTRY 2'  : (6,3),

            'INT 2'     : (7,3),

            'EXIT C'    : (7,1),
            'EXIT D'    : (7,5),
        }

    def initialize_nodes(self):
        EXIT_A = Node('EXIT A')
        EXIT_B = Node('EXIT B')
        EXIT_C = Node('EXIT C')
        EXIT_D = Node('EXIT D')
        GANTRY_1 = Node('GANTRY 1')
        GANTRY_2 = Node('GANTRY 2')
        INT_1 = Node('INT 1')
        INT_2 = Node('INT 2')

        L11 = Node('L11')
        L12 = Node('L12')
        L13 = Node('L13')
        L14 = Node('L14')
        L15 = Node('L15')

        LIFT = Node('LIFT')

        GANTRY_1.connected_nodes.append(INT_1)
        INT_1.connected_nodes.append(GANTRY_1)

        INT_1.connected_nodes.append(EXIT_A)
        INT_1.connected_nodes.append(EXIT_B)

        EXIT_A.connected_nodes.append(INT_1)
        EXIT_B.connected_nodes.append(INT_1)

        GANTRY_2.connected_nodes.append(INT_2)
        INT_2.connected_nodes.append(GANTRY_2)

        INT_2.connected_nodes.append(EXIT_C)
        INT_2.connected_nodes.append(EXIT_D)

        EXIT_C.connected_nodes.append(INT_2)
        EXIT_D.connected_nodes.append(INT_2)


        L11.connected_nodes.append(GANTRY_1)
        L11.connected_nodes.append(L12)

        L12.connected_nodes.append(L11)
        L12.connected_nodes.append(L13)

        L13.connected_nodes.append(LIFT)
        L13.connected_nodes.append(L12)
        L13.connected_nodes.append(L14)

        L14.connected_nodes.append(L13)
        L14.connected_nodes.append(L15)

        LIFT.connected_nodes.append(L13)

        L15.connected_nodes.append(L13)
        L15.connected_nodes.append(EXIT_B)

        node = [EXIT_A, EXIT_B, EXIT_C, EXIT_D, INT_1, INT_2, GANTRY_1, GANTRY_2, L11, L12, L13, L14, LIFT]
        return node


    def visualize_graph(self):
        G = nx.Graph()
        for node in self.ALL_NODES:
            G.add_node(node.node_name)
        for node in self.ALL_NODES:
            for connected_node in node.connected_nodes:
                G.add_edge(node.node_name, connected_node.node_name)
        return G, self.ALL_NODES_LOCATION
#%%
