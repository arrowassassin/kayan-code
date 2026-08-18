# KayanCode ❄

A complete, local LeetCode-style practice platform purpose-built for
**senior software-engineering interview loops** (60-min live coding · Python ·
no AI assistants · warmup + harder follow-up · communication scored), with a
full study curriculum covering coding, system design, and behavioral rounds.
Fully offline, single user, no accounts.

## Quick start

```bash
pip install -r requirements.txt
uvicorn app:app          # then open http://localhost:8000
```

That's it — the built React UI ships in `frontend/dist`. Optional: create
`.env` from `.env.example` with an OpenRouter key to enable the AI reviewer.

## What's inside

- **~89-problem bank** across the interview-weighted topics (graphs, trees,
  string parsing, heap/top-K, sliding window, two pointer, DP, intervals,
  stream/design), each with an original statement, starter stub, visible +
  hidden test suites, 3 progressive hints, and a 9-part expert editorial
  (pattern recognition → brute force → key insight → derivation → annotated
  solution → spoken complexity → edge-case traps → both DP versions where
  applicable → interviewer follow-up).
- **Real judge**: subprocess runner with 3s/test wall time, memory cap, 10KB
  stdout truncation. *Run* executes the visible, user-editable cases; *Submit*
  adds the hidden suite and records history — exactly the LeetCode loop.
- **Three editor modes**: practice (bracket aids), interview (ALL assists off,
  like CoderPad with assists disabled), whiteboard (Run disabled — submit blind).
- **Any-language solutions**: pick Java/C++/JS/TS/Go/Rust in the editor and
  your code is AI-translated to Python before judging (translation shown with
  the results; needs the OpenRouter key). Mock sessions stay Python-only,
  because the real round is.
- **Mock Interview Mode**: 60-min countdown → clarify gate (2–3 questions
  before the editor unlocks) → approach + complexity gate → coding with
  narration nudges every 8 min → follow-up reveal on AC or at T-25min →
  self-review rubric + AI debrief.
- **AI reviewer** (OpenRouter, free models, config-driven list in
  `config.json`): correctness beyond the tests, missed edge cases, claimed-vs-
  actual complexity, cleanliness, the interviewer's next question, one drill.
  One review per submission, cached in SQLite; in mock mode it only runs after
  the session ends.
- **Phase 2**: spaced repetition (1/3/7-day resurfacing of failed problems),
  per-topic mastery dashboard, daily challenge + streak.

## Development

```bash
# backend tests (judge behavior + bank integrity)
python3 -m pytest tests/ -q

# verify every problem's reference solution passes its own hidden suite
python3 scripts/verify_bank.py

# frontend dev server (proxies /api to :8000)
cd frontend && npm install && npm run dev

# rebuild the production UI into frontend/dist
cd frontend && npm run build
```

Problem authoring conventions live in `AUTHORING_SPEC.md`; the product/
research plan in `PLAN.md`.
