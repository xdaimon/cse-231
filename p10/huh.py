
def pos_for_index(x):
    i_x = x // 8
    j_x = x % 8
    if j_x in [0, 7, 6]:
        x = 0
    if j_x in [1, 5]:
        x = 1
    if j_x in [2, 3, 4]:
        x = 2
    if j_x in [0, 1, 2]:
        y = 2
    if j_x in [7, 3]:
        y = 1
    if j_x in [4, 5, 6]:
        y = 0
    x = 'abcdefg'[i_x:7-i_x:3-i_x][x]
    y = '1234567'[i_x:7-i_x:3-i_x][y]
    return x+y

N = 8*3
adjacency = [[0]*N for n in range(N)]
for x in range(N):
    i_x = x // 8
    j_x = x % 8
    for y in range(N):
        if y == x:
            continue
        i_y = y // 8
        j_y = y % 8
        if (i_x == i_y) and (abs(x-y) == 1 or abs(x-y) == 7):
            adjacency[x][y] = 1
            adjacency[y][x] = 1
        if (abs(i_x - i_y) == 1) and (j_x == j_y) and (j_x % 2 == 1):
            adjacency[x][y] = 1
            adjacency[y][x] = 1

ADJACENCY = dict()
for x in range(N):
    for y in range(N):
        if adjacency[x][y]:
            try:
                ADJACENCY[pos_for_index(x)].append(pos_for_index(y))
            except:
                ADJACENCY[pos_for_index(x)] = [pos_for_index(y)]

def is_mill(x1, x2, x3):
    is_possible_mill = False
    i_x1 = x1//8
    i_x2 = x2//8
    i_x3 = x3//8
    j_x1 = x1%8
    j_x2 = x2%8
    j_x3 = x3%8
    if (i_x1 == i_x2 == i_x3):
        parity_sum = sum([xn % 2 for xn in [x1, x2, x3]])
        if parity_sum == 1:
            j_xn = [j_x1, j_x2, j_x3]
            if (max(j_xn) - 2 == min(j_xn)):
                is_possible_mill = True
            if (max(j_xn) + min(j_xn) == 7) and (sum(j_xn) == 6+7):
                is_possible_mill = True
    if (j_x1 % 2 == 1) and (i_x1 != i_x2 != i_x3) and (j_x1 == j_x2 == j_x3):
        is_possible_mill = True
    return is_possible_mill

mills = set()
for x1 in range(N):
    # this should be simplified, need permutations
    row = adjacency[x1]
    points = []
    if sum(row) == 2:
        x2 = row.index(1)
        x3 = row.index(1, x2+1)
        if is_mill(x1, x2, x3):
            points.append([x1, x2, x3])
    elif sum(row) == 3:
        x2 = row.index(1)
        x3 = row.index(1, x2+1)
        x4 = row.index(1, x3+1)
        if is_mill(x1, x2, x3):
            points.append([x1, x2, x3])
        if is_mill(x1, x3, x4):
            points.append([x1, x3, x4])
        if is_mill(x1, x2, x4):
            points.append([x1, x2, x4])
    elif sum(row) == 4:
        x2 = row.index(1)
        x3 = row.index(1, x2+1)
        x4 = row.index(1, x3+1)
        x5 = row.index(1, x4+1)
        if is_mill(x1, x2, x3):
            points.append([x1, x2, x3])
        if is_mill(x1, x3, x4):
            points.append([x1, x3, x4])
        if is_mill(x1, x2, x4):
            points.append([x1, x2, x4])
        if is_mill(x1, x3, x5):
            points.append([x1, x3, x5])
        if is_mill(x1, x2, x5):
            points.append([x1, x2, x5])
        if is_mill(x1, x4, x5):
            points.append([x1, x4, x5])

    for i in range(len(points)):
        points[i].sort()
        mills.add(tuple(points[i]))

MILLS = []
for points in mills:
    lis = list(map(pos_for_index, points))
    lis.sort()
    MILLS.append(lis)
MILLS.sort()

import NMM
is_eq = True
for k,v in ADJACENCY.items():
    if k in NMM.Board.ADJACENCY:
        if sorted(v) != sorted(NMM.Board.ADJACENCY[k]):
            is_eq = False
    else:
        is_eq = False
    if not is_eq:
        break

print('ADJACENCY ok:')
print(is_eq)
is_eq = sorted(NMM.Board.MILLS) == MILLS
print('MILLS ok:')
print(is_eq)
