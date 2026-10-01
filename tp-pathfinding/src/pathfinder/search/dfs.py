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

        # Initialize expanded with the empty dictionary
        expanded = dict()

        # Initialize frontier with the root node
        frontier = StackFrontier()
        frontier.add(root)

        # Main loop
        while not frontier.is_empty():
            # Extract the deepest unexpanded node (LIFO)
            node = frontier.remove()

            # If the node has already been expanded, skip it to avoid infinite cycles
            if node.state in expanded:
                continue

            # Mark the current node's state as expanded
            expanded[node.state] = True

            # Late Goal Test: Check if we found the solution upon expansion
            if grid.objective_test(node.state):
                return Solution(node, expanded)

            # Expand the node by looking at all possible actions
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)

                # Only add to frontier if the state hasn't been expanded yet
                if successor not in expanded:
                    # Create the child node
                    child = Node(
                        value="",
                        state=successor,
                        cost=node.cost + grid.individual_cost(node.state, action),
                        parent=node,
                        action=action
                    )
                    
                    # Add the new child to the stack frontier
                    frontier.add(child)

        # If the frontier is empty and no solution was found
        return NoSolution(expanded)
