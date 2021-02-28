import copy
import os
grid_size = 3
goal = [[1,2,3], [4,5,6], [7,8,'']]
initial = [[3,1,2], ['',6,5], [8,7,4]]
#initial = [[1,2,3], [4,5,6], [7,'',8]]


class node:
    def __init__ (self, state):
        self.state = state

def print_grid(list_):
    for i in range(grid_size):
        for j in range(grid_size):
            print(f"{list_[i][j]}\t",end = "")
        print("\n")
        
def check_misplaced(node):
    h = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if node.state[i][j] != goal[i][j]:
                h += 1
    return h

def find_space(node):
    for i in range(grid_size):
        for j in range(grid_size):
            if node.state[i][j] == '':
                return i,j

def movement(old_node, move, row, col):
    node = copy.deepcopy(old_node)
    if move == 'U':
        node.state[row][col] = node.state[row-1][col]
        node.state[row-1][col] = ''
    elif move == 'D':
        node.state[row][col] = node.state[row+1][col]
        node.state[row+1][col] = ''
    elif move == 'L':
        node.state[row][col] = node.state[row][col-1]
        node.state[row][col-1] = ''
    elif move == 'R':
        node.state[row][col] = node.state[row][col+1]
        node.state[row][col+1] = ''
    return node

def possible_moves(current):
    moves_set = []
    row, col = find_space(current)
    if col == 0:
        moves_set.append('R')
        if row == 1:
            moves_set.extend(['U','D'])
        elif row == 0:
            moves_set.append('D')
        elif row == 2:
            moves_set.append('U')
    elif col == row and row == 1:
        moves_set.extend(['L','R','U', 'D'])
    elif col == 1 and row == 0:
        moves_set.extend(['L','R','D'])
    elif col == 1 and row == 2:
        moves_set.extend(['L','R','U'])
    elif col == 2:
        moves_set.append('L')
        if row == 1:
            moves_set.extend(['U','D'])
        elif row == 0:
            moves_set.append('D')
        elif row == 2:
            moves_set.append('U')
    return moves_set,row,col

def visited_check(current):
    for n in visited:
        if current.state == n.state and n.f > current.f:
            return True
    return False


def frontier_check(current):
    for n in frontier:
        if n.state == current.state and n.f < current.f:
            return True
    return False

def expand(current): #to expand a node and return all its children
    children = []
    moves_set,row,col = possible_moves(current) #to obtain the moves the empty tile can make
    for move in moves_set: #for each move, we will have a node
        child = movement(current, move, row, col)
        #print(move)
        child.parent = current
        child.h = check_misplaced(child)
        child.g = current.g + 1
        child.f = child.h + child.g
        child.move = move
        #print_grid(child.state)
        if not frontier_check(child):
            children.append(child)
    return children

def display_frontier():
    print("-----------FRONTIER-----------")
    for state in frontier:
        print_grid(state.state)
        print(f"@{state.g} and @{state.h}")

def refresh_frontier(nodes, node):
    for i,n in enumerate(nodes, start = 0):
        if not greater_visited_cost(n):
            frontier.insert(i,n)
    frontier.remove(node)

def get_valid_node():
    loc = 0
    smallest = frontier[loc].f
    for i,n in enumerate(frontier, start = 0):
        if n.f < smallest:
            smallest = n.f
            loc = i
    return frontier[loc]

def greater_visited_cost(state):
    for node in visited:
        if node.state == state.state:
            if state.f > node.f:
                return True
    return False
 
def check_frontier(current):
    for n in frontier:
        if n.state == current.state and current.f > n.f:
            return True
    return False

def form_solution(current):
    solution = []
    while current.parent != None:
        solution.insert(0,current)
        current = current.parent
    return solution
def show_solution(tree):
    for n in tree:
        if n.move:
            print(f"----------{n.move}----------")
        print_grid(n.state)
    
start = node(initial)
start.parent = None
start.h = check_misplaced(start)
start.g = 0
start.f = start.h + start.g
start.move = None
frontier = [start]
visited = []
solved = False
tree = [start]
i = 0


while not solved:
    if not frontier:
        print("Failed")
        break
    else:
        current = get_valid_node()
        if current.state == goal:
            tree.extend(form_solution(current))
            solved = True
            break
        else:
            i += 1
            if not i%1000:
                print("Checkpoint ", i)
            isAlreadyPresent = visited_check(current)#checks if this node is present in visited with less cost
            if not isAlreadyPresent:
                refresh_frontier(expand(current), current)
                visited.append(current)

if solved:
    print("SOLVED!")
    show_solution(tree)
    print(f"The puzzle was solved in {len(tree)-1} move(s)") #-1 because root is not included
else:
    print(":( Unable to solve!")