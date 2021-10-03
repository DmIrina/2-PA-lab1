import heapq
import sys
import time
# https://slidetodoc.com/presentation_image_h2/540198f5eabe4d2dd6678d42873718bc/image-57.jpg
import random
import os
import psutil


class Solution:
    def __init__(self):
        self.timeout = time.time() + 60 * 30  # 30 minutes from now
        self.dead_ends = 0
        self.queue = []
        self.queue_map = set()

    def createRandomSolution(self, n):
        solution = []
        for i in range(0, n):
            rand_val = random.randint(0, n - 1)
            solution.append(rand_val)
        return solution

    # under attack when queens have same col / row / diagonal
    @staticmethod
    def twoQueensAttack(i1: int, j1: int, i2: int, j2: int) -> bool:
        return i1 == i2 or j1 == j2 or abs(i1 - i2) == abs(j1 - j2)

    @staticmethod
    def printSolution(sol: []):
        print("==Result==")

        for i in range(0, len(sol)):  # loop through the rows
            current_row = ['-'] * len(sol)  # init array[n]
            j = sol.index(i)  # j - column with the queen in current row (i-th)
            current_row[j] = 'Q'  # set Queen to position j
            print(' '.join(str(x) for x in current_row))

    @staticmethod
    def printStart(sol: []):
        print("==Start==")
        arr = []
        for j in range(0, 8):
            current_row = ['-'] * 8
            arr.append(current_row)
        for j in range(0, 8):
            for i in range(0, 8):
                if i == sol[j]:
                    arr[i][j] = 'Q'
        for current_row in arr:
            print(*current_row)

    # Calculate number of pairs that attack each other
    def h(self, solution):
        coordinates = []
        attacks = 0
        for j1 in range(0, len(solution)):
            i1 = solution[j1]
            coordinates.append((i1, j1))
            # we don't have duplicates for column due to encoding

        # calculate diagonals for queens:
        i = 0
        j = 1
        while i < len(coordinates) - 1 and j < len(coordinates):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            if abs(x1 - x2) == abs(y1 - y2):
                attacks = attacks + 1
            i = i + 1
            j = j + 1  # if we've seen already 1 queen in diagonal, we will not see others

        # we go through all coordinates and check for same row, remove if found so we don't count twice
        while coordinates:
            coord = coordinates.pop()
            queens_in_row = [t for t in coordinates if t[0] == coord[0]]
            if len(queens_in_row) > 0:
                attacks = attacks + len(queens_in_row)
                for q in queens_in_row:
                    coordinates.remove(q)

        return attacks

    # Check if all queens don't attack each other
    def goal_satisfied(self, grid):
        return self.h(grid) == 0

    def rbfs(self):
        solution = self.dequeue()

        if self.goal_satisfied(solution):
            return solution, True

        children = self.get_children(solution)
        if children:
            for child in children:
                state = (child, self.h(child))
                self.enqueue(state)

            return self.rbfs()
        else:
            return solution, False

    def rbfs2(self, upper_bound):

        while self.queue:
            (h, solution, bound) = self.dequeue()
            print(f"current h is {h} with solution {solution}")
            if self.goal_satisfied(solution):
                return solution, True
            if h > upper_bound:
                continue

            children = self.get_children(solution)
            if children:
                for child in children:
                    state = (child, self.h(child), h)
                    self.enqueue(state)
            else:
                return solution, False

        return None, False

    # enqueues the current state in a priority queue
    # with the value calculated by manhattan dist
    def enqueue(self, state):
        (child, h_value, bound) = state
        if str(child) not in self.queue_map:
            heapq.heappush(self.queue, (h_value, child, bound))
            self.queue_map.add(str(child))  # This is to verify out priority queue does not have this element already

    # pop first element from priority queue
    def dequeue(self):
        if len(self.queue) <= 0:
            return None
        (h, child, bound) = heapq.heappop(self.queue)
        # self.queue_map.remove(str(child))
        return h, child, bound

    def get_children(self, solution):
        children = []

        for j1 in range(0, len(solution)):
            i1 = solution[j1]

            if i1 + 1 < len(solution):
                child = solution.copy()
                child[j1] = i1 + 1
                children.append(child)

            if i1 - 1 >= 0:
                child = solution.copy()
                child[j1] = i1 - 1
                children.append(child)

        return children


print(sys.getrecursionlimit())
sys.setrecursionlimit(4000)
sol = Solution()
init_sol = sol.createRandomSolution(8)
sol.printStart(init_sol)
sol.enqueue((init_sol, sol.h(init_sol), 10000000))
(sol_value, res) = sol.rbfs2(100000000)
print(f"We find it: {res}")

sol.printSolution(sol_value)
