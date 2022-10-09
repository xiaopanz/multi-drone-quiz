import time
import math
from result import *


def esdf(M, N, obstacle_list):
    """
    :param M: Row number
    :param N: Column number
    :param obstacle_list: Obstacle list
    :return: An array. The value of each cell means the closest distance to the obstacle
    """
    # Create the distance grid with inf distance as initial value
    distance_grid = [[999 for _ in range(N)] for _ in range(M)]

    # perform row scanning, firstly from left to right then from right to left
    for i in range(M):
        for j in range(1, N):
            if [i, j] in obstacle_list:
                distance_grid[i][j] = 0
            else:
                distance_grid[i][j] = distance_grid[i][j - 1] + 1
    for i in range(M):
        for j in range(N - 2, -1, -1):
            if [i, j] in obstacle_list:
                distance_grid[i][j] = 0
            else:
                distance_grid[i][j] = min(distance_grid[i][j], distance_grid[i][j + 1] + 1)

    # store the squared distance in order to save calculation when scanning columns
    for i in range(M):
        for j in range(N):
            distance_grid[i][j] = distance_grid[i][j] ** 2

    # perform first-pass column scanning with a stack, each stack item contains a pair of values,
    # representing respectively a row number y, and the maximum row which that row influences
    for j in range(N):
        start = 0
        for i in range(M):
            if distance_grid[i][j] < 999:
                stack = [[i, i]]
                start = i
                break
        for i in range(start, M):
            if distance_grid[i][j] > 999:
                continue
            influ = i + (distance_grid[i][j] - distance_grid[stack[-1][0]][j] - np.square(i - stack[-1][0])) / (2 * (i - stack[-1][0]))
            if influ > M:
                continue
            if influ > stack[-1][1]:
                stack.append([i, influ])
            else:
                stack.pop()
                while len(stack):
                    influ = i + (distance_grid[i][j] - distance_grid[stack[-1][0]][j] - np.square(i - stack[-1][0])) / (2 * (i - stack[-1][0]))

                    if influ > stack[-1][1]:
                        break
                    else:
                        stack.pop()
                stack.append([i, influ])

        # perform second-pass column scanning by using saved stack
        prev = M
        for row, influence in reversed(stack):
            if(math.ceil(influence+0.01) < 0):
                for i in range(0, prev):
                    distance_grid[i][j] = distance_grid[row][j] + np.square(row - i)
                prev = 0
            else:
                for i in range(math.ceil(influence+0.01), prev):
                    if i < M:
                        distance_grid[i][j] = distance_grid[row][j] + np.square(row - i)
                prev = math.ceil(influence+0.01)

        for i in range(0,math.ceil(stack[0][1]+0.01)):
            if i < M:
                distance_grid[i][j] = distance_grid[start][j] + np.square(start - i)


    for i in range(M):
        for j in range(N):
            distance_grid[i][j] = np.sqrt(distance_grid[i][j])
    return distance_grid

if __name__ == '__main__':
    st = time.time()
    for _ in range(int(2e4)):
        assert np.array_equal(esdf(M=3, N=3, obstacle_list=[[0, 1], [2, 2]]), res_1)
        assert np.array_equal(esdf(M=4, N=5, obstacle_list=[[0, 1], [2, 2], [3, 1]]), res_2)
    et = time.time()
    print(et - st)

