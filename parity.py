import graph_creation as gc
import networkx as nx

def parity_game(n_nodes=10):
    G = gc.Graph(n_nodes) # Create graph
    strategy_si = solve_parity_strategy_improvement(G)
    print("Winning regions strategy improvement: " + str(strategy_si))
    strategy_zi = solve_parity_zielonka(G)
    print("Winning strategy Zielonka: " + str(strategy_zi))
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
                node_parity = max(successor_parities) # Select the max parity

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
    priorities = {node: 0 if node in G.player0_nodes else 1 for node in G.graph.nodes} # Assign a priority to each node
    strategy = {node: -1 for node in G.graph.nodes} # Initialize the strategy of each node with -1
    components = []

    while len(Gc.nodes) > 0:
        highest_priority = max(priorities.values())
        component = dfs(Gc, highest_priority, [], [])
        components.append(component)
        for n in component:
            Gc.remove_node(n)

        for component in components:
            subgame = G.graph.subgraph(component)
            for n in subgame.nodes():
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

'''
def solve_parity_zielonka(G):
    priority = [0 for _ in range(len(G.graph.nodes))]
    winner = [0 for _ in range(len(G.graph.nodes))]

    for node in range(len(G.graph.nodes)):
        priority[node] = max(G.graph.nodes[node])

        print(priority)

    for i in range(max(priority), -1, -1):
        for node in range(len(G.graph.nodes)):
            if priority[node] == i:
                min_priority = float('inf')
                for neighbor in G.graph.nodes[node]:
                    if priority[neighbor] < min_priority:
                        min_priority = priority[neighbor]
                        winner[node] = winner[neighbor]

                priority[node] = min_priority

    #return winner
'''

parity_game()