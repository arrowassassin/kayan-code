def check(args_after, returned, expected):
    # expected carries the full compressed char array; k must equal its length
    # and the first k slots of the mutated input must match it exactly.
    if not isinstance(returned, int) or isinstance(returned, bool):
        return False, "return the new length k as an int"
    if returned != len(expected):
        return False, f"wrong length: expected k = {len(expected)}, returned {returned}"
    prefix = args_after[0][:returned]
    if prefix != expected:
        return False, f"first k entries of chars should be {expected}, got {prefix}"
    return True
