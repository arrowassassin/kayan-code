def check(args_after, returned, expected):
    """Accept ANY valid topological ordering.

    expected == []  -> the prerequisites contain a cycle: answer must be [].
    otherwise       -> expected is just one sample valid order; the real
                       validation runs against numCourses + prerequisites.
    """
    n, prerequisites = args_after[0], args_after[1]

    if expected == []:
        if returned == []:
            return True
        return (False, "the prerequisites contain a cycle, so the answer must be []")

    if not isinstance(returned, list) or any(not isinstance(x, int) or isinstance(x, bool) for x in returned):
        return (False, "answer must be a list of course numbers")
    if sorted(returned) != list(range(n)):
        return (False, f"answer must be a permutation of 0..{n - 1}")

    pos = {course: i for i, course in enumerate(returned)}
    for a, b in prerequisites:
        if pos[b] >= pos[a]:
            return (False, f"course {b} is a prerequisite of course {a} but does not come before it")
    return True
