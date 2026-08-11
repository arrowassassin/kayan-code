import heapq


class Solution:
    def employeeFreeTime(self, schedule: list[list[list[int]]]) -> list[list[int]]:
        # k-way merge of the per-employee sorted lists via a min-heap.
        # Heap entry: (start, employee index, interval index)
        heap = [(emp[0][0], i, 0) for i, emp in enumerate(schedule)]
        heapq.heapify(heap)

        free = []
        busy_until = None                  # right edge of the merged busy block so far
        while heap:
            start, i, j = heapq.heappop(heap)
            end = schedule[i][j][1]
            if busy_until is None or start <= busy_until:
                # touches/overlaps the current busy block -> extend it
                busy_until = end if busy_until is None else max(busy_until, end)
            else:
                free.append([busy_until, start])   # a gap nobody works in
                busy_until = end
            if j + 1 < len(schedule[i]):
                heapq.heappush(heap, (schedule[i][j + 1][0], i, j + 1))
        return free
