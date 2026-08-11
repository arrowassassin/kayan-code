class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split("/"):
            if part == "" or part == ".":
                continue                 # empty (from // or edges) and "here" are no-ops
            if part == "..":
                if stack:                # ".." at root stays at root
                    stack.pop()
            else:
                stack.append(part)       # real name, including things like "..." or ".hidden"
        return "/" + "/".join(stack)
