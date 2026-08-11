"""API-level tests, including regressions for the security review findings."""
import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app  # noqa: E402

client = TestClient(app)
SLUG = "0057-insert-interval"
AC_CODE = open(os.path.join(os.path.dirname(__file__), "..", "problems", SLUG,
                            "solution.py")).read()


def test_problems_list():
    r = client.get("/api/problems")
    assert r.status_code == 200
    assert len(r.json()) >= 79


def test_problem_detail_hides_hidden_tests():
    r = client.get(f"/api/problems/{SLUG}")
    body = r.json()
    assert body["hidden_count"] > 0
    assert "hidden" not in body
    assert all("expected" in c for c in body["visible_tests"])


def test_unknown_problem_404():
    assert client.get("/api/problems/nope").status_code == 404


def test_run_and_submit_roundtrip():
    r = client.post("/api/run", json={"slug": SLUG, "code": AC_CODE})
    assert r.status_code == 200 and r.json()["verdict"] == "AC"
    r = client.post("/api/submit", json={"slug": SLUG, "code": AC_CODE})
    body = r.json()
    assert body["verdict"] == "AC" and body["submission_id"] > 0


def test_run_rce_via_input_py_is_neutralized():
    """SECURITY regression: API-supplied cases must never be eval'd."""
    marker = "/tmp/kayan-rce-marker"
    if os.path.exists(marker):
        os.remove(marker)
    evil = {"input_py": f"__import__('pathlib').Path('{marker}').touch()",
            "expected": 1}
    r = client.post("/api/run", json={
        "slug": SLUG, "code": AC_CODE,
        "cases": [{"input": [[], [1, 2]], "expected": [[1, 2]], **evil}]})
    assert r.status_code == 200          # input_py silently stripped
    assert not os.path.exists(marker)    # and never evaluated
    # a case with ONLY input_py (no input array) is rejected outright
    r = client.post("/api/run", json={"slug": SLUG, "code": AC_CODE,
                                      "cases": [evil]})
    assert r.status_code == 422
    assert not os.path.exists(marker)


def test_run_custom_case_count_capped():
    cases = [{"input": [[], [1, 2]], "expected": [[1, 2]]}] * 26
    r = client.post("/api/run", json={"slug": SLUG, "code": AC_CODE,
                                      "cases": cases})
    assert r.status_code == 422


def test_run_malformed_case_rejected():
    r = client.post("/api/run", json={"slug": SLUG, "code": AC_CODE,
                                      "cases": [{"expected": 1}]})
    assert r.status_code == 422


def test_starter_stub_generation():
    r = client.get(f"/api/problems/{SLUG}/starter", params={"language": "java"})
    assert r.status_code == 200
    assert "class Solution" in r.json()["starter"]
    r = client.get(f"/api/problems/{SLUG}/starter", params={"language": "cobol"})
    assert r.status_code == 404


def test_mock_gates():
    sid = client.post("/api/mock/start", json={"slug": SLUG}).json()["id"]
    assert client.post(f"/api/mock/{sid}/clarify",
                       json={"text": "one line only"}).status_code == 422
    ok = client.post(f"/api/mock/{sid}/clarify",
                     json={"text": "empty input?\nbounds?\nduplicates?"})
    assert ok.json()["stage"] == "approach"
    assert client.post(f"/api/mock/{sid}/approach",
                       json={"text": "short"}).status_code == 422
    ok = client.post(f"/api/mock/{sid}/approach", json={
        "text": "Linear scan: copy the before-zone, fold overlaps with "
                "min/max into the new interval, then copy the after-zone.",
        "complexity": "O(n) time O(n) space"})
    assert ok.json()["stage"] == "coding"
    # non-Python submits are rejected inside a mock
    r = client.post("/api/submit", json={"slug": SLUG, "code": "x",
                                         "language": "java",
                                         "mock_session_id": sid})
    assert r.status_code == 409
    done = client.post(f"/api/mock/{sid}/finish", json={"rubric": {"clarified": True}})
    assert done.json()["stage"] == "done"


def test_stats_and_daily():
    assert client.get("/api/stats").status_code == 200
    d = client.get("/api/daily").json()
    assert d["slug"] and d["difficulty"]
