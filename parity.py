import graph_creation as gc
from collections import deque

def parity_game(n_nodes=10):
    G = gc.Graph(n_nodes)
    print(solve_parity(G))
    G.visualize_graph()

def solve_parity(G):
    parities = {node: node % 2 for node in G.graph.nodes}
    print(parities)
    player = 0
    strategy = {}

    while True:
        has_changed = False

        for node in G.graph.nodes:
            successors = list(G.graph.successors(node))
            if not successors:
                continue  # Skip terminal nodes

            # Calculate the parity of the successors
            successor_parities = [parities[successor] for successor in successors]
            node_parity = max(successor_parities)

            if parities[node] != node_parity:
                # Update the strategy for the current player
                strategy[node] = player
                parities[node] = node_parity
                has_changed = True

        player = 1 if player == 0 else 0

        if not has_changed:
            break

    print(strategy)

parity_game()