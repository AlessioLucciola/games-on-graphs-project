from datetime import datetime
from tqdm import tqdm
from os import path
import reachability
import time
import json
import os

def evaluate_reachability(edge_probabilities, n_winnings, n_nodes):
    all_combinations = [(ep, nw, nn) for ep in edge_probabilities for nw in n_winnings for nn in n_nodes]
    results = []

    for ep, nw, nn in tqdm(all_combinations):
        start_time = time.time()

        _, _, recursion_count = reachability.reachability_game(n_nodes=nn, edge_probability=ep, n_winning=nw)

        time.sleep(1)
        elapsed_time = (time.time() - start_time) / 60.0

        combination_data = {
            "n_nodes": nn,
            "edge_probability": ep,
            "n_winning": nw,
            "time": elapsed_time,
            "recursion_count": recursion_count
        }

        results.append(combination_data)
    
    if path.exists("./Evaluations/") == False:
        os.mkdir("./Evaluations/")

    current_datetime = datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"./Evaluations/evaluation_{current_datetime_str}.json", 'w') as json_file:
        json.dump(results, json_file, indent=2)

#edge_probabilities = [0.02, 0.05, 0.1, 0.2, 0.35, 0.5]
#n_winnings = [0.05, 0.1, 0.15, 0.2]
#n_nodes = [10, 50, 100, 1000, 3000, 10000]

edge_probabilities = [0.5]
n_winnings = [0.2]
n_nodes = [50]

evaluate_reachability(edge_probabilities, n_winnings, n_nodes)


    

