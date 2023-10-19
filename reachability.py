import graph_creation as gc
from collections import deque, defaultdict

def reachability_game(n_nodes=10):
    G = gc.Graph(n_nodes)
    W = G.get_winning_nodes()
    r = solve_reachability(G, W)
    print("Winning nodes: " + str(W))
    print("Ranks: " + str(r))
    G.visualize_graph()

"""
    This function takes a direct graph and a set terminal nodes and solve reachability games.
    It measure how many nodes can be reached from a given node within a certain number of steps.

    :param G: A direct graph
    :param W: A (non-empty) set of terminal (winning) nodes
    :return: A dictionary of nodes. The key is the id of the node, the value represents it rank that
            is the number of steps that are needed to reach a winning node. If 0 the node is a winning one.
            If infinity, it is not possible to reach a winning one from that specific node.
""" 
def solve_reachability(G, W):
    #Initialize distances and visited flags
    rank = {}
    for node in G.graph.nodes():
        #Terminal nodes have a rank of 0, the others are initialized with infinity
        rank[node] = 0 if node in W else float('inf')

    '''
    #For each terminal node
    for terminal_node in W:
        visited = set()
        queue = deque()
        queue.append(terminal_node)
        visited.add(terminal_node)
        depth = 0

        while queue: #Recursive approach that implement a depth-first search (DFS)
            depth += 1
            for _ in range(len(queue)): 
                current_node = queue.popleft() #Retrieve the first element from the queue
                for prec in G.predecessors(current_node): #For all predecessors of that element
                    if prec not in visited: #If it is not visisted yet
                        queue.append(prec)
                        visited.add(prec)
                        if depth < rank[prec]: #Update the rank only if the current depth is smaller than the one already registered
                            rank[prec] = depth

    return rank
    '''
    queue = deque()
    win_region = [w for w in W]

    for w in W:
        queue.append(w)
    
        while queue:
            n = queue.popleft() #Retrieve the first element from the queue
            for pred in G.get_predecessors(n):
                print(str(n) + " " + str(pred))
                if pred in G.player0_nodes:
                    if (pred not in win_region):
                        queue.append(pred)
                        win_region.append(pred)
                else:
                    if (pred not in win_region) and all(succ in win_region for succ in G.get_successors(pred)): # To do: The second condition may not be valid at first so the node can be discarded if it is eventually in the winning region 
                        queue.append(pred)
                        win_region.append(pred)
    
    print("Winning region: " + str(win_region))


reachability_game()