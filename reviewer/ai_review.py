"""OpenRouter client: post-session coach + any-language → Python transpiler.

- Model list lives in config.json (free models get delisted); requests use
  OpenRouter's `models` fallback-routing array.
- Review JSON is requested via structured outputs (response_format
  json_schema); parsing falls back to json-repair, and the result is
  validated with pydantic — no hand-rolled scraping.
- Code extraction from transpile replies uses markdown-it-py's fence tokens.
- OPENROUTER_API_KEY comes from .env (gitignored) — never hardcoded/logged.
"""
import json
import os

import httpx
import json_repair
from dotenv import load_dotenv
from markdown_it import MarkdownIt
from pydantic import BaseModel, Field, ValidationError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "config.json")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

load_dotenv(os.path.join(ROOT, ".env"))

_md = MarkdownIt()


class ReviewError(Exception):
    pass


class AIReview(BaseModel):
    correctness_verdict: str = ""
    missed_edge_cases: list[str] = Field(default_factory=list)
    complexity_check: str = ""
    code_cleanliness: list[str] = Field(default_factory=list)
    interviewer_follow_up: str = ""
    drill_suggestion: str = ""


REVIEW_JSON_SCHEMA = {
    "name": "interview_review",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "required": list(AIReview.model_fields),
        "properties": {
            "correctness_verdict": {
                "type": "string",
                "description": "Verdict on correctness BEYOND the tests it ran against",
            },
            "missed_edge_cases": {
                "type": "array", "items": {"type": "string"},
                "description": "Specific inputs this code would get wrong or never exercised",
            },
            "complexity_check": {
                "type": "string",
                "description": "Claimed vs actual time/space complexity, called out plainly",
            },
            "code_cleanliness": {
                "type": "array", "items": {"type": "string"},
                "description": "Concrete notes: naming, structure, idioms, dead code",
            },
            "interviewer_follow_up": {
                "type": "string",
                "description": "The follow-up a real interviewer would ask next + expected adaptation",
            },
            "drill_suggestion": {
                "type": "string",
                "description": "ONE concrete drill to do next and why",
            },
        },
    },
}


def _config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def _chat(messages, temperature, response_format=None):
    """One OpenRouter call with model-array failover. Returns (content, model).
    If the routed model rejects response_format, retries without it."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ReviewError("OPENROUTER_API_KEY is not set. Create a .env file "
                          "(see .env.example) with your OpenRouter key.")
    cfg = _config()
    body = {"models": cfg["reviewer_models"], "temperature": temperature,
            "messages": messages}
    if response_format:
        body["response_format"] = response_format
    for attempt in (1, 2):
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
                              "50/day). Try again later — nothing is lost, "
                              "results are cached.")
        if resp.status_code == 200:
            data = resp.json()
            try:
                return (data["choices"][0]["message"]["content"],
                        data.get("model", "unknown"))
            except (KeyError, IndexError):
                raise ReviewError("Unexpected OpenRouter response shape")
        # some free models reject structured outputs — drop it and retry once
        if response_format and attempt == 1 and 400 <= resp.status_code < 500:
            body.pop("response_format", None)
            continue
        raise ReviewError(f"OpenRouter returned HTTP {resp.status_code}: "
                          f"{resp.text[:300]}")
    raise ReviewError("OpenRouter request failed")


# ------------------------------------------------------------------ review

def build_review_prompt(statement, code, judge_result, mock_context=None):
    parts = [
        "You are a rigorous coding-interview coach reviewing a candidate's "
        "submission for a senior-level 60-minute live coding round "
        "(Python, communication scored). Respond with the requested JSON "
        "object only.",
        "## Problem\n" + statement,
        "## Candidate's code\n```\n" + code + "\n```",
        "## Judge results\n" + json.dumps({
            "verdict": judge_result.get("verdict"),
            "passed": judge_result.get("passed"),
            "total": judge_result.get("total"),
            "failing_cases": [
                {k: c.get(k) for k in ("verdict", "input", "output", "expected", "error")}
                for c in judge_result.get("cases", []) if c.get("verdict") != "AC"
            ][:5],
        }, indent=2, default=str),
    ]
    if mock_context:
        parts.append("## Mock-interview context (grade their communication too)\n"
                     + json.dumps(mock_context, indent=2))
    return "\n\n".join(parts)


def review_submission(statement, code, judge_result, mock_context=None):
    """Returns (review_dict, model_used). Raises ReviewError on failure."""
    content, model = _chat(
        [{"role": "user",
          "content": build_review_prompt(statement, code, judge_result, mock_context)}],
        temperature=_config().get("reviewer_temperature", 0.2),
        response_format={"type": "json_schema", "json_schema": REVIEW_JSON_SCHEMA},
    )
    return parse_review(content).model_dump(), model


def parse_review(content) -> AIReview:
    """Strict JSON → json-repair fallback → pydantic validation."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = json_repair.loads(content)
    if isinstance(data, dict):
        try:
            return AIReview.model_validate(data)
        except ValidationError:
            # salvage the fields that do fit
            cleaned = {k: v for k, v in data.items() if k in AIReview.model_fields}
            try:
                return AIReview.model_validate(cleaned)
            except ValidationError:
                pass
    # last resort: keep the raw text so a flaky model never loses the review
    return AIReview(correctness_verdict=str(content))


# --------------------------------------------------------------- transpile

def transpile_to_python(code, language, starter, entry):
    """Translate a solution written in another language into judge-ready
    Python 3. Returns (python_code, model_used). Raises ReviewError."""
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise ReviewError("Multi-language mode needs the AI translator: set "
                          "OPENROUTER_API_KEY in .env (see .env.example), or "
                          "switch the language back to Python.")
    prompt = "\n\n".join([
        f"Translate this {language} solution into Python 3 for an automated "
        "judge. Rules:\n"
        "- Preserve the algorithm, semantics and complexity EXACTLY — do not "
        "fix bugs, do not optimize, do not add features. If the code has a "
        "bug, the Python must reproduce the same bug.\n"
        "- Match this Python entry-point shape exactly (same class and "
        "method/constructor names, same parameter order):\n"
        f"```python\n{starter}\n```\n"
        f"- The judge instantiates and calls `{entry}`.\n"
        "- TreeNode/ListNode/Node classes are predefined by the judge — "
        "reference them without defining or importing them.\n"
        "- Use only the Python standard library.\n"
        "- Reply with a single fenced python code block and nothing else.",
        f"```{language}\n{code}\n```",
    ])
    content, model = _chat([{"role": "user", "content": prompt}], temperature=0.0)
    python_code = extract_code(content)
    if not python_code.strip():
        raise ReviewError("The translator returned no code — try again or "
                          "switch to Python.")
    return python_code, model


def extract_code(content):
    """First fenced code block via markdown-it tokens; else the raw text."""
    fences = [t for t in _md.parse(content) if t.type == "fence"]
    if fences:
        preferred = [t for t in fences
                     if (t.info or "").strip().lower() in ("python", "python3", "py")]
        return (preferred[0] if preferred else fences[0]).content
    return content.strip() + "\n"
