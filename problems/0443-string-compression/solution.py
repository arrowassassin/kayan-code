class Solution:
    def compress(self, chars: list[str]) -> int:
        write = 0
        read = 0
        n = len(chars)
        while read < n:
            ch = chars[read]
            start = read
            while read < n and chars[read] == ch:   # measure the whole run first
                read += 1
            chars[write] = ch
            write += 1
            count = read - start
            if count > 1:                            # a lone char gets NO count digit
                for d in str(count):                 # 12 -> '1','2' (multi-char counts)
                    chars[write] = d
                    write += 1
        return write
