"""Judge harness. Runs inside the sandboxed subprocess.

Usage: python3 harness.py <payload.json> <results.json>

Payload:
{
  "user_code": "...",
  "judge": {
    "mode": "function" | "methods",
    "entry": "numIslands" | "LRUCache",
    "arg_types": ["raw", "tree", "listnode", "listnode[]", "graph"],   # optional, per-arg
    "ret_type": "raw" | "tree" | "listnode" | "graph" | "float",       # optional
    "compare": "exact" | "unordered" | "unordered_2d" | "float",       # default exact
    "compare_arg": 0,          # optional: compare this (mutated) argument instead of return
    "time_limit": 3.0,         # seconds per test
  },
  "checker_src": "def check(args_after, returned, expected): ...",     # optional
  "cases": [{"input": [...], "expected": ...}, ...]
}

Results file: {"status": "ok", "cases": [{verdict, time_ms, output, expected, stdout, error}]}
             or {"status": "error", "error": "..."}

Per-test wall clock is enforced with SIGALRM; an address-space rlimit caps
memory; user prints are captured and truncated to 10KB.
"""
import io
import json
import math
import resource
import signal
import sys
import time
import traceback

MEM_LIMIT_BYTES = 1024 * 1024 * 1024  # 1 GB address space
STDOUT_CAP = 10 * 1024                # 10KB of user prints per test
FLOAT_TOL = 1e-6


# ---------- shared data structures available to user code ----------

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Node:  # graph node (LC 133 style)
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_tree(values):
    """Level-order array with nulls -> TreeNode."""
    if not values:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = [root]
    for node in queue:
        try:
            v = next(it)
            if v is not None:
                node.left = TreeNode(v)
                queue.append(node.left)
            v = next(it)
            if v is not None:
                node.right = TreeNode(v)
                queue.append(node.right)
        except StopIteration:
            break
    return root


def tree_to_list(root):
    """TreeNode -> level-order array, trailing nulls stripped."""
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def build_listnode(values):
    head = None
    for v in reversed(values or []):
        head = ListNode(v, head)
    return head


def listnode_to_list(head, max_len=100000):
    out = []
    while head is not None and len(out) < max_len:
        out.append(head.val)
        head = head.next
    if head is not None:
        raise ValueError("linked list too long or cyclic")
    return out


def build_graph(adj):
    """Adjacency list (1-indexed node values, LC 133 format) -> Node."""
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, neighbors in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
    return nodes[0]


def graph_to_adj(node):
    if node is None:
        return []
    seen = {}
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.val in seen:
            continue
        seen[cur.val] = cur
        stack.extend(cur.neighbors)
    n = max(seen)
    return [[nb.val for nb in seen[i + 1].neighbors] if (i + 1) in seen else []
            for i in range(n)]


# ---------- conversion ----------

def convert_arg(value, typ):
    if typ == "tree":
        return build_tree(value)
    if typ == "listnode":
        return build_listnode(value)
    if typ == "listnode[]":
        return [build_listnode(v) for v in value]
    if typ == "graph":
        return build_graph(value)
    return value


def convert_ret(value, typ):
    if typ == "tree":
        return tree_to_list(value)
    if typ == "listnode":
        return listnode_to_list(value)
    if typ == "graph":
        return graph_to_adj(value)
    return value


# ---------- comparison ----------

def canonical(x):
    if isinstance(x, tuple):
        x = list(x)
    if isinstance(x, list):
        return [canonical(v) for v in x]
    if isinstance(x, dict):
        return {k: canonical(v) for k, v in x.items()}
    if isinstance(x, set):
        return sorted((canonical(v) for v in x), key=repr)
    return x


def _key(x):
    return json.dumps(x, sort_keys=True, default=repr)


def values_equal(actual, expected, mode):
    actual, expected = canonical(actual), canonical(expected)
    if isinstance(expected, dict) and set(expected.keys()) == {"$anyOf"}:
        return any(values_equal(actual, opt, mode) for opt in expected["$anyOf"])
    if mode == "float":
        return floats_equal(actual, expected)
    if mode == "unordered":
        if not isinstance(actual, list) or not isinstance(expected, list):
            return False
        return sorted(map(_key, actual)) == sorted(map(_key, expected))
    if mode == "unordered_2d":
        if not isinstance(actual, list) or not isinstance(expected, list):
            return False
        norm = lambda outer: sorted(_key(sorted(inner, key=_key) if isinstance(inner, list) else inner) for inner in outer)
        return norm(actual) == norm(expected)
    # exact — but bool is not int, and int == float allowed
    return exact_equal(actual, expected)


