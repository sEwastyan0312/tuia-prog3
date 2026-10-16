from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Inicializar el diccionario de estados expandidos
        expanded = dict()

        # Inicializar la frontera con el nodo raiz 
        frontier = StackFrontier()
        frontier.add(root)

        # Bucle Principal
        while not frontier.is_empty():
            # Extraer el nodo mas profundo no expandido (LIFO)
            node = frontier.remove()

            # Si el nodo ya ha sido expandido, se omite para evitar ciclos infinitos
            if node.state in expanded:
                continue

            # Marcar el estado del nodo actual como expandido
            expanded[node.state] = True

            # Prueba de objetivo tardia: comprueba si se encontro la solucion al expandir
            if grid.objective_test(node.state):
                return Solution(node, expanded)

            # Expandir el nodo analizando todas las acciones posibles
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)

                # Solo añadir a la frontera si el estado aun no ha sido expandido 
                if successor not in expanded:
                    # Crear el nodo hijo
                    child = Node(
                        value="",
                        state=successor,
                        cost=node.cost + grid.individual_cost(node.state, action),
                        parent=node,
                        action=action
                    )
                    
                    # Añadir el nuevo hijo a la frontera de tipo pila
                    frontier.add(child)

        # Si la frontera esta vacia y no se encontro solucion 
        return NoSolution(expanded)
