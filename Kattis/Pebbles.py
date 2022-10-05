
games = []
n = int(input())
for i in range(0,n):
    games.append(input())
global bestPebbles
bestPebbles = 25
mem = {}

def main():
    for game in games:
        pebbles = game.count("o")
        global bestPebbles
        bestPebbles = pebbles
        OPT(game,0,pebbles)
        print(bestPebbles)
        

def moveRight(gameRight,pos, pebbles):
    if pos > 20 or not gameRight[pos+1] == "o" or not gameRight[pos+2] == "-":
        return 25
    gameRight = gameRight[:pos] + "--o" + gameRight[pos+3:]
    return OPT(gameRight, max(0,pos-2), pebbles-1)
    
def moveLeft(gameLeft,pos, pebbles):
    if pos < 2 or not gameLeft[pos-1] == "o" or not gameLeft[pos-2] == "-":
        return 25
    gameLeft = gameLeft[:pos-2] + "o--" + gameLeft[pos+1:]
    return OPT(gameLeft, max(0,pos-3), pebbles-1)

def OPT(game,pos,pebbles):
    if pos >= 23:
        global bestPebbles
        if pebbles < bestPebbles:
            bestPebbles = pebbles
        return pebbles
    if game[pos] == "-": 
        OPT(game,pos+1,pebbles)
    else:
        if game in mem: 
            return mem[game] or 25
        right = moveRight(game, pos, pebbles)
        left = moveLeft(game, pos, pebbles)
        # Below is some of the worst comparison code I've ever seen. Please excuse it. I'm trying to compare something that can be NoneType, and it's a bitch. I'm new to python, ok.
        smallest = (right or 25) if (right or 25) < (left or 25) else (left or 25)
        noMove = OPT(game,pos+1,pebbles)
        actaullysmallest = (smallest or 25) if (smallest or 25) <(noMove or 25) else (noMove or 25)
        mem[game] = actaullysmallest
        return actaullysmallest

main()