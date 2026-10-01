from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

         # Primer test objetivo
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # Crea la frontera con la clase queue (FIFO) y añade root para luego expandirlo
        frontier = QueueFrontier()
        frontier.add(root)

        
        while not frontier.is_empty():
            # Saca un nodo de la frontera, el primero que entra, sale primero
            node = frontier.remove()

            # Se expande el nodo con todas las acciones posibles
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)

                # Chequea que la posicion nueva no haya sido explorada antes, para evitar bucles
                if successor not in reached:
                    # Crea el nodo hijo
                    child = Node(
                        value="",
                        state=successor,
                        cost=node.cost + grid.individual_cost(node.state, action),
                        parent=node,
                        action=action
                    )

                    # Se agrega el nodo hijo al diccionario de alcanzados con valor True
                    reached[successor] = True

                    # Chequea si successor es la posición obj
                    if grid.objective_test(successor):
                        return Solution(child, reached)

                    # Añade el hijo a la frontera
                    frontier.add(child)

        # Si no encontró solución, devuelve NoSolution
        return NoSolution(reached)
