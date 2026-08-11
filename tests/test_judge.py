"""Judge behavior tests: AC / WA / TLE / crash / exception / methods mode."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from judge import runner

ADD_CFG = {"mode": "function", "entry": "add", "compare": "exact", "time_limit": 2.0}
ADD_CASES = [{"input": [1, 2], "expected": 3}, {"input": [-1, 1], "expected": 0}]


def run(code, cases=ADD_CASES, cfg=ADD_CFG, checker=None):
    return runner.run_cases(code, cases, cfg, checker)


def test_accepted():
    r = run("class Solution:\n    def add(self, a, b):\n        return a + b\n")
    assert r["status"] == "ok"
    assert [c["verdict"] for c in r["cases"]] == ["AC", "AC"]
    assert all(c["time_ms"] < 2000 for c in r["cases"])


def test_wrong_answer():
    r = run("class Solution:\n    def add(self, a, b):\n        return a - b\n")
    assert r["cases"][0]["verdict"] == "WA"
    assert r["cases"][0]["output"] == -1
    assert r["cases"][1]["verdict"] == "WA"


def test_time_limit_exceeded():
    r = run("class Solution:\n    def add(self, a, b):\n"
            "        while True:\n            pass\n")
    assert r["cases"][0]["verdict"] == "TLE"
    assert "Time limit" in r["cases"][0]["error"]


def test_exception_in_user_code():
    r = run("class Solution:\n    def add(self, a, b):\n        return a / 0\n")
    assert r["cases"][0]["verdict"] == "RE"
    assert "ZeroDivisionError" in r["cases"][0]["error"]


def test_syntax_error_is_reported():
    r = run("class Solution\n    def add(self, a, b): return 3\n")
    assert r["status"] == "error"
    assert "SyntaxError" in r["error"]


def test_missing_solution_class():
    r = run("def add(a, b):\n    return a + b\n")
    assert r["status"] == "error"
    assert "Solution" in r["error"]


def test_missing_method():
    r = run("class Solution:\n    def wrong_name(self, a, b):\n        return a + b\n")
    assert r["status"] == "error"
    assert "add" in r["error"]


def test_stdout_captured_and_truncated():
    r = run("class Solution:\n    def add(self, a, b):\n"
            "        print('x' * 20000)\n        return a + b\n")
    assert r["cases"][0]["verdict"] == "AC"
    assert "truncated" in r["cases"][0]["stdout"]
    assert len(r["cases"][0]["stdout"]) < 11000


def test_infinite_recursion_is_runtime_error():
    r = run("class Solution:\n    def add(self, a, b):\n"
            "        return self.add(a, b)\n")
    assert r["cases"][0]["verdict"] == "RE"
    assert "Recursion" in r["cases"][0]["error"]


def test_unordered_compare():
    cfg = {"mode": "function", "entry": "f", "compare": "unordered", "time_limit": 2.0}
    r = run("class Solution:\n    def f(self, xs):\n        return sorted(xs, reverse=True)\n",
            [{"input": [[1, 2, 3]], "expected": [1, 3, 2]}], cfg)
    assert r["cases"][0]["verdict"] == "AC"


def test_unordered_2d_compare():
    cfg = {"mode": "function", "entry": "f", "compare": "unordered_2d", "time_limit": 2.0}
    r = run("class Solution:\n    def f(self, xs):\n        return [[3,1],[2]]\n",
            [{"input": [[0]], "expected": [[2], [1, 3]]}], cfg)
    assert r["cases"][0]["verdict"] == "AC"


def test_tree_arg_and_ret():
    cfg = {"mode": "function", "entry": "mirror", "arg_types": ["tree"],
           "ret_type": "tree", "compare": "exact", "time_limit": 2.0}
    code = ("class Solution:\n"
            "    def mirror(self, root):\n"
            "        if not root: return None\n"
            "        root.left, root.right = "
            "self.mirror(root.right), self.mirror(root.left)\n"
            "        return root\n")
    r = run(code, [{"input": [[1, 2, 3]], "expected": [1, 3, 2]}], cfg)
    assert r["cases"][0]["verdict"] == "AC"


def test_methods_mode():
    cfg = {"mode": "methods", "entry": "Counter", "compare": "exact", "time_limit": 2.0}
    code = ("class Counter:\n"
            "    def __init__(self, start):\n        self.n = start\n"
            "    def incr(self):\n        self.n += 1\n        return self.n\n")
    cases = [{"input": [["Counter", "incr", "incr"], [[10], [], []]],
              "expected": [None, 11, 12]}]
    r = run(code, cases, cfg)
    assert r["cases"][0]["verdict"] == "AC"


def test_methods_any_of():
    cfg = {"mode": "methods", "entry": "Bag", "compare": "exact", "time_limit": 2.0}
    code = ("class Bag:\n"
            "    def __init__(self):\n        self.xs = [3, 7]\n"
            "    def pick(self):\n        return self.xs[0]\n")
    cases = [{"input": [["Bag", "pick"], [[], []]],
              "expected": [None, {"$anyOf": [3, 7]}]}]
    r = run(code, cases, cfg)
    assert r["cases"][0]["verdict"] == "AC"


def test_custom_checker():
    cfg = {"mode": "function", "entry": "anyPalindrome", "compare": "exact",
           "time_limit": 2.0}
    checker = ("def check(args_after, returned, expected):\n"
               "    return returned == returned[::-1] and len(returned) == expected\n")
    r = run("class Solution:\n    def anyPalindrome(self, n):\n        return 'a' * n\n",
            [{"input": [3], "expected": 3}], cfg, checker)
    assert r["cases"][0]["verdict"] == "AC"


def test_compare_arg_inplace():
    cfg = {"mode": "function", "entry": "sortColors", "compare": "exact",
           "compare_arg": 0, "time_limit": 2.0}
    r = run("class Solution:\n    def sortColors(self, nums):\n        nums.sort()\n",
            [{"input": [[2, 0, 1]], "expected": [0, 1, 2]}], cfg)
    assert r["cases"][0]["verdict"] == "AC"


def test_bool_is_not_int():
    r = run("class Solution:\n    def add(self, a, b):\n        return True\n",
            [{"input": [0, 1], "expected": 1}])
    assert r["cases"][0]["verdict"] == "WA"
