import sys
from trace import Trace 

blosum_file= open(r"BLOSUM62.txt", "r")
input_file= open(r"HbB_FASTAs-in.txt","r")
# input_file= open(r"Toy_FASTAs-in.txt","r")

name = ""
val = ""
pairList = []

for line in input_file.readlines():
    if line.startswith('>'):
        pairList.append((name,val))
        name = line.split()[0][1:] # Should be name
        val = ""
    else:
        val += line.strip("\n")

pairList.append((name,val)) # We remove the empty set from the first time we enter if statement and add the last pair
pairList = pairList[1:]

lines = [x.strip() for x in blosum_file.readlines() if not x.startswith("#")]
#Cooler way to do it  => lines = filter(lambda x : not x.startswith("#"), sys.stdin.readlines())

aplhabet = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', 'B', 'Z', 'X']
# lines = [['A',1,3,6,3,8,9,3,6,8,3,6,4,5,6,7,3,5,4,6,5,4,3,4],['B',1,3,6,3,8,9,3,6,8,3,6,4,5,6,7,3,5,4,6,5,4,3,6]]

blosum = {}
for line in lines:
    line = line.replace("  "," ")
    letter = line[0]
    line = line.split()
    for x in range(len(aplhabet)):
        blosum[((letter,aplhabet[x]))] = line[x+1]

# Gap penalty
delta = -4 

def sequenceCalculator(s_1: str, s_2: str): 
    n = len(s_1)
    m = len(s_2)
    # Initialise the memoization array
    # MIGHT NEED TO SWAP m AND n HERE, DON'T KNOW -_-
    M, Trace = initialiseMemoizationArrays(n+1, m+1)

    # These steps are matched to the order of the "recursions" on the line defining the "temp" array
    steps = [(1, 1), (1, 0), (0, 1)]
    for i in range(1,n+1):
        for j in range(1,m+1):
            # The alpha for the matching of each char
            match_score = int(blosum[(s_1[i-1], s_2[j-1])])
            # Wrap the different options in an array
            temp = [match_score + M[i-1][j-1], delta + M[i-1][j], delta + M[i][j-1]]
            # This is to avoid making a lot of different if statements
            highest = temp.index(max(temp))
            M[i][j] = temp[highest]
            Trace[i][j] = steps[highest]
    return M[n][m], Trace

def produceMatchStringsFromTrace(TraceArr, s_1: str, s_2: str):
    n = len(s_1)
    m = len(s_2)
    res_1 = ""
    res_2 = ""
    counter_1 = n
    counter_2 = m
    # Continue until we are in the final corner of the trace array
    # Again might be some n/m confusion here, let's just try
    while(counter_1 > 0 and counter_2 > 0):
        (a, b) = TraceArr[counter_1][counter_2]
        if (a, b) == (1, 0):
            res_1 = s_1[counter_1-1] + res_1
            res_2 = '-'+res_2
            counter_1 -= 1
        elif (a, b) == (0, 1):
            res_2 = s_2[counter_2-1] + res_2
            res_1 = '-'+res_1
            counter_2 -= 1
        # Case (1, 1)
        else:
            res_1 = s_1[counter_1-1] + res_1
            res_2 = s_2[counter_2-1] + res_2
            counter_1 -= 1
            counter_2 -= 1
    
    return (res_1, res_2)

def initialiseMemoizationArrays(n: int, m: int):
    temp = [ [0]*m for _ in range(n) ]
    s = [ [(0, 0)] * m for _ in range(n) ]
    for i in range(n):
        temp[i][0] = delta*i
    for j in range(m):
        temp[0][j] = delta*j
    return temp, s

def matchPairs(pairList):
    length = len(pairList)
    for i in range(length):
        for j in range(i+1,length):
            (name1, s1)    = pairList[i]
            (name2, s2)    = pairList[j]
            (score, trace) = sequenceCalculator(s1,s2)
            (res1,  res2)  = produceMatchStringsFromTrace(trace,s1,s2)
            print(name1 + "--" + name2 + ": " + str(score))
            print(res1)
            print(res2)

matchPairs(pairList)