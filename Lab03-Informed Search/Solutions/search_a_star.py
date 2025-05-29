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
            s = Node(child, self, 0, self.depth + 1)
            s.cost=derive_cost(s)
            successors = insert(s, successors)

        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Cost: {self.cost}"


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

'''
Recursively calculates cost of node to its parent, and then from parent to its parent, etc.
'''
def derive_cost(node):
    if node.parent_node is None:
        return 0
    else:
        parent_state = node.parent_node.state
        child_state = node.state
        cost = input_costs[(parent_state, child_state)]+ derive_cost(node.parent_node)
        return cost
    


def remove_global_best(queue: list[Node]) -> Node:
    """Removes the local best element from the input list based on cost.
    The removed element will be returned."""

    if len(queue) > 0:
        index = -1

        # Calculate costs
        for i in range(len(queue)):
            cost = queue[i].cost
            heu = heuristics[queue[i].state]
            total_cost = cost + heu

            if total_cost == queue[index].cost + heuristics[queue[index].state]:
                if heu < heuristics[queue[index].state]:
                    index = i
            elif total_cost < queue[index].cost + heuristics[queue[index].state]:
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
            node = remove_global_best(fringe)
            if node.state in self.goal_state:
                return node.path()
            children = node.expand(self.state_space)
            fringe = insert_all(children, fringe, insert_as_first)
            print(f"Fringe: {fringe}")

    def run(self, insert_as_first: bool = True):
        path = self.tree_search(insert_as_first)
        print("Solution path:")
        total_costs = path[0].cost
        for node in path:
            node.display()
        
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

    heuristics = {
        'A': 6,
        'B': 5,
        'C': 5,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 4,
        'H': 1,
        'I': 2,
        'J': 1,
        'K': 0,
        'L': 0,
    }
    
    goal_state = ['K', 'L']
    searcher = Searcher('A', goal_state, state_space=StateSpace(input_state_space))
    print("A-star-search")
    searcher.run(insert_as_first=True) 