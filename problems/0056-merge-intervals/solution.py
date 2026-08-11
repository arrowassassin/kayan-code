class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort(key=lambda it: it[0])

        merged = [intervals[0][:]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                # overlaps (or touches) the last merged interval -> extend it
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged
