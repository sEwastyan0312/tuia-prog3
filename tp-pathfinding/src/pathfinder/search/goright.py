from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GoRight:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Go Right

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

        # Apply objective test
        if grid.objective_test(root.state):
            return Solution(root, reached)

        # Nodo actual, comenzando desde la raiz 
        node = root

        while True:

            # comprobamos si es posible ir a la derecha
            if "right" not in grid.actions(node.state):
                return NoSolution(reached)

            # Obtener el sucesor
            successor = grid.result(node.state, "right")

            # comprobar si el sucesor ya fue alcanzado
            if successor in reached:
                continue

            # Inicializa el nodo hijo
            son = Node(
                "",
                successor,
                cost=node.cost + grid.individual_cost(node.state, "right"),
                parent=node,
                action="right",
            )

            # Marcar el sucesor como alcanzado
            reached[successor] = True

            # Aplicar la prueba de objetivo
            if grid.objective_test(successor):
                return Solution(son, reached)
            
            # Continuar con el hijo
            node = son

