# The Pancake Problem

An A* search algorithm that reports the steps needed to arrange a stack of
pancakes from the largest on the bottom up to the smallest on top, using a
spatula that can be inserted at any point in the stack and flip all
pancakes above it. 

## Running the Script

Run `python ./pancake.py` to run the script on a default stack of pancakes
in the order [4,5,1,3,2,6]. Here, **the largest number represents the plate**
(you can't have a plate in between pancakes). The smallest pancake has the
number 1, and the largest pancake has a number one less than the plate
number. 

Run `python ./pancake.py` followed by **a list of integers, separated by a space** 
to customize input. Note that `pancake.py` will halt with an error if
the plate (the largest number) is not at the bottom (to the right), or if
values other than integers are provided. For example:
* `3 4 2 5 1 6` is a valid input.
* `5 3 4 6` is a valid input.
* `6` is a valid input.
* `3 4 2 6 5 1` is *not* a valid input.
* `3.0 4 2 5 1 6` is *not* a valid input.

Use `-h` or `--help` to view command line options. 

## Debug Mode

To print out the status of the heap each time the pancake.py is run, as
well as the results of each flip, use the flags `-v` or `--verbose`.


## Structure
The A* search uses a priority queue that stores a list of potential nodes
to be visited (to be clear, a node represents a path to a state. This means
that there can be multiple nodes for a given state). Each node is added to
the priority queue as a tuple that contains the its total cost (first
priority), the order in which it was added (second priority), and the
node itself. The order of the priority queue is first determined by the
total cost. If two nodes have the same total cost, then the node that was
first introduced has higher priority.

The priority queue is constructed using a python heap.

## Cost Functions
The heuristic function is defined by the number of stack positions for
which the pancake at that position is not of adjacent size (+/- 1) to the
pancake below. Here, we also take the plate into consideration because we
want to make sure that the stack goes from largest to smallest, starting
from the plate.

The backward cost is represented by the total number of pancakes that had
to be flipped to reach a given node. 

The total cost is a sum of the heuristic function (forward cost) and the
number of pancakes that have been flipped (backward cost).

When we encounter a node that has a lower cost than a node that already
exists in the priority queue with the same state, we replace the existing
node with the new one. 

## Uniform-Cost Search Variation
To run the UCS version of the pancake problem, follow the same instructions
as those provided above, except using the script `pancake_ucs.py`. 

The performance of the A* version is about 1.5x of the UCS version (~25 s
vs. 38 s on a stack of 7 pancakes). This is a good sign that the heuristic
in the A* algorithm is helping with improving search.

## Future Improvements
Future improvements would focus on the efficiency of the A* algorithm. The
time complexity of the current algorithm seems to grow exponentially: it
took 0.02-0.08 s to sort a stack of 5, 0.1 - 0.5 s to sort a stack of 6, 8
\- 25 s to sort a stack of 7, and ~500 s to sort a stack of 8. The way in
which the algorithm is implemented can definitely be improved, such as
combining the `has` and the `replace` methods in the priority queue class
since they are being run in duplicate. It would also be good to experiment with
different variations of the backward cost.


## References
* https://stackoverflow.com/questions/18181818/python-priority-queue-checking-to-see-if-item-exists-without-looping
* Python documentation pages

## Author
Jiayi (Frank) Ma