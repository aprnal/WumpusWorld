# 2 Gold 3 Wumpus 4 Pit
import sys
import random

class Member:
    def __init__(self):
        self.num = 0
        self.stench = 0
        self.breeze = 0
        self.glitter = 0

    # 값 반환용
    def getN(self):
        return self.num

    def getS(self):
        return self.stench

    def getB(self):
        return self.breeze

    def getG(self):
        return self.glitter

    # 값 설정용
    def setN(self, num):
        self.num = num

    def setS(self, stench):
        self.stench = stench

    def setB(self, breeze):
        self.breeze = breeze

    def setG(self, glitter):
        self.glitter = glitter


# 동 1, 서 2, 남 3, 북 4
global Head, count
Head = 1  # 현재 agent가 향하고 있는 방향(동)
count = 3


def GameStart():
    Map = [[Member() for _ in range(4)] for _ in range(4)]
    Visited = [[0 for _ in range(4)] for _ in range(4)]  # DFS 탐색시 사용되는 Visited(갔던 곳 안 가도록 하려고)
    Svisited = [[0 for _ in range(4)] for _ in range(4)]  # 화살 쏘기용 list wumpus
    stack = []

    Gold, Wumpus, Pit = random.sample(range(0, 15), 3)  # G, W, P 랜덤생성

    # 랜덤생성한 위치에 부여
    # Wumpus 위치 생성 0-14
    Wy = Wumpus // 4
    Wx = Wumpus % 4
    if Wy == 3:
        Wx += 1
    Map[Wy][Wx].setN(3)  # member에 있는 setN이 3이면 wumpus 존재
    Map[Wy][Wx].setS(1)  # stench

    # Wumpus 주위에(상하좌우) Stench 설정
    for dy, dx in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        newY = Wy + dy
        newX = Wx + dx
        if 0 <= newX < 4 and 0 <= newY < 4:
            Map[newY][newX].setS(1)

    # Pit 위치  생성
    Py = Pit // 4
    Px = Pit % 4
    if Py == 3:
        Px += 1
    Map[Py][Px].setN(4)
    Map[Py][Px].setB(1)  # breeze

    for dy, dx in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        newY = Py + dy
        newX = Px + dx
        if 0 <= newX < 4 and 0 <= newY < 4:
            Map[newY][newX].setB(1)

    # Gold 위치 생성
    Gy = Gold // 4
    Gx = Gold % 4
    if Gy == 3:
        Gx += 1
    Map[Gy][Gx].setN(2)
    Map[Gy][Gx].setG(1)  # glitter

    # 각 위치에 부여 후 반환
    return Map, Visited, Svisited, stack

def goFoward(y, x, Visited):
    global Head
    if (Visited[2][0]==1 and Visited[3][1]==1):
        Head = 1
        newY = y
        newX = x+1
        if not (0 <= newX < 4 and 0 <= newY < 4):
            y, x = bump(Map, newY, newX, y, x)
            return goFoward(y, x, Visited)
        return newY, newX

    if Head == 1:  # 동
        newY = y
        newX = x + 1

    elif Head == 2:  # 서
        newY = y
        newX = x - 1

    elif Head == 3:  # 남
        newY = y + 1  # y는 커질수록 내려감 x는 커질수록 오른쪽
        newX = x

    elif Head == 4:  # 북
        newY = y - 1
        newX = x

    if not (0 <= newX < 4 and 0 <= newY < 4):
        y, x = bump(Map, newY, newX, y, x)
        return goFoward(y, x, Visited)

    elif not Visited[newY][newX]:
        Visited[newY][newX] = 1
        return newY, newX

    elif Visited[newY][newX]:
        Head = turn()
        return goFoward(y, x, Visited)

    else:
        return y, x


