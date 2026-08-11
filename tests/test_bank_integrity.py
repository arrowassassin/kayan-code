"""Every problem in the bank passes the full integrity check, including
'the reference solution gets AC on its own hidden suite via the real judge'."""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import verify_bank  # noqa: E402

PROBLEMS = os.path.join(ROOT, "problems")
SLUGS = sorted(d for d in os.listdir(PROBLEMS)
               if os.path.isdir(os.path.join(PROBLEMS, d)))


@pytest.mark.parametrize("slug", SLUGS)
def test_problem_integrity(slug):
    errors = verify_bank.check_problem(slug, set(SLUGS))
    assert not errors, f"{slug}: " + "; ".join(errors)
