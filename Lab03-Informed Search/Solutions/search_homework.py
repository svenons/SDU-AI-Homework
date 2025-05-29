from typing import Self, Any
from heapq import heappush, heappop

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
    def __init__(self, state: Any, parent: Self = None, cost: int = 0, depth: int = 0, path: list = None):
        self.state = state
        self.parent_node = parent
        self.cost = cost
        self.depth = depth
        self.path = path or [state]  # Path as a list of states from initial to current

    def expand(self, state_space: StateSpace):
        successors: list[Node] = []
        children = state_space.successor(self.state)
        for child in children:
            step_cost = input_costs.get((self.state, child), 1)
            new_cost = self.cost + step_cost
            new_path = self.path + [child]
            s = Node(child, self, new_cost, self.depth + 1, new_path)
            successors = insert(s, successors)

        return successors

    def display(self) -> None:
        print(self)

    def __repr__(self):
        return f"State: {self.state} - Depth: {self.depth} - Cost: {self.cost}"


def insert(node: Node, queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """
    Returns the queue with the node inserted (the fringe).
    Use the insert_as_first parameter to decide if the node should be inserted at the beginning or the end of the queue.
    """  
    if insert_as_first:
        queue.insert(0, node)  # DFS
    else:
        queue.append(node)     # BFS

    return queue


def insert_all(nodes_to_add: list[Node], queue: list[Node], insert_as_first: bool = True) -> list[Node]:
    """
    Inserts all nodes from the input list, into the queue using the insert function defined in this script.
    """
    for node in nodes_to_add:
        insert(node, queue, insert_as_first)
    return queue


def evaluation_cost(node: Node, strategy: str = "greedy", weight: float = 1.0) -> float:
    """
    Evaluation function depending on search strategy.
    Greedy: f(n) = h(n)
    A*: f(n) = g(n) + h(n)
    Weighted A*: f(n) = g(n) + w*h(n)
    """
    h = heuristics.get(node.state, 0)
    g = node.cost

    if strategy == 'greedy':
        return h
    elif strategy == 'astar':
        return g + h
    elif strategy == 'weighted':
        return g + weight * h
    else:
        return g  # default to uniform-cost if unknown


def remove_best_node(queue: list[Node], strategy: str = "greedy", weight: float = 1.0) -> Node:
    """Removes the best node based on evaluation cost."""
    if not queue:
        return []

    best_index = 0
    best_value = evaluation_cost(queue[0], strategy, weight)

    for i in range(1, len(queue)):
        val = evaluation_cost(queue[i], strategy, weight)
        if val < best_value:
            best_value = val
            best_index = i

    return queue.pop(best_index)


class Searcher:
    def __init__(self, initial_state, goal_state, state_space: StateSpace = None, strategy: str = "greedy", weight: float = 1.0):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_space = state_space
        self.strategy = strategy
        self.weight = weight
        self.nodes_explored = 0

    def tree_search(self, insert_as_first: bool = True) -> list[Node]:
        """
        Search the tree for the goal state
        and return the path from the initial state to the goal state.
        """
        fringe: list[Node] = []
        initial_node = Node(self.initial_state, cost=0, depth=0, path=[self.initial_state])
        fringe = insert(initial_node, fringe)
        explored_states = set()

        while fringe:
            node = remove_best_node(fringe, self.strategy, self.weight)
            self.nodes_explored += 1

            if node.state in self.goal_state:
                return node

            if node.state not in explored_states:
                explored_states.add(node.state)
                children = node.expand(self.state_space)
                fringe = insert_all(children, fringe, insert_as_first)
                print(f"Fringe: {fringe}")

        return None

    def run(self, insert_as_first: bool = True):
        goal_node = self.tree_search(insert_as_first)
        print("Solution path:")
        if goal_node:
            for state in goal_node.path:
                print(f"State: {state}")
            print('Total cost of path: ' + str(goal_node.cost))
            print('Total nodes explored: ' + str(self.nodes_explored))
        else:
            print("No solution found.")


if __name__ == '__main__':
    # Define the graph structure (state space) as an adjacency list
    # Each key is a node, and its value is a list of child nodes (i.e., successors)
    input_state_space = {
        'A': ['B', 'C', 'D'],
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

    # Define the actual cost of moving from one node to another (i.e., g(n))
    # These values are used in A* and Weighted A* to calculate total cost from start
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

    # Define heuristic values for each node (i.e., h(n))
    # These are estimates of the cost from each node to the goal
    # Used in Greedy Best-First, A*, and Weighted A* search
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
        'K': 0,  # goal
        'L': 0,  # goal
    }

    # Define the goal states — the search should terminate when it reaches either 'K' or 'L'
    goal_state = ['K', 'L']

    print("Greedy-best-first")
    searcher = Searcher('A', goal_state, state_space=StateSpace(input_state_space), strategy="greedy")
    searcher.run(insert_as_first=True)

    print("\nA-star")
    searcher = Searcher('A', goal_state, state_space=StateSpace(input_state_space), strategy="astar")
    searcher.run(insert_as_first=True)

    print("\nWeighted A-star (w=2.0)")
    searcher = Searcher('A', goal_state, state_space=StateSpace(input_state_space), strategy="weighted", weight=2.0)
    searcher.run(insert_as_first=True)