import heapq
import copy
import random
import time

# 8-puzzle problem using A* algorithm with misplaced tiles and total length heuristics

# Define a class for nodes in the search tree
class Node:
    def __init__(self, state, parent,g, f, h):
        self.state = state
        self.parent = parent
        self.g = g
        self.f = f
        self.h = h
    
    # Comparing f values of two nodes to sort them in open_list when using heapq push
    def __lt__(self, other):
        return self.f < other.f
        
# Function to calculate the heuristic for misplaced tiles
def misplaced_heuristic(board, target):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != target[i][j]:
                count += 1
    return count

# Function to calculate the heuristic for total distance of misplaced tiles
def total_length(current, target):
    
    total_distance = 0

    for i in range(len(current)):
        for j in range(len(current)):
            wanted = current[i][j]
            if wanted != 0:
                # Find the position of the current tile in the target board
                for k in range(len(target)):
                    for l in range(len(target)):
                        if wanted == target[k][l]:
                            # Calculate the distance between the current tile and the target tile
                            total_distance += abs(i - k) + abs(j - l)
    
    return total_distance

# Function to get neighbors
def get_neighbors(board):
    neighbors = []
    empty_row, empty_col = find_empty_space(board)
    # RIGHT LEFT DOWN UP
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for d_row, d_col in moves:
        # New position of the empty space
        new_row, new_col = empty_row + d_row, empty_col + d_col
        # Check if the new position is in the board
        if 0 <= new_row < len(board) and 0 <= new_col < len(board):
            new_board = copy.deepcopy(board)
            # Swap the empty space with the tile
            new_board[empty_row][empty_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[empty_row][empty_col]
            neighbors.append(new_board)

    return neighbors

# Function to find empty space on the board
def find_empty_space(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return i, j

# Function to get the path from the initial state to the final state
def get_path(node):
    path = []
    while node.parent is not None: 
        path.append(node.state)
        node = node.parent
    path.append(node.state)
    path.reverse()
    return path

# Function to implement A* algorithm to solve the 8-puzzle problem
def a_star(initial_state, final_state, heuristic):
    open_list = []  # Contains the nodes that are to be visited
    closed_list = set()  # Contains unique states only
    
    if heuristic == "total":
        node = Node(initial_state, None,0, 0, total_length(initial_state, final_state))
    else:
        node = Node(initial_state, None,0, 0, misplaced_heuristic(initial_state, final_state))

    node.f = node.h + node.g 
    # Add the initial state to the open list
    heapq.heappush(open_list, node)

    while open_list:
                
        # Removes the first element from the open list and removes it
        current_node = heapq.heappop(open_list)

        # Check if the current node is the goal state
        if current_node.h == 0:
            path = get_path(current_node)
            return path

        # Get possible moves
        possible_neighbors = get_neighbors(current_node.state)  

        # Add the current state to the closed list
        closed_list.add(tuple(map(tuple, current_node.state)))

        # Create nodes for each possible move
        for neighbor in possible_neighbors:
            
            # Check if the state is in the closed list
            if tuple(map(tuple, neighbor)) not in closed_list:
                
                if heuristic == "total":
                    child_node = Node(neighbor, current_node, current_node.g + 1, 0, total_length(neighbor, final_state))
                else:
                    child_node = Node(neighbor, current_node, current_node.g + 1, 0, misplaced_heuristic(neighbor, final_state))

                child_node.f = child_node.g + child_node.h

                heapq.heappush(open_list, child_node)

            # If the state is in the closed list check open list
            else:
                for node in open_list:
                    # If the state already exists
                    if node.state == neighbor:
                        if node.f > current_node.f:
                            node.g = current_node.g + 1
                            node.f = node.g + node.h
                            node.parent = current_node                
                            
    return None

# Function to print the board
def print_board(board):
    for row in board:
        print(row)

def is_solvable(state):
    state_list = [int(tile) for row in state for tile in row if tile != 0]
    num_of_inversions = 0

    for i in range(len(state_list)):
        for j in range(i + 1, len(state_list)):
            if state_list[i] > state_list[j]:
                num_of_inversions += 1

    return num_of_inversions % 2 == 0

def generate_matrix():
    numbers = [0,1,2,3,4,5,6,7,8]
    matrix = [[0,0,0],[0,0,0],[0,0,0]]

    for i in range(3):
        for j in range(3):
            random_number = random.choice(numbers)
            matrix[i][j] = random_number
            numbers.remove(random_number)

    return matrix

def main():
    print("1-4 single test cases\n5 for 10 random test cases\n6 to exit")
    choice = input("Choose number of input 1-5 to exit enter 6:\n")

    if choice == "1":
        initial_state = [
            [1, 2, 3, ],
            [4, 5, 6, ],
            [7, 8, 0  ]
        ]

        final_state = [
            [1, 2, 3, ],
            [0, 4, 5, ],
            [7, 8, 6  ]
        ]
    elif choice == "2":
        initial_state = [
            [1, 2, 3, ],
            [4, 5, 6, ],
            [7, 0, 8  ]
        ]

        final_state = [
            [1, 2, 3, ],
            [4, 5, 0, ],
            [7, 8, 6 ]
        ]
    elif choice == "3":
        initial_state = [
            [2, 3, 0, ],
            [1, 5, 6, ],
            [4, 7, 8  ]
        ]

        final_state = [
            [1, 2, 3, ],
            [4, 5, 6, ],
            [7, 8, 0  ]
        ]
    elif choice == "4":
        initial_state = [
            [1, 2, 3, ],
            [4, 5, 0, ],
            [6, 7, 8  ]
        ]

        final_state = [
            [1, 2, 3, ],
            [0, 5, 8, ],
            [6, 7, 4  ]
        ]

    elif choice == "5":

        initial_state = []
        final_state = [] 

        for _ in range(10):
            temp = generate_matrix()

            while is_solvable(temp) == False:
                temp = generate_matrix()

            initial_state.append(temp)

            temp = generate_matrix()
            while is_solvable(temp) == False:
               temp = generate_matrix()

            final_state.append(temp)
        
    elif choice == "6":
        exit()

    # Menu to choose the heuristic
    heuristic = input("Enter the heuristic you want to use \n1 for Misplaced tiles\n2 for Total length\nEnter your choice:\n ")
    heuristic = "1"
    if heuristic == "1":
        heuristic = "misplaced"
    elif heuristic == "2":
        heuristic = "total"
    else:
        print("Invalid choice")
        exit()
    
    if choice == "5":
        print("Misplaced tiles")
        # Output the reversed path from the initial state to the final state
        for i in range(10):
            start = time.time()
            path = a_star(initial_state[i], final_state[i], "misplaced")
            end = time.time()
            print_board(initial_state[i])
            print()
            for board in path:
                print_board(board) 
                print()
            print_board(final_state[i])
            print("Time taken: ", round(end - start, 4), "s" )
        
        i = 0
        print("Manhattan distance")
        for i in range(10):
            start = time.time()
            path = a_star(initial_state[i], final_state[i], "total")
            end = time.time()
            print_board(initial_state[i])
            print()
            for board in path:
                print_board(board) 
                print()
            print_board(final_state[i])
            print("Time taken: ", round(end - start, 4), "s" )

    else:
        start = time.time()
        path = a_star(initial_state, final_state, heuristic)
        end = time.time()
        print("Time taken: ", round(end - start, 4), "s" )

    # Print the path
    for board in path:
        print_board(board) 
        print()
    
if __name__ == "__main__":
    while True:
        main()