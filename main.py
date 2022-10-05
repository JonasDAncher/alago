def main():
    var = []
    n = int(input()) # Number of cases
    var = [int(v) for v in input().split()]
    var.sort(reverse=True)
    sum = 0
    for m in range(2,n,3):
        sum += var[m]
    print(sum)

main()