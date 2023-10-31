import graph_creation as gc
import networkx as nx

def parity_game(n_nodes=10):
    G = gc.Graph(n_nodes) # Create graph
    print(solve_parity(G))
    #G.visualize_graph()
'''
def solve_parity(G):
    parities = {node: node for node in G.graph.nodes}
    player = 0
    strategy = {}

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

        player = 1 if player == 0 else 0

        if not has_changed:
            break

    print(strategy)
'''

def solve_parity(G):
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
def solve_parity(G):
    # Priority Promotion
    priorities = promote_priorities(G)
    
    # Strategy Improvement
    strategy = {}
    for node in G.graph.nodes:
        if node in G.player0_nodes:
            strategy[node] = assign_strategy(node, G, priorities)

    print(strategy)
    
    # Check Winning Conditions
    if all(node in strategy for node in G.graph.nodes) and all(priorities[node] % 2 != 0 for node in strategy):
        return "Player 1 wins"
    if 0 in strategy.values():
        return "Player 0 wins"
    return "No winner yet"

def promote_priorities(G):
    priorities = {node: float('inf') for node in G.graph.nodes}
    sorted_priorities = sorted(set(nx.get_node_attributes(G.graph, 'priority').values()), reverse=True)

    for priority in sorted_priorities:
        nodes_to_promote = [node for node in G.graph.nodes if G.graph.nodes[node]['priority'] == priority]
        for node in nodes_to_promote:
            if node in G.player0_nodes:
                successors = list(G.graph.successors(node))
                if successors:
                    min_successor_priority = min([priorities[successor] for successor in successors])
                    priorities[node] = min(priorities[node], min_successor_priority)
            else:
                successors = list(G.graph.successors(node))
                if successors:
                    max_successor_priority = max([priorities[successor] for successor in successors])
                    priorities[node] = max(priorities[node], max_successor_priority)
        for node in nodes_to_promote:
            G.graph.remove_node(node)
    
    return priorities

def assign_strategy(node, G, priorities):
    successors = list(G.graph.successors(node))
    for successor in successors:
        if successor in G.player0_nodes and priorities[successor] < priorities[node]:
            return successor
    return None
'''

parity_game()