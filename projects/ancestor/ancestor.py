# so this is more or less a BFT and we find the value or "ancestor" with no higher nodes above it

# so first we need to have classes of graphes to impliment so when we start the BFT on the we can track the path and find the end point much like the "destination" assignment from the previous night

# this here is more or less the same as the homework we init the class then we can add the node and the connecting vertices
class Graph:
    def __init__(self):
        self.vertices = {}

    def add_node(self, node):
        self.vertices[node] = set()

    def add_edge(self,v1,v2):
        if v1 not in self.vertices:
            self.add_node(v1)
        if v2 not in self.vertices:
            self.add_node(v2)
        # and since we are techincally going "backwards" we add the vertices the same way
        self.vertices[v2].add(v1)

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self,value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

# so here we do a BFT to get our answer for the longest distance traveled

# more or less we have a starting point and it can have mulitple destinations BUT the longest graph so to speak will have the earliest known ancestor.  which is what we return as the answer for this question BUT FIRST we have to find all KNOWN paths FROM the starting node

# it also states in the read me that if there is a tie then we return the one with the lowest numeric ID so for example "9" will have a tie of "4" and "11" so we return the "4"

def bft(graph, starting_node):
    # so first we start the queue
    q = Queue()
    # then we add the starting node to it, we also add it in as an array
    q.enqueue([starting_node])
    # then we create a "visited" list so we can keep track of the nodes we visited and don't loop forever
    visited = set()
    # then we create an array of "all paths" so we can compair and find the longest one
    all_paths = []
    # so we start by saying if there is ANYTHING in the queue this loop will run
    while q.size() > 0:
        # we first create a variable that will keep track of whatevers in the queue to create our first "path" so to speak
        path = q.dequeue()
        # this weird little thing python does by putting "[-1]" we jump the END of the array automatically don't know why it's magic
        # so we find the last thing on the path and we insert it into this new variable "node" 
        node = path[-1]

        # then we check if the node is not in visited and if it is then we SKIP!!
        if node not in visited:
            # but if it isn't then we add it in so we don't visit it again
            visited.add(node)
            # then we check the length of the graph and if it is greater then 0 we reset the all_paths variable
            if len(graph.vertices[node]) > 0:
                all_paths = []
            # if it IS 0 then we loop through visited queued node
            for new_node in graph.vertices[node]:
                # we copy the path into a new variable
                new_path = list(path)
                # and we APPEND the new_node onto the new_path
                new_path.append(new_node)
                # ALTHOUGH we check to see if the length of the new node on the graph has no other vertices appened to it meaning it's the LOWEST part of the graph 
                # or earliest ancestor for the node
                if len(graph.vertices[new_node]) == 0:
                    # so we are don't we tracked it down and we now append it to the "all_path" variable
                    all_paths.append(new_path)
                else:
                    # if there is then we RE enqueue the new path to start again so to speak
                    # and this will run since the while loop will keep running until the queue is empty
                    q.enqueue(new_path)
    return all_paths

# now that we have ALL the paths from the starting node we now compare and find the longest length between them and return the end of that array of if its a tie we return the lowest value

def earliest_ancestor(ancestors, starting_node):
    # pass
    # so first we start the graph again
    graph = Graph()

    # then we are given the ancestors through the parameter so we pass that in into the graph and we populate it so to speak
    for ancestor in ancestors:
        # here we are adding in the first and second as a set
        graph.add_edge(ancestor[0], ancestor[1])

    # so now we call the function above while passing in the graph we just populated and the starting node
    all_paths = bft(graph, starting_node)

    # so lets TEST it first by find the all paths for this on line 119
    # comment out the bottom as well see that the path given to us is [1,10]
    # print(all_paths)

    # we create the answer now by saying that the answer is the LAST element in the array
    answer = -1 if len(all_paths) == 0 else all_paths[0][-1]

    # so now we see if the all_path is greater then 1 which it shouldn't since only one path should have been found but nonetheless have a backup never hurts
    if len(all_paths) > 1:
        # so if we do have more than one path we have to compare them
        # for every element in the all_path's array
        for i in range(len(all_paths)-1):
            # if "i" which is the first element in the array of "all_paths" we compair it's last element with the answer if it is smaller then we replace it
            if all_paths[i+1][-1] < answer:
                answer = all_paths[i+1][-1]
    # if NOT then we just move on and at the end we return the answer
    return answer

# now the test on test_ancestor.py should pass


# test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

# earliest_ancestor(test_ancestors, 1)
