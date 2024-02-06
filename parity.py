# Temptative to solve parity games using the strategy improvement algorithm and Zielonka's recursive algorithm.

import graph_creation as gc
from config import *

"""
    Init function for the parity game. It creates a graph and solves the parity game.

    :param n_nodes: Number of nodes in the graph.
    :param edge_probability: Probability of an edge between two nodes.
    :param visualize: Visualize the (randomly created) graph at each game.
    :param print_info: Print the strategy, winning and losing regions.

    :return: strategy_si: Stategy given by the strategy improvement algorithm.
    :return: strategy_zi: Stategy given by Zielonka's recursive algorithm.
"""
def parity_game(n_nodes, edge_probability, visualize=False, print_info=True):
    G = gc.Graph(n_nodes, edge_probability, n_winning=0, mode='parity') # Create graph
    strategy_si = solve_parity_strategy_improvement(G)
    strategy_zi = solve_parity_zielonka(G)
    if print_info:
        print("Winning regions strategy improvement: " + str(strategy_si))
        print("Winning strategy Zielonka: " + str(strategy_zi))

    if visualize:
        G.visualize_graph()

    return strategy_si, strategy_zi

"""
    This function takes a direct graph and solve parity games using the strategy improvement algorithm.

    :param G: A direct graph.
    :return: strategy: A dictionary where the key is the current node and the value is a successor that, if chosen, allows player 0 to stay in the winning region.
"""
def solve_parity_strategy_improvement(G):
    parities = {node: node for node in G.graph.nodes} # Assign a priority to each node
    strategy = {node: -1 for node in G.graph.nodes} # Initialize the strategy of each node with -1
    player = 0

    while True: # Running until the parities change
        has_changed = False
        current_player_nodes = G.player0_nodes if player == 0 else G.player1_nodes
        for node in current_player_nodes:
            successors = list(G.graph.successors(node))
            if successors: #If there are successors
                successor_parities = [parities[successor] for successor in successors] # Calculate the parity of the successors
                node_parity = max(successor_parities) if player == 0 else min(successor_parities) # Select the max parity

                # If the parity of the node is different from the max successor parity update the parity of the node
                if parities[node] != node_parity:
                    strategy[node] = player
                    #Note: There are some cases in which if the node and successor are from the same player, a loop occurs when selecting the max/min successor (10->12, 12->10, 10->12, etc..).
                    #This for is to avoid this kind of loop. So if the successor is of the same player and the assigned parity is already larger of the found one, avoid updating the parity.
                    if node in G.player0_nodes and parities[node] > node_parity:
                        pass
                    else:
                        parities[node] = node_parity
                        has_changed = True
            else:
                strategy = player

        player = 1 if player == 0 else 0 # Change player at each iteration

        if not has_changed:
            break

    return strategy

"""
    This function takes a direct graph and solve parity games using Zielonka's recursive algorithm.

    :param G: A direct graph.
    :return: strategy: A dictionary where the key is the current node and the value is a successor that, if chosen, allows player 0 to stay in the winning region.
"""

def solve_parity_zielonka(G):
    Gc = G.graph.copy()
    priorities = {node: node for node in G.graph.nodes} # Assign a priority to each node
    strategy = {node: -1 for node in G.graph.nodes} # Initialize the strategy of each node with -1
    components = [] # Initialize a list where to put each component of the graph

    while len(Gc.nodes) > 0: # Iterate until all components are found
        highest_priority = max(priority for priority in priorities.values() if priority in Gc.nodes) # Get the highest priority in the graph
        component = dfs(Gc, highest_priority, [], []) # Apply dfs from the highest priority node to get the associated component
        components.append(component) 
        for n in component: # Remove the nodes in the found component
            Gc.remove_node(n)

    for component in components: # For each component found
        subgame = G.graph.subgraph(component) # Create a subgame from the initial graph
        for n in subgame.nodes(): # Assign winning strategies
            if priorities[n] % 2 == 0:
                strategy[n] = 0
            else:
                strategy[n] = 1
    return strategy

"""
    Depth-first search algorithm to find the components of a graph.

    :param G: A graph.
    :param node: The current node.
    :param component: The current component.
    :param visited: The visited nodes.

    :return: component: A list of nodes that are part of the same component.
"""
def dfs(G, node, component, visited):
    if node not in visited: visited.append(node)
    if node not in component: component.append(node)
    for successor in G.successors(node):
        if successor not in visited:
            dfs(G, successor, component, visited)
    return component

if __name__ == "__main__":
    parity_game(n_nodes=N_NODES, edge_probability=EDGE_PROBABILITY, visualize=VISUALIZE_GRAPH, print_info=PRINT_INFO)