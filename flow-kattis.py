class Player:    
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
    def __init__(self, start: int, end: int, capacity: int, infinite: int):
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

players = [] # Collection of nodes
edges = [] # Collection of edges

def main():
    parse()
    # print(players)
    # print(edges)
    path = find_path()
    while path:
        augment(path)
        path = find_path()
    
    # print(summarise()) # Comment to remove printing of flow


    min_cut = get_min_cut()
    for id in range(len(min_cut)):
        if min_cut[id].ab_residual == 0:
            print(id)
        # print(id)
    
    # for edge in min_cut: # Comment to remove min-cut printing.
    #     edge.pretty_print()

def summarise():
    sum = 0
    for edge in players[len(players)-1].edges.values():
        sum += edge.ba_residual
    return sum

def parse():
    num_players, lines = input().split()
    num_players, lines = int(num_players), int(lines)

    players.append(Player(0))

    for player in range(1,num_players+1):
        edge = Edge(0, player, 1, True)
        players[0].add_edge(player,edge)

    for player in range(1,num_players*2+1):        
        players.append(Player(player))

    for _ in range(lines):
        shooter,target = input().split(" ")
        shooter,target = ((int(shooter)),(int(target)))
        edge    = Edge(target, num_players+shooter, 10000, False) 
        edgeDup = Edge(shooter, num_players+target, 10000, False) 
        edges.append(edge)
        # players[shooter].add_edge(target,edge)
        players[shooter].add_edge(num_players+target,edgeDup)
        players[target].add_edge(num_players+shooter,edge)


    sink = Player(num_players*2+1)
    players.append(sink)
    for player in range(4,num_players*2+1):
        edge = Edge(player,sink.id, 1, True)
        edges.append(edge)
        players[player].add_edge(sink.id,edge)

def augment(used_nodes):
    flow = 1
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
    source = players[0]
    sink = players[len(players)-1]
    return DFS(source, sink, set(), [])
                
def DFS(current, end, discovered, path):
    discovered.add(current.id)
    if current == end: 
        return path + [current]
    for key, edge in current.edges.items(): 
        if key not in discovered and edge.get_residual(current.id) != 0:
            # print(key)
            p = DFS(players[key], end, discovered, path + [current])
            if p: 
                return p
    return []
# https://stackoverflow.com/questions/7375020/depth-first-graph-search-that-returns-path-to-goal

def get_min_cut():
    discovered = set()
    source = players[0]
    sink = players[len(players)-1]
    DFS(source, sink, discovered, [])
    min_cut = []
    for edge in edges:
        start = edge.start in discovered
        end = edge.end in discovered
        if start != end:
            min_cut.append(edge)
    return min_cut
    
main()
