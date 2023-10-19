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
        winning_nodes = random.sample(range(n_nodes), n_winning)
        attributes = {}
        for n in self.graph.nodes:
            if n in winning_nodes:
                attributes[n] = {'winning': True}
            else:
                attributes[n] = {'winning': False}
        nx.set_node_attributes(self.graph, attributes)

        # Split nodes between the two players
        self.player0_nodes = [n for n in winning_nodes]
        while len(self.player0_nodes) < n_nodes/2:
            num = random.randint(0, n_nodes-1)
            if num not in self.player0_nodes:
                self.player0_nodes.append(num)
        self.player1_nodes = [node for node in range(n_nodes) if node not in self.player0_nodes]

        print("Nodes of player 0: " + str(self.player0_nodes))
        print("Nodes of player 1: " + str(self.player1_nodes))

        # Color the winning node in the graph
        node_colors = {node: 'red' if node in winning_nodes else 'blue' for node in self.player0_nodes}
        nx.set_node_attributes(self.graph, node_colors, 'color')

        # Create a dictionary for labeling the nodes with their numbers
        self.node_labels = {node: str(node) for node in self.graph.nodes}

    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)
        node_colors = [self.graph.nodes[node]['color'] if 'color' in self.graph.nodes[node] else 'blue' for node in self.player0_nodes]
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.player0_nodes, node_shape='s', node_color=node_colors, label='Player 0 (red if winning node, blue otherwise)')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.player1_nodes, node_color='blue', label='Player 1')
        nx.draw_networkx_labels(self.graph, pos, labels=self.node_labels)
        nx.draw_networkx_edges(self.graph, pos)

        #plt.legend(loc="lower center", bbox_to_anchor=(0.5, 0), title="Legend")
        plt.show()
    
    def get_winning_nodes(self):
        return [n for n in self.graph.nodes if self.graph.nodes[n]['winning']]
    
    def is_winning(self, n):
        return False if (n > self.n_nodes or not self.graph.nodes[n]['winning']) else True
    
    def get_predecessors(self, node):
        return list(self.graph.predecessors(node))
    
    def get_successors(self, node):
        return list(self.graph.successors(node))
    
    def return_graph(self):
        return self.graph
    