import heapq


class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda it: it[0])   # process meetings in start order

        ends = []                              # min-heap of end times of occupied rooms
        for start, end in intervals:
            if ends and ends[0] <= start:
                # the earliest-freeing room is free by now -> reuse it
                heapq.heapreplace(ends, end)
            else:
                heapq.heappush(ends, end)      # every room busy -> open a new one
        return len(ends)
