"""OpenRouter post-session coach.

The model list lives in config.json (free models get delisted without notice);
requests use OpenRouter's `models` fallback-routing array. The key comes from
OPENROUTER_API_KEY in .env — never hardcoded, never logged.
"""
import json
import os

import httpx
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config.json")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

load_dotenv(os.path.join(ROOT, ".env"))


class ReviewError(Exception):
    pass


def _config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


REVIEW_SCHEMA_HINT = """Respond with ONLY a JSON object, no markdown fences, shaped:
{
  "correctness_verdict": "short verdict on correctness BEYOND the tests it ran against",
  "missed_edge_cases": ["specific inputs this code would get wrong or that were never exercised"],
  "complexity_check": "claimed vs actual time/space complexity, called out plainly",
  "code_cleanliness": ["concrete notes: naming, structure, idioms, dead code"],
  "interviewer_follow_up": "the follow-up question a real interviewer would ask next, and a hint at the expected adaptation",
  "drill_suggestion": "ONE concrete drill to do next (a specific problem or exercise and why)"
}"""


def build_prompt(statement, code, judge_result, mock_context=None):
    parts = [
        "You are a rigorous coding-interview coach reviewing a candidate's "
        "submission for a Snowflake-style 60-minute live coding round "
        "(Python, communication scored).",
        "## Problem\n" + statement,
        "## Candidate's code\n```python\n" + code + "\n```",
        "## Judge results\n" + json.dumps({
            "verdict": judge_result.get("verdict"),
            "passed": judge_result.get("passed"),
            "total": judge_result.get("total"),
            "failing_cases": [
                {k: c.get(k) for k in ("verdict", "input", "output", "expected", "error")}
                for c in judge_result.get("cases", []) if c.get("verdict") != "AC"
            ][:5],
        }, indent=2),
    ]
    if mock_context:
        parts.append("## Mock-interview context (grade their communication too)\n"
                     + json.dumps(mock_context, indent=2))
    parts.append(REVIEW_SCHEMA_HINT)
    return "\n\n".join(parts)


def review_submission(statement, code, judge_result, mock_context=None):
    """Returns (review_dict, model_used). Raises ReviewError on any failure."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ReviewError("OPENROUTER_API_KEY is not set. Create a .env file "
                          "(see .env.example) with your OpenRouter key.")
    cfg = _config()
    body = {
        "models": cfg["reviewer_models"],
        "temperature": cfg.get("reviewer_temperature", 0.2),
        "messages": [
            {"role": "user",
             "content": build_prompt(statement, code, judge_result, mock_context)},
        ],
    }
    try:
        resp = httpx.post(
            OPENROUTER_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json=body, timeout=120)
    except httpx.HTTPError as e:
        raise ReviewError(f"OpenRouter request failed: {e.__class__.__name__}")
    if resp.status_code == 429:
        raise ReviewError("OpenRouter rate limit hit (free tier: 20 req/min, "
                          "50/day). Try again later — reviews are cached, "
                          "so nothing is lost.")
    if resp.status_code != 200:
        raise ReviewError(f"OpenRouter returned HTTP {resp.status_code}: "
                          f"{resp.text[:300]}")
    data = resp.json()
    try:
        model = data.get("model", "unknown")
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise ReviewError("Unexpected OpenRouter response shape")
    review = parse_review(content)
    return review, model


def parse_review(content):
    """Extract the JSON object from the model output, tolerating fences."""
    text = content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    # fall back to raw text so a flaky model never loses the review
    return {"correctness_verdict": content, "missed_edge_cases": [],
            "complexity_check": "", "code_cleanliness": [],
            "interviewer_follow_up": "", "drill_suggestion": ""}
