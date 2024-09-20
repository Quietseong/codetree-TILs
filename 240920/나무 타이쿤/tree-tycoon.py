def Input(): #input 함수
    n, m = map(int, input().split())
    graph = [list(map(int, input().split())) for _ in range(n)]
    movelist = [tuple(map(int, input().split())) for _ in range(m)]

    return n, m, graph, movelist

def moveandgrow(nutrients, move): #이동, 리브로수 성장 함수
    direction = [(0,0), (0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1)]
    diagonal = [(-1,-1),(-1,1),(1,1),(1,-1)]  # 대각선 위치

    for i in range(len(nutrients)): #영양제 이동
        x, y = nutrients[i]
        nx, ny = (x+direction[move[0]][0]*move[1])%n, (y+direction[move[0]][1]*move[1])%n
        nutrients[i] = (nx,ny)
        # 영양제가 있는 리브로수 높이 증가시켜주기
        graph[nx][ny] += 1

    # 대각선 리브로수 있는지 보고 높이 증가시켜주기
    for (nx, ny) in nutrients:
        for d in diagonal:
            gx, gy = nx+d[0], ny+d[1]
            if 0<=gx<n and 0<=gy<n and graph[gx][gy]>0:
                graph[nx][ny] += 1

    return nutrients

def cut(): # 크기가 2 이상인 경우 -2만큼 잘라주고 새 위치 업데이트
    newnutrients = []
    for x in range(n):
        for y in range(n):
            if (x,y) not in nutrients and graph[x][y]>1:
                graph[x][y] -= 2
                newnutrients.append((x,y))
    return newnutrients

def answer():
    # 리브로수 높이 다 합치기

    sum = 0
    for x in range(n):
        for y in range(n):
            sum += graph[x][y]
    print(sum)


n, m, graph, movelist = Input()
nutrients = [(n-2,0),(n-2,1),(n-1,0),(n-1,1)] #nxn 초기 특수영양제 위치(좌하단 구석)

for time in range(m): # m년 동안 moveandgrow와 cut에 따라 바뀌는 영양제 좌표를 업데이트.

    nutrients = moveandgrow(nutrients, movelist[time])
    nutrients = cut()

answer()

len(nutrients)