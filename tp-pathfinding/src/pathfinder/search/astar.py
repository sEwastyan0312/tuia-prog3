from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        # Distancia Manhattan (válida para grillas 4-direcciones)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
   
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Reached: estado -> mejor g(n)
        reached = {root.state: root.cost}

        # Frontier: prioridad = f(n) = g(n) + h(n)
        frontier = PriorityQueueFrontier()
        h0 = AStarSearch.heuristic(root.state, grid.end)
        frontier.add(root, priority=root.cost + h0)
        

        while frontier.frontier:
            node = frontier.pop()

            # Test objetivo al extraer
            if grid.objective_test(node.state):
                return Solution(node, reached)

            # Expandir
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)
                new_cost = node.cost + grid.individual_cost(node.state, action)

                # Si no visto o mejor camino
                if successor not in reached or new_cost < reached[successor]:
                    reached[successor] = new_cost

                    child = Node(
                        value="",
                        state=successor,
                        cost=new_cost,
                        parent=node,
                        action=action
                    )

                    h = AStarSearch.heuristic(successor, grid.end)
                    frontier.add(child, priority=new_cost + h)

        

        return NoSolution(reached)
