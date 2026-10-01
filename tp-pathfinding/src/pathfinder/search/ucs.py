from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

         # Test objetivo inicial
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # Frontera con prioridad (menor costo primero)
        frontier = PriorityQueueFrontier()
        frontier.add(root, priority=root.cost)

        while frontier.frontier:
            # Extrae el nodo de menor costo
            node = frontier.pop()

            # Test objetivo (en UCS va acá)
            if grid.objective_test(node.state):
                return Solution(node, reached)

            # Expandir nodo
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)

                # Calcular nuevo costo acumulado
                new_cost = node.cost + grid.individual_cost(node.state, action)

                # Si no fue visitado o encontramos un mejor camino
                if successor not in reached or new_cost < reached[successor]:

                    # Crear nodo hijo
                    child = Node(
                        value="",
                        state=successor,
                        cost=new_cost,
                        parent=node,
                        action=action
                    )

                    # Actualizar el mejor costo
                    reached[successor] = new_cost

                    # Agregar a la frontera con prioridad
                    frontier.add(child, priority=new_cost)

        return NoSolution(reached)

