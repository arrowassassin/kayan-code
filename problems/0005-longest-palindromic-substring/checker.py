def check(args_after, returned, expected):
    """Any max-length palindromic substring of the input is accepted.

    `expected` carries one valid answer; only its LENGTH is authoritative.
    """
    s = args_after[0]
    if not isinstance(returned, str):
        return (False, "return value must be a string")
    if returned not in s:
        return (False, "returned string is not a substring of the input")
    if returned != returned[::-1]:
        return (False, "returned string is not a palindrome")
    if len(returned) != len(expected):
        return (False,
                f"length {len(returned)} != optimal length {len(expected)}")
    return True
