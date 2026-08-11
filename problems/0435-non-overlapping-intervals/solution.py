class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda it: it[1])   # earliest finisher first

        removed = 0
        kept_end = float("-inf")
        for start, end in intervals:
            if start >= kept_end:
                # doesn't overlap the last kept interval (touching is OK)
                kept_end = end
            else:
                removed += 1                   # drop it; the kept one ends sooner
        return removed
