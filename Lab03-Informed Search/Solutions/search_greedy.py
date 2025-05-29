from typing import Self, Any

# For this lab, we will use the searcher implementation from uninformed search
# we will expand the search to utilize the heuristic cost for Greedy and A-star algorithms

class StateSpace:
    def __init__(self, state_space: dict = None):
        self.state_space = state_space

    def successor(self, state: Any):
        if self.state_space is None:
            print("No state space set")

        return self.state_space[state]


class Node:
    def __init__(self, state: Any, parent: Self = None, cost: int = 0, depth: int = 0):
        self.state = state
        self.parent_node = parent
        self.cost = cost
        self.depth = depth

    def path(self) -> list[Self]:                       # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.parent_node:                 # while current node has parent
            current_node = current_node.parent_node     # make parent the current node
            path.append(current_node)                   # add current node to path

        return path
    
    def expand(self, state_space: StateSpace):
        successors: list[Node] = []
        children = state_space.successor(self.state)
        for child in children:
            s = Node(child, self, input_heuristics[(self.state, child)], self.depth + 1)
            successors = insert(s, successors)

        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Depth: {self.depth}"


def insert(node: Node, queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """
    Returns the queue with the node inserted (the fringe).
    Use the insert_as_first parameter to decide if the node should be inserted at the beginning or the end of the queue.
    """  
    if insert_as_first:
        queue.insert(0, node)  # DFS
    else:
        queue.append(node)      # BFS

    return queue


def insert_all(nodes_to_add: list[Node], queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """
    Inserts all nodes from the input list, into the queue using the insert function defined in this script.
    """
    for node in nodes_to_add:
        insert(node, queue, insert_as_first)
    return queue


def local_cost(node):
    if node.parent_node is None:
        return 0
    else:
        parent_state = node.parent_node.state
        child_state = node.state
        cost = input_heuristics[(parent_state, child_state)]
        return cost
    

def remove_local_best(queue: list[Node]) -> Node:
    """Removes the local best element from the input list based on cost.
    The removed element will be returned."""

    if len(queue) > 0:
        costs = []
        index = -1
        # Calculate costs
        for i in range(len(queue)):
            costs.append(local_cost(queue[i]))
        # Get lowest costs
        local_best = min(costs)
        # Find index of lowest costs
        for i in range(len(costs)):
            if costs[i] == local_best:
                index = i
        # Pop lowest costs
        best_node = queue.pop(index)
        return best_node
    return []


class Searcher:
    def __init__(self, initial_state, goal_state, state_space: StateSpace = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space

    def tree_search(self, insert_as_first: bool = True) -> list[Node]:
        """Search the tree for the goal state
        and return the path from the initial state to the goal state."""
        fringe: list[Node] = []
        initial_node = Node(self.initial_state)
        fringe = insert(initial_node, fringe)
        while fringe is not None:
            node = remove_local_best(fringe)
            if node.state in self.goal_state:
                return node.path()
            children = node.expand(self.state_space)
            fringe = insert_all(children, fringe, insert_as_first)
            print(f"Fringe: {fringe}")

    def run(self, insert_as_first: bool = True):
        path = self.tree_search(insert_as_first)
        print("Solution path:")
        total_costs = 0
        for node in path:
            node.display()
            if node.parent_node is not None:
                total_costs += input_costs[(node.parent_node.state, node.state)]
        print('Total cost of path: ' + str(total_costs))


if __name__ == '__main__':
    input_state_space =  {'A': ['B', 'C', 'D'],
               'B': ['E', 'F'],
               'C': ['E'],
               'D': ['H', 'I', 'J'],
               'E': ['G', 'H'],
               'F': ['G'],
               'G': ['K'],
               'H': ['K', 'L'],
               'I': ['L'],
               'J': [],
               'K': [],
               'L': [],
               }

    input_heuristics = {
        ('A', 'B'): 5,
        ('A', 'C'): 5,
        ('A', 'D'): 2,
        ('B', 'F'): 5,
        ('B', 'E'): 4,        
        ('C', 'E'): 4,
        ('D', 'H'): 1,
        ('D', 'I'): 2,
        ('D', 'J'): 1,        
        ('E', 'G'): 4,
        ('E', 'H'): 1,
        ('F', 'G'): 4,        
        ('G', 'K'): 0,
        ('H', 'K'): 0,
        ('H', 'L'): 0,
        ('I', 'L'): 0,
    }
    input_costs = {
        ('A', 'B'): 1,
        ('A', 'C'): 2,
        ('A', 'D'): 4,
        ('B', 'F'): 5,
        ('B', 'E'): 3,
        ('C', 'E'): 1,
        ('D', 'H'): 1,
        ('D', 'I'): 4,
        ('D', 'J'): 2,
        ('E', 'G'): 2,
        ('E', 'H'): 3,
        ('F', 'G'): 1,
        ('G', 'K'): 6,
        ('H', 'K'): 6,
        ('H', 'L'): 5,
        ('I', 'L'): 3,
    }

    goal_state = ['K', 'L']
    searcher = Searcher('A', goal_state, state_space=StateSpace(input_state_space))
    print("Greedy-best-first")
    searcher.run(insert_as_first=True)