import graph_creation as gc
import networkx as nx

def parity_game(n_nodes=15):
    G = gc.Graph(n_nodes, mode='parity') # Create graph
    strategy_si = solve_parity_strategy_improvement(G)
    print("Winning regions strategy improvement: " + str(strategy_si))
    strategy_sip = solve_parity_strategy_improvement_par(G)
    print("Winning regions strategy improvement (parallelized): " + str(strategy_sip))
    strategy_zi = solve_parity_zielonka(G)
    print("Winning strategy Zielonka: " + str(strategy_zi))

    diff1 = find_differences(strategy_si, strategy_sip)
    print("Differences among the strategy improvement approches: " + str(diff1))
    diff2 = find_differences(strategy_si, strategy_zi)
    print("Differences among the standard strategy improvement and zielonka: " + str(diff2))
    diff3 = find_differences(strategy_si, strategy_sip)
    print("Differences among the zielonka and the strategy improvement parallelized: " + str(diff3))

    G.visualize_graph()

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

def solve_parity_strategy_improvement_par(G):
    parities = {node: node for node in G.graph.nodes} # Assign a priority to each node
    strategy = {node: -1 for node in G.graph.nodes} # Initialize the strategy of each node with -1

    while True: # Running until the parities change
        has_changed = False
        for node in G.graph.nodes:
            successors = list(G.graph.successors(node))
            if successors: #If there are successors
                successor_parities = [parities[successor] for successor in successors] # Calculate the parity of the successors
                node_parity = max(successor_parities) if node in G.player0_nodes else min(successor_parities) # Select the max parity

                # If the parity of the node is different from the max successor parity
                # update the parity of the node
                if parities[node] != node_parity:
                    #print(parities[node], node_parity)
                    strategy[node] = 0 if node in G.player0_nodes else 1
                    #Note: There are some cases in which if the node and successor are from the same player, a loop occurs when selecting the max/min successor (10->12, 12->10, 10->12, etc..).
                    #This for is to avoid this kind of loop. So if the successor is of the same player and the assigned parity is already larger of the found one, avoid updating the parity.
                    if (node in G.player0_nodes and parities[node] > node_parity) or (node in G.player1_nodes and parities[node] < node_parity):
                        pass
                    else:
                        parities[node] = node_parity
                        has_changed = True
            else:
                strategy[node] = 0 if node in G.player0_nodes else 1

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