def arrow(Map, x, y, Visited, Svisited):
    global count, Head
    if count == 0:  # 화살개수 정해짐 0개일땐 못쏨
        print("화살을 다 사용했습니다..")
        return
    elif count == 3 or random.randint(0, 1) == 1:
        # 랜덤 1/2확률로 쏘기 or 화살을 한번도 쏘지 않으면 쏘기
        count -= 1
        if Head == 1:  # 방향설정 (동)
            for n in range(4):
                if n < x:
                    continue
                if Map[y][n].getN() == 3:  # W(3)존재하면 죽이기
                    print("Arrow!!")
                    print("Scream!!!")
                    Map[y][n].setN(0) # N을 0으로 설정
                    Map[y][n].setS(0)
                    if y - 1 >= 0:
                        Map[y - 1][n].setS(0)  # W 주변 S값 0 으로 설정
                    if y + 1 < 4:
                        Map[y + 1][n].setS(0)
                    if n + 1 < 4:
                        Map[y][n + 1].setS(0)
                    if n - 1 >= 0:
                        Map[y][n - 1].setS(0)
                    return

            # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
            print("Arrow!!")

        elif Head == 2:  # 방향설정 (서)
            for n in range(4):
                if n > x:
                    continue
                if Map[y][n].getN() == 3:  # W(3)존재하면 죽이기
                    print("Arrow!!")
                    print("Scream!!!")
                    Map[y][n].setN(0) # N을 0으로 설정
                    Map[y][n].setS(0)
                    if y - 1 >= 0:
                        Map[y - 1][n].setS(0)  # W 주변 S값 0 으로 설정
                    if y + 1 < 4:
                        Map[y + 1][n].setS(0)
                    if n + 1 < 4:
                        Map[y][n + 1].setS(0)
                    if n - 1 >= 0:
                        Map[y][n - 1].setS(0)
                    return

            # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
            print("Arrow!!")

        elif Head == 3:  # 방향설정 (남)
            for n in range(4):
                if n < y:
                    continue
                if Map[n][x].getN() == 3:  # W(3)존재하면 죽이기
                    print("Arrow!!")
                    print("Scream!!!")
                    Map[n][x].setN(0)  # N을 0으로 설정
                    Map[n][x].setS(0)
                    if n - 1 >= 0:
                        Map[n - 1][x].setS(0)  # W 주변 S값 0 으로 설정
                    if n + 1 < 4:
                        Map[n + 1][x].setS(0)
                    if x + 1 < 4:
                        Map[n][x + 1].setS(0)
                    if x - 1 >= 0:
                        Map[n][x - 1].setS(0)
                    return

            # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
            print("Arrow!!")

        else:  # 방향설정 (북)
            for n in range(4):
                if n > y:
                    continue
                if Map[n][x].getN() == 3:  # W(3)존재하면 죽이기
                    print("Arrow!!")
                    print("Scream!!!")
                    Map[n][x].setN(0)  # N을 0으로 설정
                    Map[n][x].setS(0)
                    if n - 1 >= 0:
                        Map[n - 1][x].setS(0)  # W 주변 S값 0 으로 설정
                    if n + 1 < 4:
                        Map[n + 1][x].setS(0)
                    if x + 1 < 4:
                        Map[n][x + 1].setS(0)
                    if x - 1 >= 0:
                        Map[n][x - 1].setS(0)
                    return

            # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
            print("Arrow!!")

    else:
        # 화살 안쏨
        return


