import sys
sys.stdin = open('input.txt')

tc = int(input())

for case in range(1, tc+1):
    N, K = map(int, input().split())  # 물건의 개수, 가방의 최대 부피

    items = [0] * N
    for idx in range(N):
        items[idx] = tuple(map(int, input().split()))  # 해당 물건의 부피, 가치
    
    dp = [0] * (K+1) # 각 부피별 최적 가치들을 저장
    
    for v, c in items:
        # K부터 v까지 역순으로 채운다
        # 정방향으로 순회 시 똑같은 물건을 2번 넣는 오류 발생 가능
        # 역방향으로 순회 시에는 이전 턴까지의 물건들로만 이루어진 최적값을 덮어쓸 수 있음
        for w in range(K, v - 1, -1):
            dp[w] = max(dp[w], dp[w - v] + c)
    
    # print(dp)
    result = dp[-1]
        
    print(f'#{case} {result}')