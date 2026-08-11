class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        lo, hi = 0, len(numbers) - 1
        while lo < hi:
            s = numbers[lo] + numbers[hi]
            if s == target:
                return [lo + 1, hi + 1]      # 1-indexed by the statement
            if s < target:
                lo += 1                      # sum too small: only a bigger left value can help
            else:
                hi -= 1                      # sum too big: only a smaller right value can help
        return []                            # unreachable: a pair is guaranteed
