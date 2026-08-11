import bisect


class Solution:
    def jobScheduling(self, startTime: list[int], endTime: list[int],
                      profit: list[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))   # by end time
        # Parallel arrays forming a monotone "profit frontier":
        # ends[k] is increasing, best[k] = max profit using jobs ending <= ends[k].
        ends = [0]
        best = [0]
        for e, s, p in jobs:
            # richest compatible prefix: last frontier entry with end <= s
            # (a job may start exactly when another ends)
            i = bisect.bisect_right(ends, s) - 1
            take = best[i] + p
            if take > best[-1]:               # only record improvements,
                ends.append(e)                # keeping best[] increasing
                best.append(take)
        return best[-1]
