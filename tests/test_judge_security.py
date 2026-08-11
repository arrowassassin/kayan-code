"""Judge hardening regressions: TLE cannot be dodged; process-exit and
malformed cases become RE, not infra crashes."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from judge import runner

CFG = {"mode": "function", "entry": "f", "compare": "exact", "time_limit": 1.0}


def run(code, cases):
    return runner.run_cases(code, cases, CFG)


def test_tle_not_dodged_by_swallowing_alarm():
    code = ("class Solution:\n"
            "    def f(self, n):\n"
            "        import time\n"
            "        end = time.time() + 3\n"
            "        while time.time() < end:\n"
            "            try:\n"
            "                pass\n"
            "            except BaseException:\n"
            "                pass\n"
            "        return n\n")
    r = run(code, [{"input": [1], "expected": 1}])
    assert r["cases"][0]["verdict"] == "TLE"


def test_tle_not_dodged_by_resetting_itimer():
    code = ("import signal, time\n"
            "class Solution:\n"
            "    def f(self, n):\n"
            "        signal.setitimer(signal.ITIMER_REAL, 0)\n"
            "        end = time.time() + 3\n"
            "        while time.time() < end:\n"
            "            pass\n"
            "        return n\n")
    r = run(code, [{"input": [1], "expected": 1}])
    assert r["cases"][0]["verdict"] == "TLE"


def test_sys_exit_becomes_runtime_error():
    code = ("class Solution:\n"
            "    def f(self, n):\n"
            "        import sys\n"
            "        sys.exit(0)\n")
    r = run(code, [{"input": [1], "expected": 1}])
    assert r["status"] == "ok"
    assert r["cases"][0]["verdict"] == "RE"


def test_baseexception_still_caught_per_case():
    code = ("class Solution:\n"
            "    def f(self, n):\n"
            "        raise BaseException('boom')\n")
    r = run(code, [{"input": [1], "expected": 1}])
    assert r["cases"][0]["verdict"] == "RE"


def test_custom_case_count_capped():
    import pytest
    with pytest.raises(ValueError):
        runner.judge_submission(
            os.path.join(os.path.dirname(__file__), "..", "problems",
                         "0057-insert-interval"),
            "class Solution:\n    def insert(self,a,b): return a\n",
            custom_cases=[{"input": [[], [1]], "expected": []}] * 99)


def test_api_supplied_input_py_not_evaluated():
    """sanitize_custom_case must strip input_py (RCE vector)."""
    c = runner.sanitize_custom_case(
        {"input": [1], "expected": 2, "input_py": "1/0", "expected_py": "1/0"})
    assert c == {"input": [1], "expected": 2}