# S를 두번이상 만남 ; Svisited에서 그전에 stench 값이 있을 경우 실행
def sureArrow(Map, x, y, i, j, visited, Svisited):  # S를 두번이상 만났다!
    global Head
    if i == x and j == y:  # 대칭구조일 때
        if y > x:  # [y-1][x]에 W 존재가능성 ㅇ
            if Head == 4:  # 방향설정 (북)
                for n in range(4):
                    if n > y:
                        continue
                    if Map[n][x].getN() == 3:  # W존재하면 죽이기
                        print("Arrow!!")
                        print("Scream!!!")
                        Map[n][x].setN(0) # N을 0으로 설정
                        Map[n][x].setS(0)
                        if n - 1 >= 0:
                            Map[n - 1][x].setS(0)  # W 주변 S값 0 으로 설정
                        if n + 1 < 4:
                            Map[n + 1][x].setS(0)
                        if x + 1 < 4:
                            Map[n][x + 1].setS(0)
                        if x - 1 >= 0:
                            Map[n][x - 1].setS(0)
                        return

                # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                print("Arrow!!")

            elif Head == 1:  # 방향설정 (동)
                for n in range(4):
                    if n < x:
                        continue
                    if Map[y][n].getN() == 3:  # W존재하면 죽이기
                        print("Arrow!!")
                        print("\nScream!!!")
                        Map[y][n].setN(0) # N을 0으로 설정
                        Map[y][n].setS(0)
                        if y - 1 >= 0:
                            Map[y - 1][n].setS(0)  # W 주변 S값 0 으로 설정
                        if y + 1 < 4:
                            Map[y + 1][n].setS(0)
                        if n + 1 < 4:
                            Map[y][n + 1].setS(0)
                        if n - 1 >= 0:
                            Map[y][n - 1].setS(0)
                        return

                # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                print("Arrow!!")

        else:  # [y][x-1]에 존재할 때
                if Head == 2:  # 방향설정 (서)
                    for n in range(4):
                        if n > x:
                            continue
                        if Map[y][n].getN() == 3:  # W존재하면 죽이기
                            print("Arrow!!")
                            print("Scream!!!")
                            Map[y][n].setN(0)  # N을 0으로 설정
                            Map[y][n].setS(0)
                            if y - 1 >= 0:
                                Map[y - 1][n].setS(0)  # W 주변 S값 0 으로 설정
                            if y + 1 < 4:
                                Map[y + 1][n].setS(0)
                            if n + 1 < 4:
                                Map[y][n + 1].setS(0)
                            if n - 1 >= 0:
                                Map[y][n - 1].setS(0)
                            return

                    # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                    print("Arrow!!")

                elif Head == 3:  # 방향설정 (남)
                    for n in range(4):
                        if n < y:
                            continue
                        if Map[n][x].getN() == 3:  # W존재하면 죽이기
                            print("Arrow!!")
                            print("Scream!!!")
                            Map[n][x].setN(0)  # N을 0으로 설정
                            Map[n][x].setS(0)
                            if n - 1 >= 0:
                                Map[n - 1][x].setS(0)  # W 주변 S값 0 으로 설정
                            if n + 1 < 4:
                                Map[n + 1][x].setS(0)
                            if x + 1 < 4:
                                Map[n][x + 1].setS(0)
                            if x - 1 >= 0:
                                Map[n][x - 1].setS(0)
                            return

                    # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                    print("Arrow!!")

    else:  # [i][j] #[y][x]
        if (i + 1) == y and (j + 1) == x:
            if Head == 4:  # 방향설정 (북)
                for n in range(4):
                    if n > y:
                        continue
                    if Map[n][x].getN() == 3:  # W존재하면 죽이기
                        print("Arrow!!")
                        print("\nScream!!!")
                        Map[n][x].setN(0) # N을 0으로 설정
                        Map[n][x].setS(0)
                        if n + 1 < 4:
                            Map[n + 1][x].setS(0)
                        if n - 1 >= 0:
                            Map[n - 1][x].setS(0)  # W 주변 S값 0 으로 설정
                        if x + 1 < 4:
                            Map[n][x + 1].setS(0)
                        if x - 1 >= 0:
                            Map[n][x - 1].setS(0)
                        return


                # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                print("Arrow!!")

            elif Head == 2:  # 방향설정 (서)
                for n in range(4):
                    if n > x:
                        continue
                    if Map[y][n].getN() == 3:  # W존재하면 죽이기
                        print("Arrow!!")
                        print("Scream!!!")
                        Map[y][n].setN(0) # N을 0으로 설정
                        Map[y][n].setS(0)
                        if y - 1 >= 0:
                            Map[y - 1][n].setS(0)  # W 주변 S값 0 으로 설정
                        if y + 1 < 4:
                            Map[y + 1][n].setS(0)
                        if n + 1 < 4:
                            Map[y][n + 1].setS(0)
                        if n - 1 >= 0:
                            Map[y][n - 1].setS(0)
                        return

                # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                print("Arrow!!")

        else:
            if Head == 1:  # 방향설정 (동)
                for n in range(4):
                    if n < x:
                        continue
                    if Map[y][n].getN() == 3:  # W존재하면 죽이기
                        print("Arrow!!")
                        print("Scream!!!")
                        Map[y][n].setN(0) # N을 0으로 설정
                        Map[y][n].setS(0)
                        if y - 1 >= 0:
                            Map[y - 1][n].setS(0)  # W 주변 S값 0 으로 설정
                        if y + 1 < 4:
                            Map[y + 1][n].setS(0)
                        if n + 1 < 4:
                            Map[y][n + 1].setS(0)
                        if n - 1 >= 0:
                            Map[y][n - 1].setS(0)
                        return

                # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                print("Arrow!!")

            elif Head == 3:  # 방향설정 (남)
                for n in range(4):
                    if n < y:
                        continue
                    if Map[n][x].getN() == 3:  # W존재하면 죽이기
                        print("Arrow!!")
                        print("Scream!!!")
                        Map[n][x].setN(0) # N을 0으로 설정
                        Map[n][x].setS(0)
                        if n - 1 >= 0:
                            Map[n - 1][x].setS(0)  # W 주변 S값 0 으로 설정
                        if n + 1 > 4:
                            Map[n + 1][x].setS(0)
                        if x + 1 < 4:
                            Map[n][x + 1].setS(0)
                        if x - 1 >= 0:
                            Map[n][x - 1].setS(0)
                        return

                # 화살을 쏜 뒤에 아무일이 일어나지 않을 때 방문한 배열의 정보 출력
                print("Arrow!!")


