import sys
sys.stdin = open('input.txt')

def on_every_second(speed, result, temp):
    # 커맨드가 0인 경우 (유지)
    if temp[0] == 0:
        new_speed = speed
        new_result = result + speed
    # 가속
    elif temp[0] == 1:
        new_speed = speed + temp[1]
        new_result = result + new_speed
    # 감속
    elif temp[0] == 2:
        new_speed = max(speed - temp[1], 0)  # 0 이하로 떨어질 수는 없음
        new_result = result + new_speed
    
    return new_speed, new_result




tc = int(input())

for case in range(1, tc+1):
    N = int(input())  # N of commands == 시간 범위
    speed = 0 # 계속 바뀔 현재 상태의 속도
    result = 0 # 최종 누적 거리
    
    for command_num in range(N):
        # 커맨드가 0 일시에는 1개의 값만 들어오므로 일단 리스트로 받는다.
        temp = list(map(int, input().split()))
        # 각 커맨드 처리
        speed, result = on_every_second(speed, result, temp)
        
    print(f'#{case} {result}')