def exact_equal(a, b):
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(exact_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(exact_equal(a[k], b[k]) for k in a)
    if isinstance(a, float) or isinstance(b, float):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return False
        return floats_equal(a, b)
    return a == b


def floats_equal(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(floats_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=FLOAT_TOL, abs_tol=FLOAT_TOL)
    return exact_equal(a, b)


# ---------- per-test sequence for "methods" mode ----------

def run_methods_case(ns, entry, case_input):
    ops, args_list = case_input
    cls = ns[entry]
    obj = cls(*args_list[0])
    outputs = [None]
    for op, args in zip(ops[1:], args_list[1:]):
        outputs.append(getattr(obj, op)(*args))
    return outputs


# ---------- timeout ----------

class TestTimeout(Exception):
    pass


def _alarm(signum, frame):
    raise TestTimeout()


class CappedWriter(io.StringIO):
    def __init__(self, cap):
        super().__init__()
        self.cap = cap
        self.truncated = False

    def write(self, s):
        if self.tell() < self.cap:
            super().write(s[: self.cap - self.tell()])
            if self.tell() >= self.cap:
                self.truncated = True
        else:
            self.truncated = True
        return len(s)


def trimmed_traceback():
    """Traceback showing only frames from the user's code (<solution>)."""
    etype, evalue, tb = sys.exc_info()
    frames = traceback.extract_tb(tb)
    user_frames = [f for f in frames if f.filename == "<solution>"]
    shown = user_frames if user_frames else frames[-3:]
    lines = ["Traceback (most recent call last):\n"]
    lines += traceback.format_list(shown)
    lines += traceback.format_exception_only(etype, evalue)
    return "".join(lines)


def main():
    payload_path, results_path = sys.argv[1], sys.argv[2]
    with open(payload_path) as f:
        payload = json.load(f)

    try:
        resource.setrlimit(resource.RLIMIT_AS, (MEM_LIMIT_BYTES, MEM_LIMIT_BYTES))
    except (ValueError, OSError):
        pass
    sys.setrecursionlimit(30000)

    judge = payload.get("judge", {})
    mode = judge.get("mode", "function")
    entry = judge["entry"]
    arg_types = judge.get("arg_types")
    ret_type = judge.get("ret_type", "raw")
    compare = judge.get("compare", "exact")
    compare_arg = judge.get("compare_arg")
    time_limit = float(judge.get("time_limit", 3.0))

    ns = {
        "TreeNode": TreeNode, "ListNode": ListNode, "Node": Node,
        "__name__": "solution",
    }

    def finish(obj):
        with open(results_path, "w") as f:
            json.dump(obj, f)
        sys.exit(0)

    try:
        code_obj = compile(payload["user_code"], "<solution>", "exec")
        exec(code_obj, ns)
    except Exception:
        finish({"status": "error", "error": trimmed_traceback()})

    checker = None
    if payload.get("checker_src"):
        cns = dict(ns)
        exec(compile(payload["checker_src"], "<checker>", "exec"), cns)
        checker = cns["check"]

    if mode == "function":
        if "Solution" not in ns:
            finish({"status": "error", "error": "No `class Solution` found in your code."})
        sol = ns["Solution"]()
        if not hasattr(sol, entry):
            finish({"status": "error",
                    "error": f"`class Solution` has no method `{entry}`."})
        func = getattr(sol, entry)
    elif entry not in ns:
        finish({"status": "error", "error": f"No `class {entry}` found in your code."})

    signal.signal(signal.SIGALRM, _alarm)
    results = []
    for case in payload["cases"]:
        raw_input = case["input"]
        expected = case.get("expected")
        cap = CappedWriter(STDOUT_CAP)
        real_stdout = sys.stdout
        verdict, output_repr, error, elapsed_ms = "AC", None, None, 0
        try:
            if mode == "function":
                args = list(raw_input)
                if arg_types:
                    args = [convert_arg(a, t) for a, t in zip(args, arg_types)]
                sys.stdout = cap
                signal.setitimer(signal.ITIMER_REAL, time_limit)
                t0 = time.perf_counter()
                returned = func(*args)
                elapsed_ms = (time.perf_counter() - t0) * 1000
                signal.setitimer(signal.ITIMER_REAL, 0)
                sys.stdout = real_stdout
                actual = convert_ret(returned, ret_type)
                if checker:
                    args_after = [convert_ret(a, t) if t in ("tree", "listnode", "graph") else a
                                  for a, t in zip(args, arg_types or ["raw"] * len(args))]
                    ok = checker(args_after, actual, expected)
                    note = None
                    if isinstance(ok, tuple):
                        ok, note = ok
                    verdict = "AC" if ok else "WA"
                    if note and verdict == "WA":
                        error = note
                elif compare_arg is not None:
                    actual = args[compare_arg]
                    verdict = "AC" if values_equal(actual, expected, compare) else "WA"
                else:
                    verdict = "AC" if values_equal(actual, expected, compare) else "WA"
                output_repr = _safe_json(actual)
            else:  # methods
                sys.stdout = cap
                signal.setitimer(signal.ITIMER_REAL, time_limit)
                t0 = time.perf_counter()
                outputs = run_methods_case(ns, entry, raw_input)
                elapsed_ms = (time.perf_counter() - t0) * 1000
                signal.setitimer(signal.ITIMER_REAL, 0)
                sys.stdout = real_stdout
                if checker:
                    ok = checker([raw_input], outputs, expected)
                    note = None
                    if isinstance(ok, tuple):
                        ok, note = ok
                    verdict = "AC" if ok else "WA"
                    if note and verdict == "WA":
                        error = note
                else:
                    ok = len(outputs) == len(expected) and all(
                        values_equal(a, e, compare) for a, e in zip(outputs, expected))
                    verdict = "AC" if ok else "WA"
                output_repr = _safe_json(outputs)
        except TestTimeout:
            elapsed_ms = time_limit * 1000
            verdict = "TLE"
            error = f"Time limit exceeded ({time_limit:.0f}s)"
        except MemoryError:
            verdict = "RE"
            error = "Memory limit exceeded"
        except RecursionError:
            verdict = "RE"
            error = "RecursionError: maximum recursion depth exceeded"
        except Exception:
            verdict = "RE"
            error = trimmed_traceback()
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            sys.stdout = real_stdout

        stdout_text = cap.getvalue()
        if cap.truncated:
            stdout_text += "\n... [stdout truncated at 10KB]"
        results.append({
            "verdict": verdict,
            "time_ms": round(elapsed_ms, 2),
            "output": output_repr,
            "expected": expected,
            "stdout": stdout_text,
            "error": error,
        })

    finish({"status": "ok", "cases": results})


def _safe_json(x):
    """Best-effort JSON-serializable rendition of a return value."""
    try:
        json.dumps(x)
        return x
    except (TypeError, ValueError):
        return repr(x)


if __name__ == "__main__":
    main()
