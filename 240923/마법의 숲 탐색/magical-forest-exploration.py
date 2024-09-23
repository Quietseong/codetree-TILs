r, c, k = map(int, input().split()) #6 5 6
unit = [list(map(int, input().split())) for i in range(k)]
arr = [[1]+[0]*c+[1] for _ in range(r+3)]+[[1]*(c+2)] #grid 만들어주기
exit = set()

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def bfs(si, sj):
    q = []
    v = [[0]*(c+2) for _ in range(r+4)] #방문 여부
    max_i = 0 #가장 아래쪽 행

    q.append((si, sj))
    v[si][sj]=1

    while q:
        ci, cj=q.pop(0) #q가 빌때까지 현재 좌표 처리
        max_i = max(max_i, ci)
        # 상하좌우, 미방문, 조건: 같은 값 또는 출구 -> 상대방 골렘(넘버링이 1보다 큰 골렘)
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = ci+di, cj+dj #원점에서 방향좌표만큼 이동
            if v[ni][nj]==0 and (arr[ci][cj]==arr[ni][nj] or ((ci,cj) in exit and arr[ni][nj]>1)):
                #방문 x칸, 현재칸=인접칸이면 같은 골렘, 현위치가 출구이면서 인접칸이 다른 골렘인 경우
                q.append((ni, nj))
                v[ni][nj]=1 #방문 처리

    return max_i-2 #grid 인덱스를 2 추가해놨기 때문에

ans = 0
num = 2 #골렘 넘버링
#골렘 입력 좌표/방향에 따라 남쪽 이동 및 정령 최대좌표 계산

for cj, dr in unit: #중앙좌표, 유닛에서 하나씩 꺼내서 c, dr(출구방향)로
    ci=1 # 초기값 행 1
    while True: #무한루프 -> 탈출
        if arr[ci+1][cj-1]+arr[ci+2][cj]+arr[ci+1][cj+1]==0: #아래로 가는 조건 3개, 모두 0이면 빈칸
            ci+=1 #만족하면 한칸 아래로 내려가기
        elif arr[ci-1][cj-1]+arr[ci][cj-2]+arr[ci+1][cj-1]+arr[ci+1][cj-2]+arr[ci+2][cj-1]==0: #서쪽(왼쪽) 조건 5개, 모두 0이면 빈칸
            ci+=1
            cj-=1
            dr=(dr-1)%4 #왼쪽으로 가면 서->남->동->북->서 이런 순서대로
        elif arr[ci-1][cj+1]+arr[ci][cj+2]+arr[ci+1][cj+1]+arr[ci+1][cj+2]+arr[ci+2][cj+1]==0: #동쪽(오른쪽)으로 가는 조건 5개, 모두 0이면 빈칸
            ci+=1
            cj+=1
            dr=(dr+1)%4 #오른쪽으로 가면 서->북->동->남->서 이런 순서대로
        else:
            break #이동안되면 나가기

    if ci < 4: #범위 밖인 경우 골렘 다 빠지고 새로운 탐색 시작, 값 초기화
        arr=[[1]+[0]*c+[1] for _ in range(r + 3)]+[[1]*(c+2)] # grid 만들어주기
        exit=set()
        num=2

    else: #아니면 남쪽으로. bfs 탐색하면서 max_i찾기
        # 골렘을 2부터 증가하면서 표시(경계선은 1)
        arr[ci+1][cj]=arr[ci-1][cj]=num #골렘 몸체의 세로(행)방향에 num 부여
        arr[ci][cj-1:cj+2]=[num]*3 #골렘 몸체의 가로(열)방향 num 부여
        num+=1 #다음 골렘에 num 1개 추가해서 표시

        exit.add((ci+di[dr], cj+dj[dr])) #출구 표시, 원점에서 위치만큼 이동한 곳이 출구
        ans+=bfs(ci, cj) #정령의 최종 위치(행 번호) 누적

print(ans)
    # bfs탐색(ci,cj 기준으로)-2 
    # 탐색 조건은 같은 값(cicj == ni), 내 출구가 다른 골렘(1보다 큰) ci -> ni,nj>1