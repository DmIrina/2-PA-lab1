import time
import os
import psutil
from random import randint


# https://i.stack.imgur.com/NQ0Ne.jpg -- check # of solutions

class Solution:
    def __init__(self):
        self.timeout = time.time() + 60 * 30  # 30 minutes from now
        self.dead_ends = 0

    def loop_continues(self) -> bool:
        return time.time() < self.timeout

    # q     - current Queen
    # nq    - new (inserted) Queen
    def bfs(self, queue: [], n: int):
        result = []
        all_states = 1
        iterations = 1
        queue_max_len = 1
        blind_corners = 0

        pid = os.getpid()
        py = psutil.Process(pid)

        while queue:  # until queue is not empty and timer runs
            if not self.loop_continues():
                print("Time out")
                exit(0)

            if py.memory_info().rss > 50000000:
                print("Out of memory")
                print(str(py.memory_info().rss) + " bytes")
                exit(0)

            q_tuple = queue.pop(0)  # queue - take from the top
            children = 0

            nq_col = self.get_nq_col(q_tuple)  # find column for new Queen

            if nq_col == -5:  # all columns are full
                result.append(q_tuple)  # add solution to result
                continue

            for nq_row in range(0, n):  # find rows for new Queen
                nq_no_attack = True
                for q_col in range(0, n):  # N of column with current Queen, solution index
                    q_row = q_tuple[q_col]  # N of row with current Queen
                    iterations = iterations + 1
                    if q_row != -1:  # if there is a queen
                        if self.twoQueensAttack(nq_row, nq_col, q_row, q_col):
                            nq_no_attack = False

                if nq_no_attack:
                    nq_tuple = q_tuple.copy()
                    nq_tuple[nq_col] = nq_row
                    self.get_nq_col(nq_tuple)
                    all_states = all_states + 1

                    if nq_col != -5:  # there are empty columns
                        queue.append(nq_tuple)
                        children = children + 1

                        if queue_max_len < len(queue):
                            queue_max_len = len(queue)

                if children == 0:
                    blind_corners = blind_corners + 1
        print("blind_corners = " + str(blind_corners))
        print("queue_max_len = " + str(queue_max_len))
        print("iterations = " + str(iterations))
        print("all_states = " + str(all_states))

        print(str(py.memory_info().rss) + " bytes")

        return result

    # under attack when queens have same col / row / diagonal
    @staticmethod
    def twoQueensAttack(i1: int, j1: int, i2: int, j2: int) -> bool:
        return i1 == i2 or j1 == j2 or abs(i1 - i2) == abs(j1 - j2)

    @staticmethod
    def get_nq_col(tuple: []) -> int:
        res = next((i for i, x in enumerate(tuple) if x < 0), -5)
        return res

    def createEmptySolution(self, n):
        return [-1] * n

    def printSolution(self, sol: []):
        print("==Result==")

        for i in range(0, len(sol)):  # loop through the rows
            current_row = ['-'] * len(sol)  # init array[n]
            j = sol.index(i)  # j - column with the queen in current row (i-th)
            current_row[j] = 'Q'  # set Queen to position j
            print(' '.join(str(x) for x in current_row))

    def printStart(self, row, col):
        print("==Start==")
        arr = []
        for i in range(0, 8):
            current_row = ['-'] * 8
            arr.append(current_row)
        arr[row][col] = 'Q'
        for current_row in arr:
            print(*current_row)


    def solveNQueens(self, n: int):
        queue = []
        q_tuple = self.createEmptySolution(n)
        row = randint(0, n - 1)
        col = randint(0, n - 1)
        self.printStart(row, col)
        q_tuple[col] = row
        queue.append(q_tuple)
        res = self.bfs(queue, n)
        print(f"We had {len(res)} variants of solution. They are: {res}")
        if res:
            self.printSolution(res[0])


n = 8
sol = Solution()
sol.solveNQueens(n)
