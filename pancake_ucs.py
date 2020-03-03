import argparse             # For Parsing Arguments
import logging              # For Debugging Functions
import heapq                # Heaps for Priority Queue
import copy                 # For Deep Copying
import timeit               # Timing


# Each nodes represents a series of steps taken to arrive at a certain
# state. This means that there might be multiple nodes for one given state
class Node: 
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent    # Keeps track of the parent of each node
        self.backward_cost = 0
    
    # The total cost is now only the backward cost
    def total_cost(self):
        return self.backward_cost
    
    # This is the original heuristic function used in A*, now used as a
    # goal test.
    def goal_test(self):
        h_gap = 0
        prev_pancake = self.state[0]
        for pancake in self.state[1:]:
            if abs(pancake - prev_pancake) != 1:
                h_gap += 1
            prev_pancake = pancake
        return h_gap
    
    # This class method allows us to flip a stack of pancakes at a given
    # flip_depth. 
    def flip(self, flip_depth):
        # We save this information so that the steps of flipping can be
        # printed out with the solution
        self.flip_depth = flip_depth
        logging.debug("Before flipping: "), logging.debug(self.state)

        # We swap the first and the last pancake in the range of the flip
        # depth. In the case where there is an odd number of pancakes, the
        # middle pancake would just be swapped with itself
        for x in range(int(flip_depth / 2)):
            temp = self.state[x]
            self.state[x] = self.state[flip_depth - x - 1]
            self.state[flip_depth - x - 1] = temp

        # The backward cost is how many pancakes have been flipped (i.e.
        # flip_depth)
        self.backward_cost += flip_depth
        logging.debug("After flipping: "), logging.debug(self.state)


# Python has a Queue library that contains a priority queue, but I'm not
# using it here because it doesn't has certain functions that check whether
# if an element is already in the queue, or replace an element in the
# queue. Both of these functions are needed to implement A*
class PriorityQueue():
    def __init__(self):
        self.heap = [] # The Heap is represented by a list
    
    # To put a node onto the priority queue, push onto the heap. The order
    # of the priority queue is determined by the total cost determined in
    # the Node class. If two nodes have the same total cost, then the node
    # that was first introduced has higher priority.
    def put(self, node):
        heapq.heappush(self.heap, node)
        logging.debug("Priority Queue now contains: "), logging.debug(self.heap)
    
    # To get the node with the least cost, pop from the heap.
    def get(self):
        return heapq.heappop(self.heap)
    
    # Loop through the heap to see if an existing state is already in a
    # node in the the priority queue. If this is the case, then return
    # true. Otherwise, return false.
    def has(self, state):
        for node in self.heap:
            if node[2].state == state:
                return True
        return False
    
    # If a new node is lower in cost than an existing node in the priority
    # queue, then replace the old node with the new node
    def replace(self, new_node):
        for node in self.heap:
            if node[2].state == new_node[2].state:
                if new_node[2].total_cost() < node[2].total_cost():
                    self.heap[self.heap.index(node)] = new_node
    
    # Return True if heap is empty
    def empty(self):
        return len(self.heap) == 0


def astar(initial_state):
    length = len(initial_state)
    visited = []      # Keeps track of the states that have been visited
    order_added = 1   # Keeps track of the order in which a given node is added
    frontier = PriorityQueue()  # The frontier is a priority queue
    
    # First, put the start in the priority queue
    root = Node(initial_state, None) # The root no parents
    frontier.put((root.total_cost(), order_added, root))
    order_added += 1


    while True:
        # If our frontier is empty and we haven't yet encountered a goal
        # state, that means there is no solution
        if frontier.empty():
            return False
        
        # Pop the priority queue to choose the node with the least cost
        curr_node = frontier.get()[2]

        # Add the state to the list of states that have been visited
        visited.append(curr_node.state)

        # If the goal test (i.e. the heuristic function used in A*) returns
        # 0, then we are at the goal 
        if curr_node.goal_test() == 0:
            return curr_node
        
        # We add every possible node that the current node can reach to the
        # frontier. Each children represents what the stack would look like
        # with each possible flip. We cannot have a flip depth of 1,
        # because that's pointless. We cannot have a flip of depth length, since
        # the last element is the plate itself. 
        for flip_depth in range(2, length):
            child = copy.deepcopy(curr_node)    # Make a deep copy
            child.flip(flip_depth)
            child.parent = curr_node
            
            # If the child contains a state that has not been visit, and
            # the frontier does not already have the child's state, then
            # add the child to the frontier
            if (child.state not in visited) and (not frontier.has(child.state)):
                # Each node is added to the priority queue as a tuple that
                # contains the child's total cost (first priority), the
                # order in which it was added (second priority), and the
                # child itself.
                frontier.put((child.total_cost(), order_added, child))
                order_added += 1
            
            # If the frontier has the child's state but the child has a
            # lower cost to get to that state, replace the existing node in
            # the frontier with the child
            elif frontier.has(child.state):
                frontier.replace((child.total_cost(), order_added, child))
                order_added += 1
        
        # Print out debugging info only if the heap is not empty
        if not frontier.empty():
            logging.debug("Top of the heap is "),
            logging.debug(frontier.heap[0][2].state)
                     

def main():
    # Setup parser and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", 
                        help="Increase verbosity", 
                        action="store_true")
    parser.add_argument(dest = "stack", # By specifying the destination, we    
                                        # avoid the need of having to have the  
                                        # numbers be preceded by a flag
                        nargs = "*",
                        type = int,
                        default = [4,5,1,3,2,6],
                        help = "Define a stack of pancakes to be sorted. Default: %(default)s")    
    args = parser.parse_args()
    
    # Setup Debugging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # The largest number represents the plate and must be at the bottom.
    for pancake in args.stack:
        if pancake > args.stack[len(args.stack) - 1]:
            print("The plate (the largest number) must be at the bottom")
            exit()

    # Start timer
    start = timeit.default_timer()

    # Run a star on the default or user provided stack of pancakes.
    # Solution here is only the final node and does not contain any
    # information about the steps. However, this node contains information
    # about its parent and we can trace back.
    solution = astar(args.stack)
    
    if solution == False:
        print("No solution found")
    else:
        solution_steps = []
        while solution != None: # Stop when we reach the start
            solution_steps.append(solution)
            solution = solution.parent
        
        # If there is only one state in our solution, then the user input
        # is already the solution
        if len(solution_steps) == 1:
            print("Your stack of pancakes is already sorted!")
            exit()
        
        # Reverse the steps because it's backwards
        solution_steps.reverse()
        
        # Finally, print the steps to get to the solution
        print("To sort the stack", solution_steps[0].state, "do the following:")
        for step in range(1, len(solution_steps)):
            print("Step", step, ": Flip the top", 
                  solution_steps[step].flip_depth,
                  "pancakes to get", solution_steps[step].state)
    
    # Stop the timer and print execution time
    stop = timeit.default_timer()
    print("Execution Time:", round(stop - start, 2), "s")  


if __name__ == '__main__':
    main()