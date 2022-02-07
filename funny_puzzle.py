import heapq
import numpy as np


def calc_succ(state):
    ret = []
    zero_pos = find_0_pos(state)
    zero_x = zero_pos[0]
    zero_y = zero_pos[1]
    poss_pos = legit_ops(zero_pos)
    for posi in poss_pos:
        x = posi[0]
        y = posi[1]
        toret = np.array(state).reshape((3, 3))
        toret[x][y], toret[zero_x][zero_y] = toret[zero_x][zero_y], toret[x][y]
        toret = toret.reshape(9)
        toIns = toret.tolist()
        ret.append(toIns)
    return sorted(ret)


def print_succ(state):
    items = calc_succ(state)
    for item in items:
        print(item, " h=", calc_h(item), sep="")


def solve(state):
    max_len = 0
    pq = []
    heapq.heappush(pq, (calc_h(state), state, 0, -1))
    poped = []
    to_pop = heapq.heappop(pq)
    poped.append(to_pop)
    while(to_pop[1] != [1, 2, 3, 4, 5, 6, 7, 8, 0]):
        for item in calc_succ(to_pop[1]):
            repeated = 0
            for pd in poped:
                if item == pd[1]:
                    repeated = 1
                    break
            if repeated == 0:
                heapq.heappush(pq, (to_pop[2]+1+calc_h(item), item,
                                    to_pop[2]+1, calc_h(item), to_pop))
        max_len = max_len if max_len > len(pq) else len(pq)
        to_pop = heapq.heappop(pq)
        poped.append(to_pop)
        # print("G:", to_pop[2], "H:", to_pop[3])
        # print(np.array(to_pop[1]).reshape((3, 3)))
    dest = poped[-1]
    step = []
    while dest[-1] != -1:
        step.append(dest[1])
        dest = dest[-1]
    step.append(state)
    index = len(step) - 1
    for i in range(index + 1):
        print(step[index - i], " h=",
              calc_h(step[index - i]), " moves: ", i, sep="")
    # print("Max queue length: ", max_len)


def num_to_2d(num):
    num -= 1
    x = int(num / 3)
    y = num % 3
    return (x, y)


def calc_h(state):
    h = 0
    two_d = np.array(state).reshape((3, 3))
    for i in state:
        if i == 0:
            continue
        h += abs(np.where(two_d == i)[0][0] - num_to_2d(i)[0])
        h += abs(np.where(two_d == i)[1][0] - num_to_2d(i)[1])
    return h


def find_0_pos(state):
    state = np.array(state)
    state = state.reshape((3, 3))
    zero_x = np.where(state == 0)[0][0]
    zero_y = np.where(state == 0)[1][0]
    return([zero_x, zero_y])


def legit_ops(loc):
    if loc == [0, 0]:
        return ([0, 1], [1, 0])
    if loc == [0, 2]:
        return ([0, 1], [1, 2])
    if loc == [2, 0]:
        return ([2, 1], [1, 0])
    if loc == [2, 2]:
        return ([2, 1], [1, 2])

    if loc == [0, 1]:
        return ([0, 0], [0, 2], [1, 1])
    if loc == [1, 0]:
        return ([0, 0], [2, 0], [1, 1])
    if loc == [1, 2]:
        return ([0, 2], [2, 2], [1, 1])
    if loc == [2, 1]:
        return ([2, 0], [2, 2], [1, 1])

    if loc == [1, 1]:
        return([0, 1], [1, 0], [1, 2], [2, 1])
