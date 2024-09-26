L, N, Q = map(int, input().split())
graph = [[2]*(L+2)]+ [[2] + list(map(int, input().split())) + [2] for _ in range(L)] + [[2]*(L+2)]
#0: 빈칸, 1: 함정, 2: 벽
#방향 좌표, 상 우 하 좌
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]
#겹침: q추가, q에서 하나씩빼서 순차적 처리-> 모든기사 겹침체크
#이동대상 mv set() 추가
# 기사 dict = {1: [r,c,h,w,k]} ,2:....}
knight = {}

# 초기 체력 저장 후, init_k = [0, 5, ..] 비교
init_k = [0]*(N+1)
for i in range(1, N+1):
    r, c, h, w, k = map(int, input().split())
    knight[i] = [r, c, h, w, k]
    init_k[i] = k #초기 체력 저장

# 함수화 벽을 만나면 return
def mv_knight(start, dr): #start를 밀고 연쇄처리
    q =[] #밀어버릴 대상
    mv_set = set() #이동한 기사번호 저장
    damage = [0]*(N+1) #각 유닛별 대미지 누적

    q.append(start)
    mv_set.add(start)

    while q:
        current_num = q.pop(0)
        r, c, h, w, k = knight[current_num]
        #벽이 아닌 경우, 명령받은 방향으로 진행, 겹치는 다른 조각이면 q에 삽입
        ni, nj = r+di[dr], c+dj[dr]
        for i in range(ni, ni+h):
            for j in range(nj, nj+w):
                if graph[i][j]==2: #벽인 경우 밀기 불가능
                    return
                #함정 처리
                if graph[i][j]==1: #함정이면, 대미지 누적
                    damage[current_num]+=1
        #벽, 함정 통과했다면 기사 여부 체크. 겹치는 다른 기사 있으면 큐에 추가
        for idx in knight:
            if idx in mv_set: continue #이미 움직일 대상이면 체크 필요 없음
            ti, tj, th, tw, tk = knight[idx]

            #겹치는 경우
            if ni<=ti+th-1 and ni+h-1>=ti and tj<=nj+w-1 and nj<=tj+tw-1:
                q.append(idx)
                mv_set.add(idx)
    # 명령 받은 기사는 데미지 입지 않는 조건
    damage[start]=0

    # 대미지 처리, 체력보다 대미지가 이상이면 삭제, 이동처리
    for idx in mv_set:
        r, c, h, w, k = knight[idx]

        if k<=damage[idx]: #체력보다 대미지가 큰 경우
            knight.pop(idx) #기사 삭제
        else:
            ni, nj = r + di[dr], c + dj[dr]
            knight[idx]=[ni, nj, h, w, k-damage[idx]]

# mv set의 기사들을 dr방향으로 한 칸 이동, v[]표시

for _ in range(Q): #이동
    idx, dr = map(int, input().split())
    if idx in knight:
        mv_knight(idx, dr) #명령받은 기사 -> 벽이 없을때 연쇄적으로 밀기

# 대미지 처리, 리스트 -> 일정 대미지 이상이면(체력) 기사 삭제
ans = 0
for idx in knight:
    ans+=init_k[idx]-knight[idx][4] #체력 차이
print(ans)