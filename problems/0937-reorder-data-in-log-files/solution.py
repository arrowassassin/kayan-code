class Solution:
    def reorderLogFiles(self, logs: list[str]) -> list[str]:
        def sort_key(log: str):
            ident, rest = log.split(" ", 1)
            if rest[0].isdigit():
                return (1,)              # all digit-logs share one key -> stable order kept
            return (0, rest, ident)      # letter-logs: content first, identifier breaks ties
        return sorted(logs, key=sort_key)   # sorted() is stable — that IS the algorithm