def turn():  # 방향설정
    print("turn~!")

    if Head == 1:  # 동에서 북
        return 4

    elif Head == 2:  # 서에서 남
        return 3

    elif Head == 3:  # 남에서 동
        return 1

    elif Head == 4:  # 북에서 서
        return 2


# agent 머리 표현하는 함수 (GUI 용)
# 동 1, 서 2, 남 3, 북 4
def printHead():
    if Head == 1:
        return "⇨"
    elif Head == 2:
        return "⇦"
    elif Head == 3:
        return "⇩"
    elif Head == 4:
        return "⇧"


def bump(Map, y, x, prev_y, prev_x):  # agent가 도달한 곳이 맵의 경계를 넘어서면
    global Head

    if not (0 <= x < 4 and 0 <= y < 4):  # 다음 위치가 맵의 범위를 벗어나면
        print("Bump!")
        Head = turn()  # 에이전트의 방향을 바꾸기
        return prev_y, prev_x  # 이전 위치 반환
    else:
        return y, x


def ClimbingDFS(y, x, Visited, stack):
    print("Climbing...")
    while stack:
        y, x = stack.pop()
        print(f"\n경로: ({3-y},{x})")
    print("\nSuccess!!!")


## 실질적인 게임 코드
def DFS(y, x, Map, Visited, Svisited, stack):
    global Head
    Visited[y][x] = 1  # 방문했음 표시
    stack.append((y, x))

    Print_agentMap(Map, Visited, y, x)

    if Map[y][x].getN() == 2:  # 금
        Visited[y][x] = 1
        print("Gold found at ({}, {})!".format(3-y, x))
        print("Grab Gold!!")

        ClimbingDFS(y, x, Visited, stack)

        sys.exit("Game Clear!")

    if Map[y][x].getN() == 3:  # 웜프스
        Svisited[y][x] = 1
        print("Wumpus를 만나 죽음")
        stack.clear()
        Head = 1
        DFS(3, 0, Map, Visited, Svisited, stack)

    if Map[y][x].getN() == 4:  # 구덩이
        Visited[y][x] = 1
        print("Pit를 만나 죽음")
        stack.clear()
        Head = 1
        DFS(3, 0, Map, Visited, Svisited, stack)

    if Map[y][x].getB() == 1:  # 현재 위치에 바람(Breeze)이 불면
        Head = turn()

    # 화살쏘기 S가 있을 경우
    if Map[y][x].getS() == 1:
        for i in range(len(Svisited)):  # 그전에 S값이 존재했는지 찾기
            for j in range(len(Svisited[i])):
                if Svisited[i][j] == 1:
                    sureArrow(Map, x, y, i, j, Visited, Svisited)
                    Svisited[y][x] = 1
                    # 해당 좌표에 Svisited 값 넣기 (S가 존재했다는 것을 알리기위함)
                    # 존재했다면 무조건 근처에 W가 존재
                    break

        arrow(Map, x, y, Visited, Svisited)
        # Svisited에 값이 없으면 그냥 화살 쏘기

    newY, newX = goFoward(y, x, Visited)
    DFS(newY, newX, Map, Visited, Svisited, stack)


# 맵 출력 함수 (확인용)
def print_map(Map):
    for y in range(4):
        for x in range(4):
            member = Map[y][x]
            realY = 3 - y
            print(f"({realY}, {x}) N:{member.getN()} S:{member.getS()} B:{member.getB()} G:{member.getG()}", end=' | ')
        print()


# agent가 방문한 곳 출력
def print_visited(Visited):
    for y in range(4):
        for x in range(4):
            print(f"{Visited[y][x]}", end=' ')
        print()


# 맵 출력 함수 (에이전트용) - 실제 게임 출력용
def Print_agentMap(Map, Visited, ay, ax):
    print("\nagnet Map:")
    for y in range(4):
        for x in range(4):
            if y == ay and x == ax:
                print(f"{printHead()} ", end=' ')
            else:
                print(f"{Visited[y][x]} ", end=' ')
        print()
    realY = 3 - ay
    print(f"({realY}, {ax}) N:{Map[ay][ax].getN()} S:{Map[ay][ax].getS()} B:{Map[ay][ax].getB()} G:{Map[ay][ax].getG()}")


############### 여기서부터 Main

# Game 환경을 위한 맵 설정
Map, Visited, Svisited, stack = GameStart()

# Map 출력
print("\nMap:")
print_map(Map)

# Visited 출력
print("\nVisited:")
print_visited(Visited)

# DFS 실행 - 게임 실행
DFS(3, 0, Map, Visited, Svisited, stack)
