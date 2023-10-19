
<p align="center"><img src="routeviz.png" height = "256" ></img></p>
<p align="center">

RouteViz is a repository dedicated to providing interactive visualizations of popular pathfinding algorithms using Python and Pygame. This project offers a hands-on way to understand and explore the mechanics of algorithms.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Pathfinding algorithms are fundamental in computer science and find applications in various domains, from video games to network routing. Understanding how these algorithms work can be complex, but visualizing them can make the learning process more intuitive and enjoyable.

RouteViz simplifies this learning experience by providing visual representations of pathfinding algorithms in action. Users can interact with the visualizations, gain insights into algorithm behaviors, and even experiment with custom scenarios.

## Features

- **Interactive Visualizations:** Watch Pathfinding algorithms in action with interactive, real-time visualizations.
- **Custom Scenarios:** Create your own maps, set start and end points, and run the algorithms on custom scenarios to experiment with different situations.
- **Step-by-Step Control:** Step through the algorithm's execution to observe how it evaluates and selects paths.
- **Educational Tool:** RouteViz is a valuable resource for students, educators, and anyone interested in understanding and teaching pathfinding algorithms.

# Algorithms present

- [x] Dijkstra's Algorithm:

Dijkstra's algorithm finds the shortest path from a source node to all other nodes in a weighted graph (where each edge has a non-negative weight).
It is based on a greedy strategy, always choosing the node with the smallest tentative distance from the source.
Dijkstra's algorithm guarantees the shortest path but is not efficient for graphs with negative edge weights.

- [x] A*Algorithm:

A* is an extension of Dijkstra's algorithm that uses a heuristic to prioritize nodes. The heuristic provides an estimate of the cost from the current node to the target.
It combines the advantages of both Dijkstra's algorithm and greedy best-first search.
A* is widely used in applications where finding the shortest path quickly is important, such as in games and maps.

- [x] Breadth-First Search (BFS):

BFS explores all possible paths from the source in a level-by-level manner. It is primarily used for unweighted graphs.
While BFS doesn't necessarily find the shortest path, it does find a path with the fewest number of edges.

- [x] Depth-First Search (DFS):

DFS explores as far as possible along each branch before backtracking. It is not typically used for finding the shortest path but can be adapted for certain cases.

- [ ] Bellman-Ford Algorithm:

The Bellman-Ford algorithm finds the shortest path in a weighted graph, even if it contains negative weight edges (as long as there are no negative cycles).
It can handle a wider range of edge weight scenarios compared to Dijkstra's algorithm.

- [ ] Floyd-Warshall Algorithm:

The Floyd-Warshall algorithm is used to find the shortest path between all pairs of nodes in a weighted graph. It can handle negative edge weights, but not negative cycles.

## Installation

To run RouteViz on your local machine, follow these steps:

1. Clone the repository to your computer.
   ```bash
   git clone https://github.com/NebulaTris/RouteViz.git
   ```
   
2. Navigate to the project directory.
   ```bash
   cd RouteViz
   ```

3. Install the required Python libraries. You can use `pip` to install them from the provided `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the RouteViz application.

- On Windows, run 
```bash
   python run.pyw
```
- On Linux, run
```bash
   python3 run.pyw
```

2. Use the interactive GUI to select an algorithm, create a map, set start and end points, and visualize the algorithm in action.

3. Step through the algorithm's execution to gain a better understanding of its decision-making process.

4. Experiment with custom scenarios to see how the algorithms behave under different conditions.

## Contributing

Contributions to RouteViz are welcome! Whether you want to fix a bug, add a new feature, or improve the documentation, please feel free to contribute. Please follow the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

RouteViz is released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as long as the original license is included.