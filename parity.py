import graph_creation as gc
import networkx as nx

def parity_game(n_nodes=15):
    G = gc.Graph(n_nodes) # Create graph
    strategy_si = solve_parity_strategy_improvement(G)
    print("Winning regions strategy improvement: " + str(strategy_si))
    strategy_zi = solve_parity_zielonka(G)
    print("Winning strategy Zielonka: " + str(strategy_zi))
    #G.visualize_graph()

    diff = find_differences(strategy_si, strategy_zi)
    print("Differences among the strategies: " + str(diff))

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

                # If the parity of the node is different from the max successor parity
                # update the parity of the node
                if parities[node] != node_parity:
                    strategy[node] = player
                    parities[node] = node_parity
                    has_changed = True

        player = 1 if player == 0 else 0 # Change player at each iteration

        if not has_changed:
            break

    return strategy

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


def dfs(G, node, component, visited):
    if node not in visited: visited.append(node)
    if node not in component: component.append(node)
    for successor in G.successors(node):
        if successor not in visited:
            dfs(G, successor, component, visited)
    return component

def find_differences(strategy1, strategy2):
    return [key for key in strategy1 if strategy1[key] != strategy2[key]]

parity_game()