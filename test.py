import heapq                # Heaps for Priority Queue

def main():
    heap = []
    node1 = Node(4, 10)
    node2 = Node(5, 2)
    node3 = Node(4, 12)
    node4 = Node(5, 5)
    heapq.heappush(heap, node1)
    heapq.heappush(heap, node2)
    heapq.heappush(heap, node3)
    heapq.heappush(heap, node4)

    print(heap)
    
    for i in range(4):
        node = heapq.heappop(heap)
        print("(" + str(node.i1) + "," + str(node.i2) + ")")


class Node():
    def __init__(self, i1, i2):
        self.i1 = i1
        self.i2 = i2
    
    def __lt__(self, other):
        if self.i1 != other.i1:
            return self.i1 < other.i1
        else:
            return self.i2 < other.i2

main()