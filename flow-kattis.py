class Player:    
    def __init__(self, id: int):
        self.edges   = {}
        self.id      = id
        self.flow_in = 0

    def add_edge(self, node, edge):
        self.edges[node] = edge

    def change_flow(self,amount):
        self.flow_in = amount
 
class Edge:
    def __init__(self, start: int, end: int, capacity: int):
        self.start    = start
        self.end      = end
        self.ab_residual  = capacity
        self.ba_residual  = 0

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

edges   = [] # Collection of edges
players = [] # Collection of nodes

def main():
    num_players = parse()

    path = find_path()
    while path:
        augment(path)
        path = find_path()

    # Count how many shots have been fired.
    shots = 0
    for edge in edges:
        if edge.start == 0 or edge.end == num_players*2+1: # If looking at source or sink, ignore
            continue
        if edge.ba_residual == 0: # A shots been fired, increment counter
            shots += 1
    
    if shots != num_players: # If all players haven't shot, print impossible
        print("Impossible")
    else:
        for player in range(1,num_players+1):
            for edge in players[player].edges.values():
                if edge.start == 0:         # If edge starts in source, ignore
                    continue
                if edge.ab_residual == 0:   # If there's been fired a shot from a to b, print b
                    print(edge.end-num_players)    

def parse():
    num_players, lines = input().split()
    num_players, lines = int(num_players), int(lines)

    # Add all player nodes (player and player-prime) plus source and sink
    players.append(Player(0))
    for player in range(1, num_players * 2 + 1):        
        players.append(Player(player))
    sink = Player(num_players*2+1)
    players.append(sink)

    # Add edge between source and players
    for player in range(1, num_players + 1):
        edge = Edge(0, player, 1)
        players[0].add_edge(player,edge)
        players[player].add_edge(0,edge)
        edges.append(edge)

    # Add edge between players and player-prime
    for _ in range(lines):
        shooter,target = input().split(" ")
        shooter,target = ((int(shooter)),(int(target)))

        edge    = Edge(target, num_players + shooter, 1) 
        edgeDup = Edge(shooter, num_players + target, 1) 

        edges.append(edge)
        edges.append(edgeDup)

        players[shooter].add_edge(num_players + target,edgeDup)
        players[target].add_edge(num_players + shooter,edge)

        players[num_players + target].add_edge(shooter,edgeDup)
        players[num_players + shooter].add_edge(target,edge)

    # Add edge between player-prime and sink
    for player in range(num_players + 1, sink.id):
        edge = Edge(player, sink.id, 1)
        edges.append(edge)
        players[player].add_edge(sink.id, edge)
        players[sink.id].add_edge(player, edge)

    return num_players # Returning amount of players for use in printing logic


def augment(used_nodes):
    flow = 1
    old_node = None
    for node in used_nodes:
        if old_node == None:
            old_node = node
            continue

        edge = old_node.edges[node.id]

        old_ab_residual = edge.get_residual(old_node.id)
        old_ba_residual = edge.get_residual(node.id)

        edge.set_residual(old_node.id,old_ab_residual-flow)
        edge.set_residual(node.id,old_ba_residual+flow)

        old_node = node
    
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
            p = DFS(players[key], end, discovered, path + [current])
            if p: 
                return p
    return []
# https://stackoverflow.com/questions/7375020/depth-first-graph-search-that-returns-path-to-goal
    
main()
