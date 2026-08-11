"""AI-output parsing: fence extraction (markdown-it) and review JSON
recovery (json-repair + pydantic) — no network involved."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reviewer.ai_review import AIReview, extract_code, parse_review


def test_extract_fenced_python():
    out = extract_code("Sure!\n```python\ndef f():\n    return 1\n```\nDone.")
    assert out == "def f():\n    return 1\n"


def test_extract_prefers_python_fence():
    out = extract_code("```java\nint x;\n```\n```python\nx = 1\n```")
    assert out.strip() == "x = 1"


def test_extract_unfenced_falls_through():
    assert extract_code("x = 1").strip() == "x = 1"


def test_parse_review_valid_json():
    r = parse_review('{"correctness_verdict": "ok", "missed_edge_cases": [],'
                     ' "complexity_check": "O(n)", "code_cleanliness": [],'
                     ' "interviewer_follow_up": "scale it", "drill_suggestion": "LC 76"}')
    assert isinstance(r, AIReview)
    assert r.interviewer_follow_up == "scale it"


def test_parse_review_repairs_truncated_json():
    r = parse_review('{"correctness_verdict": "solid", "missed_edge_cases": ["empty",')
    assert r.correctness_verdict == "solid"
    assert "empty" in r.missed_edge_cases


def test_parse_review_salvages_extra_fields():
    r = parse_review('{"correctness_verdict": "fine", "bogus_field": 42}')
    assert r.correctness_verdict == "fine"


def test_parse_review_never_loses_content():
    r = parse_review("not json at all, just prose")
    assert "prose" in r.correctness_verdict
