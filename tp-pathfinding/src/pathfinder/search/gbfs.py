from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # reached (solo para evitar repetir estados)
        reached = {}
        reached[root.state] = True

        # Test objetivo inicial
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # Frontera con prioridad por heurística
        frontier = PriorityQueueFrontier()
        h = GreedyBestFirstSearch.heuristic(root.state, grid.end)
        frontier.add(root, priority=h)

        while frontier.frontier:
            node = frontier.pop()

            # Test objetivo
            if grid.objective_test(node.state):
                return Solution(node, reached)

            # Expandir nodo
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)

                if successor not in reached:

                    child = Node(
                        value="",
                        state=successor,
                        cost=node.cost + grid.individual_cost(node.state, action),
                        parent=node,
                        action=action
                    )

                    reached[successor] = True

                    # Prioridad = heurística
                    h = GreedyBestFirstSearch.heuristic(successor, grid.end)
                    frontier.add(child, priority=h)

        return NoSolution(reached)
