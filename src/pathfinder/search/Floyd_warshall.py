from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class FloydWarshall:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Floyd Warshall algorithm

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Get a list of all unvisited nodes, excluding the start node
        nodes = grid.get_node(grid.start)

        # Get the number of nodes
        V = len(nodes)

        # Initialize the distance matrix with all values set to infinity
        distance = [[float("inf") for _ in range(V)] for _ in range(V)]

        # Initialize the distance values in the distance matrix
        for i in range(V):
            for j in range(V):
                # If the nodes are neighbors, set the distance to 1
                if nodes[i] in nodes[j].neighbors:
                    distance[i][j] = 1
            # If the two nodes are the same, set the distance to 0
            distance[i][i] = 0

       

        # Used for path reconstruction
        checked_nodes = [grid.start]

        # Iterate through all nodes in the list
        for k in range(V):
            # If the run flag is False, break out of the loop

            

            # Iterate through all pairs of nodes in the list
            for i in range(V):
                for j in range(V):
                    # If the distance between the two nodes is currently longer than
                    # the path through the k-th node, set it to the new shorter distance
                    if distance[i][j] > distance[i][k] + distance[k][j]:
                        distance[i][j] = distance[i][k] + distance[k][j]

                    # If none of the nodes are the start or end nodes, uncheck them
                    if (not nodes[i].is_start() and not nodes[i].is_end() and
                            not nodes[j].is_start() and not nodes[j].is_end() and
                            not nodes[k].is_start() and not nodes[k].is_end()):
                        nodes[i].uncheck()
                        nodes[j].uncheck()
                        nodes[k].uncheck()

            # Draw the updated distances
            grid.draw()

            # If none of the nodes are the start or end nodes, check them again
            if (not nodes[i].is_start() and not nodes[i].is_end() and
                    not nodes[j].is_start() and not nodes[j].is_end() and
                    not nodes[k].is_start() and not nodes[k].is_end()):
                checked_nodes.append(nodes[i])
                checked_nodes.append(nodes[j])
                checked_nodes.append(nodes[k])
                nodes[i].check()
                nodes[j].check()
                nodes[k].check()

        # Adding end if it is connected to start
        try:
            test = nodes.index(grid.end)
            checked_nodes.append(grid.end)
        except ValueError:
            pass

        # Trace the shortest path through the distance matrix
        cells = []
        path_cost = 0
        temp = grid.get_node(pos=grid.end)
        while temp.parent != None:
            cells.append(temp.state)
            path_cost += temp.cost
            temp = temp.parent
        cells.append(grid.start)
        cells.reverse()

        return Solution(cells, checked_nodes, path_cost=path_cost)
