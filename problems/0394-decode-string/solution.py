class Solution:
    def decodeString(self, s: str) -> str:
        stack = []       # frames of (outer_pieces, repeat_count)
        cur = []         # pieces of the string being built at this depth
        num = 0          # multiplier being accumulated digit by digit
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)     # multi-digit counts like 12[
            elif ch == "[":
                stack.append((cur, num))     # suspend the outer context
                cur, num = [], 0
            elif ch == "]":
                outer, k = stack.pop()       # finish this block, resume outer
                outer.append("".join(cur) * k)
                cur = outer
            else:
                cur.append(ch)
        return "".join(cur)
