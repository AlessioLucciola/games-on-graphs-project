import graph_creation as gc

def solve_reachability():
    G = gc.Graph(100, 0.2)
    G.visualize_graph()
    print(G.return_winning_nodes())

solve_reachability()