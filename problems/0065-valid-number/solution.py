class Solution:
    def isNumber(self, s: str) -> bool:
        s = s.strip(" ")            # leading/trailing spaces are allowed, nothing else
        n = len(s)

        def scan_digits(i: int):
            """Advance past ASCII digits; report whether we saw at least one."""
            start = i
            while i < n and "0" <= s[i] <= "9":
                i += 1
            return i, i > start

        i = 0
        if i < n and s[i] in "+-":               # optional sign
            i += 1
        i, int_digits = scan_digits(i)           # integer part
        frac_digits = False
        if i < n and s[i] == ".":                # optional decimal point
            i += 1
            i, frac_digits = scan_digits(i)      # fractional part
        if not (int_digits or frac_digits):      # ".", "+", "+." all die here
            return False
        if i < n and s[i] in "eE":               # optional exponent
            i += 1
            if i < n and s[i] in "+-":
                i += 1
            i, exp_digits = scan_digits(i)
            if not exp_digits:                   # "4e", "4e+" die here
                return False
        return i == n                            # every character must be consumed
