import argparse             # For Parsing Arguments
import logging              # For Debugging Functions
import heapq                # Heaps for Priority Queue
import copy                 # For Deep Copying
import timeit               # Timing

"""
Node Class
----------
Each nodes represents a series of steps taken to arrive at a certain state,
which is recorded by the parent attribute. This means that there might be
multiple nodes for one given state. However, there are no two nodes with
the same state and the same parent.
"""
class Node: 
    def __init__(self, state, parent):
        """
        Creates a new Node Object

        Args
        ----
        state : array
            An arrangement of the stack of pancakes

        parent: Node object
            Parent of the current node
        """
        self.state = state
        self.parent = parent    # Keeps track of the parent of each node
        self.backward_cost = 0
    

    def total_cost(self):
        """
        Calculates the total cost of a flip, which is the sum of the
        heuristic function (forward cost) and the number of pancakes that
        have been flipped (backward cost)
        
        Returns
        -------
        The total cost of a flip
        """
        return self.heuristic() + self.backward_cost
    

    def heuristic(self):
        """
        The heuristic function is defined by the number of stack positions
        for which the pancake at that position is not of adjacent size (+/-
        1) to the pancake below (specified in "Landmark Heuristics for the
        Pancake Problem" by Malte Helmert.) Here, we also take the plate
        into consideration because we want to make sure that the stack
        goes from largest to smallest, starting from the plate.

        Returns
        -------
        h_gap: integer
            The heuristic of the current state
        """
        h_gap = 0
        prev_pancake = self.state[0]
        for pancake in self.state[1:]:
            if abs(pancake - prev_pancake) != 1:
                h_gap += 1
            prev_pancake = pancake
        return h_gap
    

    def flip(self, flip_depth):
        """
        Flip a stack of pancakes at a given flip_depth. 

        Args
        ----
        flip_depth: integer
            The number of pancakes that will be flipped
        """
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

"""
PriorityQueue Class
-------------------
Python has a Queue library that contains a priority queue, but I'm not
using it here because it doesn't has certain functions that check whether
if an element is already in the queue, or replace an element in the
queue. Both of these functions are needed to implement A*.
"""
class PriorityQueue():
    def __init__(self):
        """
        Creates a heap, which is represented by a Python list
        """
        self.heap = []
    

    def put(self, node):
        """
        To put a node onto the priority queue, push onto the heap. The
        order of the priority queue is determined by the total cost
        determined in the Node class (the smaller the higher priority). If
        two nodes have the same total cost, then the node that was first
        introduced has higher priority.

        Args
        ---
        node: Node object
        """
        heapq.heappush(self.heap, node)
        logging.debug("Priority Queue now contains: "), logging.debug(self.heap)
    
    
    def get(self):
        """
        To get the node with the least cost, pop from the heap.

        Returns
        -------
        top: Node object
            Returns the top element of the min heap
        """
        top = heapq.heappop(self.heap);
        return top
    
    
    def has(self, state):
        """
        Loop through the heap to see if an existing state is already in a
        node in the the priority queue. If this is the case, then return
        true. Otherwise, return false.

        Args
        ----
        state: array
            The state for which we are checking whether if it already
            exists in the heap

        Returns
        -------
        boolean
            True if the state is already in the heap, false otherwise
        """
        for node in self.heap:
            if node[2].state == state:
                return True
        return False
    
    
    def replace(self, new_node):
        """
        If a new node is lower in cost than an existing node in the priority
        queue, then replace the old node with the new node.

        Args
        ----
        new_node: Node object
            The new node that would replace one already in the priority
            queue should it have a lower total_cost
        """
        for node in self.heap:
            if node[2].state == new_node[2].state:
                if new_node[2].total_cost() < node[2].total_cost():
                    self.heap[self.heap.index(node)] = new_node
    
    
    def empty(self):
        """
        Returns
        -------
        boolean
            returns True if the priority queue is empty, False otherwise
        """
        return len(self.heap) == 0


class astar():
    def __init__(self, initial_state):
        self.length = len(initial_state)
        self.visited = []      # Keeps track of the states that have been visited
        self.order_added = 0   # Keeps track of the order in which a given node is added
        self.frontier = PriorityQueue()  # The frontier is a priority queue
        
        # First, put the start in the priority queue
        self.root = Node(initial_state, None) # The root no parents
        self.frontier.put((self.root.total_cost(), self.order_added, self.root))
        self.order_added += 1


    def run(self):
        while True:
            # If our frontier is empty and we haven't yet encountered a goal
            # state, that means there is no solution
            if self.frontier.empty():
                return False
            
            # Pop the priority queue to choose the node with the least cost
            curr_node = self.frontier.get()[2]

            # Add the state to the list of states that have been visited
            self.visited.append(curr_node.state)

            # If the heuristic function returns 0, then we are at the goal
            if curr_node.heuristic() == 0:
                return curr_node
            
            # We add every possible node that the current node can reach to
            # the frontier. Each children represents what the stack would
            # look like with each possible flip. We cannot have a flip
            # depth of 1, because that's pointless. We cannot have a flip
            # of depth length, since the last element is the plate itself. 
            for flip_depth in range(2, self.length):
                child = copy.deepcopy(curr_node)    # Make a deep copy
                child.flip(flip_depth)
                child.parent = curr_node
                
                # If the child contains a state that has not been visit, and
                # the frontier does not already have the child's state, then
                # add the child to the frontier
                if (child.state not in self.visited) and (not self.frontier.has(child.state)):
                    # Each node is added to the priority queue as a tuple that
                    # contains the child's total cost (first priority), the
                    # order in which it was added (second priority), and the
                    # child itself.
                    self.frontier.put((child.total_cost(), self.order_added, child))
                    self.order_added += 1
                
                # If the frontier has the child's state but the child has a
                # lower cost to get to that state, replace the existing node in
                # the frontier with the child
                elif self.frontier.has(child.state):
                    self.frontier.replace((child.total_cost(), self.order_added, child))
                    self.order_added += 1
            
            # Print out debugging info only if the heap is not empty
            if not self.frontier.empty():
                logging.debug("Top of the heap is "),
                logging.debug(self.frontier.heap[0][2].state)

           
def main():
    """
    Parse through command line arguments, calls astar(), and print out steps
    to the solution if one is found
    """
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
    AStar = astar(args.stack)
    solution = AStar.run()
    
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