import sys
sys.stdin = open('input.txt')

tc = int(input())

for case in range(1, tc+1):
    N, K = map(int, input().split())  # 물건의 개수, 가방의 최대 부피

    items = [0] * (N+1)
    for idx in range(N):
        # 1번부터 N번 인덱스까지 저장 및 사용
        items[idx+1] = tuple(map(int, input().split()))  # 해당 물건의 부피, 가치
    # print(items)
    
    dp = [[0] * (K+1) for _ in range(N+1)]
    
    # 1번 인덱스부터 순회
    for idx, (weight, score) in enumerate(items[1:]):
        # print(idx+1, weight, score)
        for bag_weight in range(K+1): # 현재 보고있는 물건보다 적은 무게 후보들은 이전걸 따라감
            if bag_weight < weight: 
                dp[idx+1][bag_weight] = dp[idx][bag_weight]
            else:
                dp[idx+1][bag_weight] = max(dp[idx][bag_weight], dp[idx][bag_weight-weight] + score)
        # print(dp[idx+1])
    
    result = dp[-1][-1]
        
    print(f'#{case} {result}')