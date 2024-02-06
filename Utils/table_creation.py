import json

# Create a table in markdown from the results data
def create_table(edge_probability, data):
    print("{\\begin{longtable}{|c|c|c|c|c|}")
    print("\\hline")
    print(f"\multicolumn{{4}}{{|c|}}{{edge\_probability={edge_probability}}} \\\\")
    print("\\hline")
    print("\\textbf{n\_nodes} & \\textbf{Time (in sec)} & \\textbf{Recursion Counts} \\\\")
    print("\\hline")
    print("\\endhead")

    #Put data here
    for row in data:
        print(f"{row[0]} & {round(row[1], 10)} & {row[2]} \\\\")
        print("\\hline")
    ###

    print(f"\\caption{{Performance evaluation results with edge\\_probability={edge_probability}}}")
    print(f"\\label{{tab:results_table_ep{edge_probability}}}")
    print("\\end{longtable}}")

def upload_and_read_data_jsons(files):
    data_list = []
    for file in files:
        with open("./Evaluations/"+file, 'r') as file:
            data = json.load(file)
            data_list.append(data)
    return data_list

def extract_data_for_table(files, edge_probability):
    time_dict = {}
    rec_dict = {}
    data_list = upload_and_read_data_jsons(files)
    for data in data_list:
        for conf in data:
            if conf["edge_probability"] == edge_probability:
                if conf["n_nodes"] in time_dict:
                    time_dict[conf["n_nodes"]] = time_dict[conf["n_nodes"]] + conf["time"]
                    rec_dict[conf["n_nodes"]] = rec_dict[conf["n_nodes"]] + conf["recursion_count"]
                else:
                    time_dict[conf["n_nodes"]] = conf["time"]
                    rec_dict[conf["n_nodes"]] = conf["recursion_count"]
    time_dict = {key: value / len(files) for key, value in time_dict.items()}
    rec_dict = {key: value / len(files) for key, value in rec_dict.items()}

    result_list = []
    for key in time_dict:
        result_list.append([key, time_dict[key], rec_dict[key]])
    return result_list

files = ["evaluation_reachability_2023-11-17_10-32-58.json"]
edge_probability = 0.5
data = extract_data_for_table(files, edge_probability)
create_table(edge_probability, data)