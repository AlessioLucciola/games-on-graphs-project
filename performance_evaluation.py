from datetime import datetime
from tqdm import tqdm
import reachability
import time
import json
import os

# Evaluate the reachability game
def evaluate_reachability(edge_probabilities, n_winnings, n_nodes):
    all_combinations = [(ep, nw, nn) for ep in edge_probabilities for nw in n_winnings for nn in n_nodes]
    results = []

    for ep, nw, nn in tqdm(all_combinations):
        print("----Testing the following configuration:----")
        print(f"Number of nodes: {nn}")
        print(f"Edge probability among nodes: {ep*100}%")
        print(f"Number of winning nodes as a percentage of the total nodes: {nw*100}%")
        start_time = time.time()

        _, _, recursion_count = reachability.reachability_game(n_nodes=nn, edge_probability=ep, n_winning=nw, print_info=False)

        time.sleep(1)
        elapsed_time = (time.time() - start_time) # In seconds

        combination_data = {
            "n_nodes": nn,
            "edge_probability": ep,
            "n_winning": nw,
            "time": elapsed_time,
            "recursion_count": recursion_count
        }

        results.append(combination_data)
        print("---End of the configuration test---")
    
    if os.path.exists("./Evaluations/") == False:
        os.mkdir("./Evaluations/")

    current_datetime = datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"./Evaluations/evaluation_reachability_{current_datetime_str}.json", 'w') as json_file:
        json.dump(results, json_file, indent=2)

edge_probabilities = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5]
#n_winnings = [0.05, 0.1, 0.15, 0.2]
n_winnings = [0.15]
n_nodes = [10, 50, 100, 1000, 3000, 5000]

for i in tqdm(range(20)):
    evaluate_reachability(edge_probabilities, n_winnings, n_nodes)


    

