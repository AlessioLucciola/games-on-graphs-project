import math
import random
import networkx as nx
import matplotlib.pyplot as plt

class Graph():
    def __init__(self, n_nodes = 10, edge_probability = 0.3):
        super(Graph, self).__init__
        self.graph = nx.DiGraph()

        if (n_nodes < 1):
            raise ValueError("The number of nodes must be a positive number")
        
        if (edge_probability < 0 or edge_probability > 1):
            raise ValueError("The edge probability must be a value between 0 and 1")

        # Create the nodes
        for i in range(n_nodes):
            self.graph.add_node(i)

        # Add the edges randomly
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                if random.random() < edge_probability:
                    self.graph.add_edge(i, j)
        
        # Define the winning nodes
        n_winning = math.floor(n_nodes/5) # Add 2 winning nodes each 5 nodes
        winning_nodes = random.sample(range(n_nodes+1), n_winning)
        attributes = {}
        for n in self.graph.nodes:
            if n in winning_nodes:
                attributes[n] = {'winning': True}
            else:
                attributes[n] = {'winning': False}
        nx.set_node_attributes(self.graph, attributes)

        # Split nodes between the two players
        player0_nodes = [n for n in winning_nodes]
        while len(player0_nodes) < n_nodes/2:
            num = random.randint(0, n_nodes)
            if num not in player0_nodes:
                player0_nodes.append(num)
        player1_nodes = [node for node in range(10) if node not in player0_nodes]

        print("Nodes of player 0: " + str(player0_nodes))
        print("Nodes of player 1: " + str(player1_nodes))

        # Color the winning node in the graph
        node_colors = {node: 'red' if node in winning_nodes else 'blue' for node in self.graph.nodes}
        nx.set_node_attributes(self.graph, node_colors, 'color')

    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)
        node_colors = [self.graph.nodes[node]['color'] if 'color' in self.graph.nodes[node] else 'lightblue' for node in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors)
        plt.show()
    
    def get_winning_nodes(self):
        return [n for n in self.graph.nodes if self.graph.nodes[n]['winning']]
    
    def is_winning(self, n):
        return False if (n > self.n_nodes or not self.graph.nodes[n]['winning']) else True
    
    def get_predecessors(self, node):
        return list(self.graph.predecessors(node))
    
    def return_graph(self):
        return self.graph
    