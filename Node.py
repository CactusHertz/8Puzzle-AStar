class Node:

    goal_state = [[0,1,2],[3,4,5],[6,7,8]]
    h = None
    f = None
    nodes = 0 

    # Sets all the values of the node 
    def __init__(self, state, parent, g, hType):
        self.state = state
        self.parent = parent
        if parent: 
            self.g = parent.g + g 
        else: 
            self.g = g 
        self.hType = hType

        if hType == "1":
            self.h1()
        elif hType == "2":
            self.h2()

        self.f = self.h + self.g
        Node.nodes += 1
    
    # Counts the number of misplaced tiles 
    def h1(self):
        self.h = 0
        for r in range(3):
            for c in range(3):
                if self.goal_state[r][c] != self.state[r][c]:
                    self.h += 1

    # Calculates the sum of the distances of the state from the goal state 
    def h2(self):
        self.h = 0
        for r in range(3):
            for c in range(3):
                x = self.goal_state[r][c]
                init_r = None
                init_c = None

                for r2 in range(3):
                    for c2 in range(3):
                        if self.state[r2][c2] == x:
                            init_r = r2
                            init_c = r2
                self.h += (abs(init_r - r) + abs(init_c - c))
            
    
    # Finds the possible children for a given state
    def find_possible_children(self):
        possible_children = []

        # If a tile can move to a position create a child node with that swapped position
        for r in range(3):
            for c in range(3):
                if(self.state[r][c] == 0):
                    if c - 1 >= 0:
                        possible_children.append(Node(self.swap_values(r, c, r, c-1), self, 1, self.hType))
                    if c + 1 <= 2:
                        possible_children.append(Node(self.swap_values(r, c, r, c+1), self, 1, self.hType))
                    if r - 1 >= 0:
                        possible_children.append(Node(self.swap_values(r, c, r-1, c), self, 1, self.hType))
                    if r + 1 <= 2:
                        possible_children.append(Node(self.swap_values(r, c, r+1, c), self, 1, self.hType)) 
        return possible_children
        
    # Helper function used to get a state with a swapped value
    def swap_values(self, r:int, c:int, r2:int, c2:int):
        arr = [[0,0,0],[0,0,0],[0,0,0]]
        for rc in range(3):
            for cc in range(3):
                arr[rc][cc] = self.state[rc][cc]
        temp = arr[r][c]
        arr[r][c] = arr[r2][c2]
        arr[r2][c2] = temp
        return arr

    # Checks if the current state is equal to the goal state
    def solution_test(self):
        if self.goal_state == self.state:
            return True
        return False

    # Creates a list of the path from the node to the root
    def find_solution(self):
        solution = []
        solution.append(self.state)
        path = self
        # As long as a node has a parent add the node
        while path.parent != None:
            path = path.parent
            solution.append(path.state)
        solution = solution[:-1]
        # since the list starts from goal node, the list is reversed. 
        solution.reverse()
        return solution
    
        

        
