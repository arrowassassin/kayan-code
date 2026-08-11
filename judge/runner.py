"""Subprocess judge: writes a payload, runs harness.py in a child python,
collects per-case verdicts. The child enforces per-test wall time (SIGALRM),
an address-space memory cap, and 10KB stdout truncation; this parent adds a
whole-run backstop timeout in case the child wedges.
"""
import json
import os
import subprocess
import sys
import tempfile

HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness.py")
BACKSTOP_SLACK = 10  # seconds beyond sum of per-test limits


def run_cases(user_code, cases, judge_cfg, checker_src=None):
    """Run user_code against cases. Returns
    {"status": "ok", "cases": [...]} or {"status": "error", "error": str}.
    """
    payload = {
        "user_code": user_code,
        "judge": judge_cfg,
        "cases": cases,
        "checker_src": checker_src,
    }
    time_limit = float(judge_cfg.get("time_limit", 3.0))
    backstop = time_limit * max(1, len(cases)) + BACKSTOP_SLACK

    with tempfile.TemporaryDirectory(prefix="kayan-judge-") as tmp:
        payload_path = os.path.join(tmp, "payload.json")
        results_path = os.path.join(tmp, "results.json")
        with open(payload_path, "w") as f:
            json.dump(payload, f)
        try:
            proc = subprocess.run(
                [sys.executable, HARNESS, payload_path, results_path],
                capture_output=True, text=True, timeout=backstop, cwd=tmp,
            )
        except subprocess.TimeoutExpired:
            return {"status": "error",
                    "error": f"Judge backstop timeout after {backstop:.0f}s "
                             "(runaway process killed)."}
        if not os.path.exists(results_path):
            detail = (proc.stderr or proc.stdout or "").strip()[-2000:]
            return {"status": "error",
                    "error": "Judge crashed before producing results."
                             + (f"\n{detail}" if detail else "")}
        with open(results_path) as f:
            return json.load(f)


def load_problem(problem_dir):
    """Load meta.json / tests.json / optional checker.py for a problem dir."""
    with open(os.path.join(problem_dir, "meta.json")) as f:
        meta = json.load(f)
    with open(os.path.join(problem_dir, "tests.json")) as f:
        tests = json.load(f)
    checker_src = None
    checker_path = os.path.join(problem_dir, "checker.py")
    if os.path.exists(checker_path):
        with open(checker_path) as f:
            checker_src = f.read()
    return meta, tests, checker_src


def judge_submission(problem_dir, user_code, include_hidden=True, custom_cases=None):
    """Judge a run (visible/custom cases) or submission (visible + hidden)."""
    meta, tests, checker_src = load_problem(problem_dir)
    if custom_cases is not None:
        cases = custom_cases
    else:
        cases = list(tests.get("visible", []))
        if include_hidden:
            cases += tests.get("hidden", [])
    result = run_cases(user_code, cases, meta["judge"], checker_src)
    if result["status"] == "ok":
        n_visible = len(tests.get("visible", [])) if custom_cases is None else len(cases)
        first_fail_revealed = False
        for i, c in enumerate(result["cases"]):
            c["hidden"] = custom_cases is None and include_hidden and i >= n_visible
            if not c["hidden"]:
                c["input"] = cases[i]["input"]
            elif c["verdict"] != "AC" and not first_fail_revealed:
                # like LeetCode: reveal the first failing hidden case
                c["input"] = cases[i]["input"]
                first_fail_revealed = True
            else:
                # other hidden cases: verdict + runtime only
                c["expected"] = None
                c["stdout"] = ""
                if c["verdict"] == "AC":
                    c["output"] = None
        result["passed"] = sum(1 for c in result["cases"] if c["verdict"] == "AC")
        result["total"] = len(result["cases"])
        result["verdict"] = overall_verdict(result["cases"])
        result["runtime_ms"] = round(sum(c["time_ms"] for c in result["cases"]), 2)
    return result


def overall_verdict(cases):
    order = ["RE", "TLE", "WA"]
    for v in order:
        if any(c["verdict"] == v for c in cases):
            return v
    return "AC" if cases else "WA"
