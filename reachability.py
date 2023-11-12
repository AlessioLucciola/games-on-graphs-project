import graph_creation as gc
from collections import deque

def reachability_game(n_nodes=10, edge_probability=0.5, n_winning=0.1, visualize=False, print_info=True):
    G = gc.Graph(n_nodes, edge_probability, n_winning, mode='reachability')
    W = G.get_winning_nodes()
    if print_info:
        print("Winning nodes: " + str(W))
    strategy, win_region, recursion_count = solve_reachability(G, W, print_info)
    if visualize:
        G.visualize_graph()
    
    return strategy, win_region, recursion_count

"""
    This function takes a direct graph and a set terminal nodes and solve reachability games.

    :param G: A direct graph.
    :param W: A (non-empty) set of terminal (winning) nodes.
    :return: strategy: A dictionary where the key is the current node and the value is a successor that,
                        if chosen, allows player 0 to stay in the winning region.
    :return: win_region: A set of nodes from which player 0 can force player 1 to a winning node.
""" 
def solve_reachability(G, W, print_info):
    queue = set() # Add nodes to be visited yet at execution time
    strategy = {} # Keep track of a possible strategy for player 0 to reach a winning node
    win_region = set(W) # Immediatly set the winning node of player 0 in the winning region
    lose_region = set() # Initialize the losing region as an empty set
    recursion_count = 0

    for w in W: # For each winnining node 
        queue.add(w) # Add a winning node to the queue
    
        while queue:
            recursion_count += 1  # Increment the recursion count
            n = queue.pop() #Retrieve the first element from the queue
            for pred in G.get_predecessors(n): # If the predecessor is of player 0 then -> add pred in win_region X
                #print(str(n) + " " + str(pred))
                if pred in G.player0_nodes:
                    if (pred not in win_region):
                        queue.add(pred)
                        win_region.add(pred)
                        strategy[pred] = n
                else: # If the predecessor is of player 1 (opponent) and all the successors are in the win_region X then -> add pred in win_region X
                    if (pred not in win_region) and all(succ in win_region for succ in G.get_successors(pred)):
                        queue.add(pred)
                        win_region.add(pred)
                        strategy[pred] = n
    
    lose_region = set(range(len(G.graph.nodes))) - win_region

    if print_info:
        print("Strategy: " + str(strategy))
        print("Winning region: " + str(win_region))
        print("Losing region: " + str(lose_region))

    return(strategy, win_region, recursion_count)

reachability_game()