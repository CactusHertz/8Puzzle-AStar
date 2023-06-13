from queue import PriorityQueue
from Node import Node

class Astar:
    def astar(initial_state, hType):
        max_depth = 25
        high_depth = False
        count = 0
        past_nodes = []
        start_node = Node(initial_state, None, 0, hType)

        # Sorts nodes by lowest heuristic 
        frontier = PriorityQueue()
        frontier.put((start_node.f, count, start_node))

        # Search for more children if possible
        while not frontier.empty():
            # Gets the most lowest cost node
            node = frontier.get()
            node = node[2]
            past_nodes.append(node.state)
            if(node.g > max_depth):
                high_depth = True
            if high_depth == True:
                break

            # Finds possible child nodes 
            if node.solution_test():
                return node.find_solution()
            children=node.find_possible_children()
        
            # Checks if node has already been searched through
            for child in children:
                if child.state not in past_nodes:
                    count += 1
                    frontier.put((child.f, count, child))
        return