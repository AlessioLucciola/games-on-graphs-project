# Games on Graphs Project
Final project for the master's degree in Computer Science AFC course "Games on Graphs" at the University of Rome "La Sapienza" (A.Y. 2023-2024).

This project aims to create a Reachability Games Solver. Reachability games are a class of two-player combinatorial games played on directed graphs. In these games, players aim to reach or avoid specific vertices within the graph.
This repository also contains a temptative to create a Parity Games Solver using the Stategy Improvement and Zielonka Algorithms. Parity games are another class of two-player combinatorial games played on directed graphs, which extend reachability games by incorporating additional complexity through the concept of priorities assigned to vertices.

You can find more details in the [project report](https://github.com/AlessioLucciola/games-on-graphs-project/blob/main/Report/Games_on_Graphs_Report.pdf).

## Setup
If you use Anaconda, create the environment using:

```
conda env create -f environment.yaml
conda activate gog_project
```

Run the game solvers by executing the `reachability.py` or `parity.py` files. It is possibile to change the game configurations in the `config.py` file.
