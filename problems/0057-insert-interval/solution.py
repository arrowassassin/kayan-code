class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        res = []
        i, n = 0, len(intervals)
        start, end = newInterval

        # 1) everything strictly before the new interval
        while i < n and intervals[i][1] < start:
            res.append(intervals[i])
            i += 1

        # 2) absorb every interval that touches [start, end]
        while i < n and intervals[i][0] <= end:
            start = min(start, intervals[i][0])
            end = max(end, intervals[i][1])
            i += 1
        res.append([start, end])

        # 3) everything strictly after
        res.extend(intervals[i:])
        return res
