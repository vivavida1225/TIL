import sys
sys.stdin = open('input.txt')

def square(n ,m):
    if m == 1:
        return n
    return n * square(n, m-1)

tc = 10

for case in range(1, 11):
    cs = int(input())
    n, m = map(int, input().split())
    
    result = square(n ,m)
        
    print(f'#{case} {result}')