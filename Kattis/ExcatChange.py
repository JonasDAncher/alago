coins = []
result = []
amountOfCoins = 0

def findBestCombi(i):
    bestPrice   = 99999
    spendCoins  = 99999
    bestCoin    = 99999
    storage     = []

    for m in range(amountOfCoins):
        cur_coin = coins[m]
        if cur_coin >= i:
            if cur_coin < bestPrice:
                spendCoins  = 1
                bestPrice   = cur_coin
                bestCoin    = m
            continue
        
        storage = result[i-cur_coin]
        if cur_coin not in storage[2]:
            continue

        if bestPrice > storage[0]+cur_coin:
            spendCoins  = storage[1]+1
            bestPrice   = storage[0]+cur_coin
            bestCoin    = m
        elif bestPrice == storage[0]+cur_coin and spendCoins > storage[1]+1:
            spendCoins  = storage[1]+1
            bestCoin    = m
    
    if bestCoin == 99999:
        return
    
    if coins[bestCoin] >= i:
        bestPrice       = coins[bestCoin]
        spendCoins      = 1
        remainingCoins  = coins[:]
        remainingCoins.pop(bestCoin)
    else:
        valOfBestCoin = coins[bestCoin]
        storage         = result[i-valOfBestCoin]
        bestPrice       = storage[0]+valOfBestCoin
        spendCoins      = storage[1]+1
        remainingCoins  = storage[2][:]
        remainingCoins.remove(valOfBestCoin)
    
    result.append((bestPrice, spendCoins, remainingCoins))

n = int(input())
for i in range(n):
    price = int(input())
    amountOfCoins = int(input())
    coins = []
    for i in range(amountOfCoins):
        coins.append(int(input()))
  
    result = [(0,0,coins)]          # (Closest price, amount of coins spend, coins available)
    bestCombi = (99999,99999)       # To be updated once a better fit is found
    if price == 0:
        print("0 0")                # Check to see if tests use no price
        continue

    for i in range(1,price+1):      # Skip the first, and go one further
        findBestCombi(i)

        if i >= price:
            bestForI = result[i]    # Avoid looking up many times
            if bestForI[0] < bestCombi[0]:
                bestCombi = bestForI
            elif bestForI[0] == bestCombi[0] and bestForI[1] < bestCombi[1]:
                bestCombi = bestForI

    print(bestCombi[0],bestCombi[1])
