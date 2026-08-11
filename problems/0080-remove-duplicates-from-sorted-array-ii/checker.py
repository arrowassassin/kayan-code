def check(args_after, returned, expected):
    """expected = the exact list of surviving elements.

    Verifies the returned k and that the first k slots of the mutated
    array match; slots beyond k are ignored, per the statement.
    """
    if returned != len(expected):
        return (False, f"returned k={returned}, expected k={len(expected)}")
    if args_after[0][:returned] != expected:
        return (False, f"nums[:k] is {args_after[0][:returned]!r}, expected {expected!r}")
    return True
