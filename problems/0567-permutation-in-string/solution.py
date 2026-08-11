class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)
        if n1 > n2:
            return False

        need = [0] * 26
        win = [0] * 26
        a = ord("a")
        for i in range(n1):
            need[ord(s1[i]) - a] += 1
            win[ord(s2[i]) - a] += 1

        # matches = number of letters whose window count equals the target
        matches = sum(1 for i in range(26) if need[i] == win[i])
        if matches == 26:
            return True

        for right in range(n1, n2):
            # add the entering character
            i = ord(s2[right]) - a
            win[i] += 1
            if win[i] == need[i]:
                matches += 1
            elif win[i] == need[i] + 1:
                matches -= 1
            # drop the leaving character (fixed window size n1)
            j = ord(s2[right - n1]) - a
            win[j] -= 1
            if win[j] == need[j]:
                matches += 1
            elif win[j] == need[j] - 1:
                matches -= 1
            if matches == 26:
                return True
        return False
