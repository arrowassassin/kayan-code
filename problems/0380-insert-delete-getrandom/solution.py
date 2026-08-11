import random


class RandomizedSet:
    """Dynamic array of values + dict val -> index. Removal swaps the
    victim with the last element so the array never has holes; getRandom
    is one uniform index draw. All three ops O(1) average."""

    def __init__(self):
        self.vals = []
        self.pos = {}       # val -> its index in self.vals

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.vals[-1]
        self.vals[i] = last         # move last element into the hole
        self.pos[last] = i          # (harmless no-op when val IS last)
        self.vals.pop()
        del self.pos[val]
        return True

    def getRandom(self) -> int:
        return self.vals[random.randrange(len(self.vals))]
