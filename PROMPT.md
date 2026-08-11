# Build prompt for cloud agent

Copy everything below the line into the cloud session (repo: kayan-code — PLAN.md contains the full spec).

---

Build "KayanCode", a complete local LeetCode-style practice platform, exactly per **PLAN.md** in this repo. It preps me for Snowflake's Applied AI Engineer Round 2 "Coding Fundamentals": 60-min live coding, Python, no AI assistants allowed, warmup problem + harder follow-up, communication scored. Read PLAN.md first — it is the source of truth. Summary of what to build:

## Stack & architecture
- FastAPI + SQLite, single process (`uvicorn app:app`, UI at localhost:8000). No auth, single user, fully local.
- Frontend: static HTML/JS with CodeMirror 6 (Python). Two editor modes: **practice** (bracket matching ok) and **interview** (ALL assists off — no autocomplete, no lint, no snippets).
- Judge: subprocess runner (`judge/runner.py`) — generates a harness that imports my solution, runs each test case, compares outputs (type-aware; order-insensitive option for set-like answers). Limits per test: 3s wall time, memory cap via `resource.setrlimit`, 10KB stdout truncation. Two paths like real LeetCode: **Run** (visible, user-editable test case; shows input/your output/expected) and **Submit** (visible + hidden suite; verdict + per-case runtime; recorded in submission history).

## Problem bank (~75 problems — this is the bulk of the work; author ALL of them)
One folder per problem: `problem.md` (statement, examples, constraints), `meta.json` (id, title, difficulty, topics, snowflake_priority 1–3, follow_up_of links), `starter.py`, `tests.json` (visible + hidden cases), `hints.md` (3 progressive hints), `editorial.md`.

**Every editorial follows this exact 9-part structure** (goal: make me a DS/Algo expert, step by step with the WHY):
1. Pattern recognition — what in the statement signals the technique
2. Brute force — code sketch, complexity, exactly why it fails the constraints
3. The key insight — one sentence
4. Step-by-step derivation from brute force to optimal
5. Annotated interview-ready Python solution
6. Time/space complexity with the one-line spoken justification
7. Edge-case traps (what the follow-up question will target)
8. For DP problems: BOTH top-down memoized and bottom-up iterative versions + the mechanical conversion recipe
9. Likely interviewer follow-up and how to adapt

Problem list (use exactly this set; ★ = highest priority, Snowflake-reported or named in my prep guide):
- Graph BFS/DFS: 200, 994, 207, 210, 133, 417, 127, 323, 1091, 130, 261
- Trees: **545 ★**, 199, 102, 103, 543, 236, 98, 297, 437, 987
- String parsing (edge-case heavy): **2062 ★**, 125, 151, 71, 394, 227, 49, 819, 937, 165, 443, 68, 65
- Top-K/Heap: 215 (heap AND quickselect), 347, 692, 973, 23, 295, 621, 767
- Sliding window: 3, 76, 424, 567, 239, 904, 992, 209
- Two pointer: 15, 11, 42, 75, 80, 680, 167
- DP (both versions each): 198, 322, 300, 139, 62, 1143, 72, 416, 91, 5, **1235 ★**
- Intervals: **57 ★**, 56, 435, 253, 759
- Stream/design: 146, 346, 362, 359, 703, 380
Write original problem statements in your own words (do not copy LeetCode text verbatim). Pre-link warmup→extension pairs in meta.json (56→57→759; 3→76; 198→1235; 102→103; 215→347; etc.).

## Mock Interview Mode (mirror the real round)
60-min countdown → **clarify gate** (must type 2–3 clarifying questions before editor unlocks) → **approach gate** (approach paragraph + stated time/space complexity) → coding in interview-mode editor with a narration nudge every ~8 min → on submit-pass or at T-25min, reveal the linked harder follow-up → debrief: self-review rubric (clarified? complexity stated? clean code? edges tested?) + AI review + logged to history.

## AI Reviewer (OpenRouter)
- POST https://openrouter.ai/api/v1/chat/completions, `Authorization: Bearer $OPENROUTER_API_KEY` from `.env` (gitignored; NEVER hardcode or log the key; create `.env.example`).
- Body uses fallback routing: `"models": ["nvidia/nemotron-3-ultra-550b-a55b:free", "openai/gpt-oss-20b:free"]`, temperature 0.2.
- Model list must live in config (free models get delisted).
- Input: problem statement + my code + judge results (+ in mock mode: my clarifying questions and approach text).
- Output (render structured): correctness verdict beyond the tests · missed edge cases · claimed-vs-actual complexity · code cleanliness · "the follow-up an interviewer would ask" · one concrete drill.
- One review per submission, cached in SQLite (free tier: 20 req/min, 50/day). In mock mode the reviewer runs ONLY after the session ends.

## Phase 2 (build after MVP works end-to-end)
Spaced repetition (failed/shaky problems resurface 1/3/7 days), per-topic stats dashboard, whiteboard mode (Run disabled), daily challenge.

## Build order & acceptance
1. Scaffold + judge + 3 pilot problems end-to-end (run/submit/history working)
2. Full 75-problem bank, topic-by-topic (graphs first, then trees, strings, heap, window, two-pointer, DP, intervals, design)
3. Mock mode 4. AI reviewer 5. Phase 2
Write tests for the judge (correct/wrong/TLE/crash/exception in user code) and for tests.json integrity (every problem's reference solution in editorial must pass its own hidden suite — verify this programmatically for ALL problems). Done = `uvicorn app:app` serves the full flow: browse bank → solve → run → submit → history → mock session → AI review.
