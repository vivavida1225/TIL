
# DP 풀이

## 1차원 배열 풀이
```python
dp = [0] * (K+1) # 각 부피별 최적 가치들을 저장

for v, c in items:
    # K부터 v까지 역순으로 채운다
    # 정방향으로 순회 시 똑같은 물건을 2번 넣는 오류 발생 가능
    # 역방향으로 순회 시에는 이전 턴까지의 물건들로만 이루어진 최적값을 덮어쓸 수 있음
    for w in range(K, v - 1, -1):
        dp[w] = max(dp[w], dp[w - v] + c)
```


## 2차원 배열 풀이
```python
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
```