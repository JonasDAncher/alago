class Node:    
    def __init__(self, id: int):
        self.edges   = {}
        self.id      = id
        self.flow_in = 0

    def add_edge(self, node, edge):
        self.edges[node] = edge

    def change_flow(self,amount):
        self.flow_in = amount

    def __repr__(self):
        return '\nnode id = {0}, edges: \n{1}'.format(self.id, self.edges)
 
class Edge:
    def __init__(self, start: int, end: int, capacity: int, infinite: bool):
        self.infinite = infinite
        self.start    = start
        self.end      = end
        self.ab_residual  = capacity
        self.ba_residual  = capacity

    def get_residual(self, origin: int):
        return self.ab_residual if origin == self.start else self.ba_residual
    
    def pretty_print(self):
        if self.ab_residual > 0:
            print(self.end, self.start, int(self.ab_residual / 2))
        else:
            print(self.start, self.end, int(self.ba_residual / 2))

    def set_residual(self, origin:int, amount: int):
        if origin == self.start:
            self.ab_residual = amount
        else:
            self.ba_residual = amount 

    def __repr__(self):
        return 'Edge start: {0} End: {1} capacity ab: {2} capacity ba: {3}\n'.format(self.start, self.end, self.ab_residual, self.ba_residual)

nodes = [] # Collection of nodes
edges = [] # Collection of edges

def main():
    parse()
    path = find_path()
    while path:
        augment(path)
        path = find_path()
    
    # print(summarise()) # Comment to remove printing of flow

    min_cut = get_min_cut()
    
    for edge in min_cut: # Comment to remove min-cut printing.
        edge.pretty_print()

def summarise():
    sum = 0
    for edge in nodes[len(nodes)-1].edges.values():
        sum += edge.ba_residual
    return sum

def parse():
    input_file= open(r"./data/rail.txt","r")

    number_of_vertices = int(input_file.readline())
    for node in range(number_of_vertices):
        input_file.readline()
        nodes.append(Node(node))

    number_of_edges = int(input_file.readline())
    for _ in range(number_of_edges):
        a,b,c = input_file.readline().strip().split(" ")
        a,b,c = (int(a),int(b),int(c))
        edge = Edge(a,b,c,c == -1) 
        edges.append(edge)
        nodes[a].add_edge(b,edge)
        nodes[b].add_edge(a,edge)

def augment(used_nodes):
    flow = find_bottleneck_flow(used_nodes)
    old_node = None
    for node in used_nodes:
        if old_node == None:
            old_node = node
            continue

        edge = old_node.edges[node.id]

        if old_node.edges[node.id].infinite:
            old_node = node
            if edge.ba_residual == -1:
                edge.ba_residual = flow
            else:
                edge.ba_residual = edge.ba_residual + flow 
            continue
        
        old_ab_residual = edge.get_residual(old_node.id)
        old_ba_residual = edge.get_residual(node.id)

        edge.set_residual(old_node.id,old_ab_residual-flow)
        edge.set_residual(node.id,old_ba_residual+flow)

        old_node = node

def find_bottleneck_flow(used_nodes):
    flow = float("inf")
    old_node = None
    for node in used_nodes:
        if old_node == None or old_node.edges[node.id].infinite:
            old_node = node
            continue
        edge = old_node.edges[node.id]
        newflow = edge.get_residual(old_node.id)
        if newflow < flow:
            flow = newflow
        old_node = node

    return flow
    
def find_path():
    source = nodes[0]
    sink = nodes[len(nodes)-1]
    return DFS(source, sink, set(), [])
                
def DFS(current, end, discovered, path):
    discovered.add(current.id)
    if current == end: 
        return path + [current]
    for key, edge in current.edges.items(): 
        if key not in discovered and edge.get_residual(current.id) != 0:
            p = DFS(nodes[key], end, discovered, path + [current])
            if p: 
                return p
    return []
# https://stackoverflow.com/questions/7375020/depth-first-graph-search-that-returns-path-to-goal

def get_min_cut():
    discovered = set()
    source = nodes[0]
    sink = nodes[len(nodes)-1]
    DFS(source, sink, discovered, [])
    min_cut = []
    for edge in edges:
        start = edge.start in discovered
        end = edge.end in discovered
        if start != end:
            min_cut.append(edge)
    return min_cut
    
main()
