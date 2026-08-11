def check(args_after, returned, expected):
    """expected == "" flags the impossible case; otherwise `expected` is just
    one sample valid answer — any permutation of s with no equal neighbors
    is accepted."""
    s = args_after[0]

    if expected == "":
        if returned == "":
            return True
        return (False, 'no valid rearrangement exists — expected ""')

    if not isinstance(returned, str):
        return (False, f"expected a string, got {type(returned).__name__}")
    if returned == "":
        return (False, "a valid rearrangement exists but \"\" was returned")
    if sorted(returned) != sorted(s):
        return (False, "returned string is not a permutation of the input")
    for i in range(len(returned) - 1):
        if returned[i] == returned[i + 1]:
            return (False, f"equal adjacent characters {returned[i]!r} at index {i}")
    return True
