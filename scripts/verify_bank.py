#!/usr/bin/env python3
"""Programmatic integrity check for the problem bank.

For every problem folder (or those matching the given prefixes):
  - required files exist (problem.md, meta.json, starter.py, tests.json,
    hints.md, editorial.md, solution.py)
  - meta.json has the required fields and a well-formed judge config
  - starter.py parses and defines the judge entry
  - hints.md has >= 3 hints (## sections)
  - editorial.md contains the required 9-part structure markers
  - the reference solution.py passes EVERY visible + hidden test via the
    real judge (this is the "editorial solution passes its own hidden
    suite" guarantee)
  - follow_up / follow_up_of links resolve to existing problems

Usage: python3 scripts/verify_bank.py [slug-prefix ...] [--quick]
Exit code 0 = all good.
"""
import ast
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from judge import runner  # noqa: E402

PROBLEMS = os.path.join(ROOT, "problems")
REQUIRED_FILES = ["problem.md", "meta.json", "starter.py", "tests.json",
                  "hints.md", "editorial.md", "solution.py"]
REQUIRED_META = ["id", "title", "difficulty", "topics", "snowflake_priority", "judge"]
EDITORIAL_MARKERS = [
    "Pattern recognition",
    "Brute force",
    "key insight",
    "derivation",
    "solution",
    "Complexity",
    "Edge-case traps",
    "follow-up",
]
DIFFICULTIES = {"Easy", "Medium", "Hard"}


def check_problem(slug, all_slugs):
    errors = []
    pdir = os.path.join(PROBLEMS, slug)

    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(pdir, f)):
            errors.append(f"missing file: {f}")
    if errors:
        return errors

    try:
        meta = json.load(open(os.path.join(pdir, "meta.json")))
    except json.JSONDecodeError as e:
        return [f"meta.json invalid JSON: {e}"]
    for k in REQUIRED_META:
        if k not in meta:
            errors.append(f"meta.json missing field: {k}")
    if meta.get("difficulty") not in DIFFICULTIES:
        errors.append(f"bad difficulty: {meta.get('difficulty')}")
    if meta.get("snowflake_priority") not in (1, 2, 3):
        errors.append("snowflake_priority must be 1, 2 or 3")
    judge_cfg = meta.get("judge", {})
    if judge_cfg.get("mode") not in ("function", "methods"):
        errors.append("judge.mode must be 'function' or 'methods'")
    if not judge_cfg.get("entry"):
        errors.append("judge.entry missing")
    for link in ("follow_up", "follow_up_of"):
        target = meta.get(link)
        if target and target not in all_slugs:
            errors.append(f"{link} points to unknown problem: {target}")

    try:
        tests = json.load(open(os.path.join(pdir, "tests.json")))
    except json.JSONDecodeError as e:
        return errors + [f"tests.json invalid JSON: {e}"]
    visible, hidden = tests.get("visible", []), tests.get("hidden", [])
    if len(visible) < 2:
        errors.append(f"need >= 2 visible tests, got {len(visible)}")
    if len(hidden) < 4:
        errors.append(f"need >= 4 hidden tests, got {len(hidden)}")
    for i, c in enumerate(visible + hidden):
        if "input" not in c or not isinstance(c["input"], list):
            errors.append(f"test {i}: 'input' must be a JSON array of arguments")
            break

    starter = open(os.path.join(pdir, "starter.py")).read()
    try:
        tree = ast.parse(starter)
        names = {n.name for n in ast.walk(tree)
                 if isinstance(n, (ast.ClassDef, ast.FunctionDef))}
        if judge_cfg.get("mode") == "function":
            if "Solution" not in names:
                errors.append("starter.py must define class Solution")
            elif judge_cfg.get("entry") not in names:
                errors.append(f"starter.py must define method {judge_cfg.get('entry')}")
        elif judge_cfg.get("entry") and judge_cfg["entry"] not in names:
            errors.append(f"starter.py must define class {judge_cfg.get('entry')}")
    except SyntaxError as e:
        errors.append(f"starter.py syntax error: {e}")

    hints = [s for s in open(os.path.join(pdir, "hints.md")).read().split("## ")
             if s.strip()]
    if len(hints) < 3:
        errors.append(f"hints.md needs 3 progressive hints (## sections), got {len(hints)}")

    editorial = open(os.path.join(pdir, "editorial.md")).read()
    for marker in EDITORIAL_MARKERS:
        if marker.lower() not in editorial.lower():
            errors.append(f"editorial.md missing required section: '{marker}'")
    if "Dynamic Programming" in meta.get("topics", []):
        low = editorial.lower()
        if "top-down" not in low or "bottom-up" not in low:
            errors.append("DP editorial must include BOTH top-down and bottom-up versions")

    # the load-bearing check: reference solution passes its own full suite
    solution = open(os.path.join(pdir, "solution.py")).read()
    result = runner.judge_submission(pdir, solution, include_hidden=True)
    if result["status"] != "ok":
        errors.append(f"solution.py failed to run: {result.get('error', '')[:400]}")
    elif result["verdict"] != "AC":
        fails = [(i, c["verdict"]) for i, c in enumerate(result["cases"])
                 if c["verdict"] != "AC"]
        errors.append(f"solution.py NOT AC: {result['verdict']} on cases {fails[:6]}")
    return errors


def main():
    prefixes = [a for a in sys.argv[1:] if not a.startswith("-")]
    slugs = sorted(d for d in os.listdir(PROBLEMS)
                   if os.path.isdir(os.path.join(PROBLEMS, d)))
    all_slugs = set(slugs)
    if prefixes:
        slugs = [s for s in slugs if any(s.startswith(p) for p in prefixes)]
    if not slugs:
        print("No problems matched.")
        sys.exit(1)

    failed = 0
    for slug in slugs:
        errors = check_problem(slug, all_slugs)
        if errors:
            failed += 1
            print(f"✗ {slug}")
            for e in errors:
                print(f"    - {e}")
        else:
            print(f"✓ {slug}")
    print(f"\n{len(slugs) - failed}/{len(slugs)} problems pass integrity checks.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
