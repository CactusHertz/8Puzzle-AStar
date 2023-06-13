from time import time 
from random import shuffle
from Node import Node
from os import path
from Astar import Astar
import sys

def start_menu():
    while True:
        print("Select:")
        print("[1] Single Test Puzzle")
        print("[2] Multi Test Puzzle")
        print("[3] Exit")
        start_input = input()

        if start_input == "1":
            print()
            return [single_input_menu()]

        elif start_input == "2":
            print()
            return multi_input_menu()

        elif start_input == "3":
            print("Goodbye")
            quit()

def single_input_menu():
    while True:
        print("Select:")
        print("[1] Random")
        print("[2] Manual")

        initialState = None
        input_type = int(input())
        if input_type == 1:
            initialState = random_state()
            print()
            return initialState
        elif input_type == 2:
            initialState = manual_state()
            print()
            return initialState

# Ask the user for the type of mutiple state input they want 

def multi_input_menu():
    while True:
        print("Select:")
        print("[1] Random")
        print("[2] File")
        print("[3] 100 Cases")

        input_type = int(input())

        # Random asks for the number of states and fills and array with that many states
        if input_type == 1:
            while True: 
                try:
                    num_states = int(input("Number of states: "))
                except ValueError:
                    print("You must enter a valid number.")
                else: 
                    if num_states > 0:
                        break
                    else:
                        print("The number must be greater than 0")
            random_states = []
            for x in range(num_states):
                random_states.append(random_state())
            print()
            return random_states

        # Checks if the file exist and then reads it. 
        elif input_type == 2:
            while True:
                file_name = input("Enter file name: ")
                if path.exists(file_name):
                    print()
                    return read_file(file_name)
                else:
                    print("The file does not exist")
        elif input_type == 3: 
            test_100(h_menu())
            quit()

# Asks the user for which h function the want to use
def h_menu():
    while True:
        print("Select H Function")
        print("[1] H1")
        print("[2] H2")
        
        h_input = input()
        if h_input == "1":
            return h_input
        elif h_input == "2":
            return h_input

# Returns a state with a random order
# Will check if the state can be solved before returning it 
def random_state():
    while True:
        arr = [[0,0,0],[0,0,0],[0,0,0]]
        possible_num = [0,1,2,3,4,5,6,7,8]
        shuffle(possible_num)
        index = 0
        for r in range(3):
            for c in range(3):
                arr[r][c] = possible_num[index]
                index += 1
        if check_state(arr):
            return arr

# Asks the user to manually input a state one number at a time. 
def manual_state():
    print("Enter Intial State")
    arr = [[0,0,0],[0,0,0],[0,0,0]]
    index = 1
    for r in range(3):
        for c in range(3):
            while True:
                try:
                    arr[r][c] = int(input("Enter a number for spot " + str(index) + ": "))
                except ValueError:
                    print("You must enter a valid number.")
                else: 
                    if arr[r][c] >= 0 and arr[r][c] <= 8:
                        break
                    else:
                        print("The number must be between 0 and 8")
            index += 1
    return arr

# Pulls states from a file based on the format of the txt provided for this project. 
def read_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()

    file_states = []
    current_array = []
    for i in range(len(lines)):
        if "/" in lines[i]:
            continue
        else:      
            current_array.append([int(x) for x in lines[i].split()])
        if len(current_array) == 3:
            file_states.append(current_array)
            current_array = []
    return file_states

# counts the number of inversions in a state
def check_state(state):
    test = [1,2,3,4,5,6,7,8]
    init_state = [] 
    number_of_inversions = 0
    # converts the 2d sate to a single list for easier comparisions 
    for r in range(3):
        for c in range(3):
            if (state[r][c] != 0):
                init_state.append(state[r][c])

    for num in test:
        start_search = False
        for num2 in init_state:
            #starts search after the instance of the number is found
            if num == num2:
                start_search = True
            if start_search == True:
                if num2 < num:
                    number_of_inversions += 1
    if number_of_inversions % 2 == 0:
        return True
    else:
        return False
        
# prints 2d array in a cleaner format
def print_state(state):
    indent = 0
    for r in range(3):
        for c in range(3):
            print(str(state[r][c]), end=" ")
            indent += 1
            if indent % 3 == 0:
                print()
    print()

# Runs a batch of 100 random cases for analysis
def test_100(h_type):
    print("Progress: ")
    successful_tests = []
    valid_tests = 0 
    while valid_tests < 100:
        initial = random_state()
        if check_state(initial):
            Node.nodes = 0
            start_time = time()
            solution = Astar.astar(initial, h_type)
            end_time = time()

            if solution:
                d = len(solution)
                search_cost = Node.nodes
                total_time = end_time - start_time
                successful_tests.append([d, total_time, search_cost])
                valid_tests +=1
                print("|",end="")
    average_time = {}
    average_cost = {}
    d_frequency = {}

    for test in successful_tests:
        d = test[0]
        if d not in average_time:
            average_time[d] = test[1]
            average_cost[d] = test[2]
            d_frequency[d] = 1
        else:
            average_time[d] = (average_time[d] + test[1]) / 2
            average_cost[d] = (average_cost[d] + test[2]) / 2
            d_frequency[d] += 1
    for d, value in average_time.items():
        print(f"D_value: {d}, Average time: {value}, Average cost: {average_cost[d]}, Frequency: {d_frequency[d]}")
 


def main():
    # Gets the initial values for the program 
    intial_states = start_menu()
    h_value = h_menu()

    average_cost = 0
    average_time = 0
    total_solutions = 0

    for state in intial_states:
        
        print("Initial State: ")
        print_state(state)

        if check_state(state):
            Node.nodes = 0
            start_time = time()
            solution = Astar.astar(state, h_value)
            end_time = time()

            if solution:
                print("Solution Found")
                step_count = 1
                for step in solution:
                    print("Step: " + str(step_count))
                    print_state(step)
                    step_count +=1

                print("Search Cost: ", Node.nodes)
                print("Time: ", end_time - start_time)
                print("Depth: ", step_count - 1)
        
                average_cost += Node.nodes
                average_time += end_time - start_time
                total_solutions += 1
            else:
                print("No solution found")
        else:
            print("No solution")
        print("___________________")
        print()
    if(total_solutions > 0):
        print("Average cost", average_cost / total_solutions)
        print("Average time", average_time / total_solutions)
    else:
        print("No solutions found")



f_file = open("output.txt", "w")
original_stdout = sys.stdout
sys.stdout = f_file

main()

sys.stdout = original_stdout
f_file.close()




        
