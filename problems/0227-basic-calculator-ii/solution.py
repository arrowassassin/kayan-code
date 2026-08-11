class Solution:
    def calculate(self, s: str) -> int:
        stack = []       # resolved terms; '+'/'-' push, '*'/'/' fold into the top
        num = 0
        op = "+"         # operator waiting to be applied to num
        n = len(s)
        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)
            # apply the pending op on an operator OR at the very last char
            if (not ch.isdigit() and ch != " ") or i == n - 1:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    # int(a / b) truncates toward zero; a // b would floor
                    stack.append(int(stack.pop() / num))
                op = ch
                num = 0
        return sum(stack)
