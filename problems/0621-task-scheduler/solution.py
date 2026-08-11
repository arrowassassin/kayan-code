from collections import Counter


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        f = max(counts.values())                     # highest frequency
        ties = sum(1 for c in counts.values() if c == f)
        # Frame around the most frequent task: (f-1) gaps of width (n+1),
        # then one final row holding every max-frequency task.
        frame = (f - 1) * (n + 1) + ties
        # If tasks overflow the frame, they fill all idles -> no waiting at all.
        return max(len(tasks), frame)
