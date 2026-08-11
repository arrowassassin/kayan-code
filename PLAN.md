# KayanCode — Personal LeetCode Clone for Snowflake Round 2 Prep

Target: **Snowflake Applied AI Engineer — Interview 2 "Coding Fundamentals"**
(60 min · remote · live coding · Python · **no AI assistants allowed** · warmup problem + harder follow-up · communication evaluated throughout)

Grounded in: the two prep PDFs in this repo + a 105-agent deep-research pass (23 sources fetched, 25 claims adversarially verified, 6 killed).

---

## 1. What the research established (verified)

- **Core LeetCode loop to clone:** two execution paths — *Run* (visible, user-editable test case; shows input / your output / expected) and *Submit* (hidden test suite under time/memory limits, recorded in submission history with pass/fail + runtime). [LeetCode help docs, 3-0]
- **Judge architecture:** for a single-user local app, a Python **subprocess judge** with wall-time (~3s), memory, output-truncation, and process caps is legitimate and sufficient — sandbox escape is a non-threat when all code is your own. Judge0/Piston (Dockerized, Isolate sandbox) are the Phase-2 upgrade if ever needed. [judge0/piston primary sources, 3-0 ×6]
- **Snowflake coding-round reality:** 60-min shared editor (CoderPad reported), difficulty reported *harder than typical FAANG*; heaviest topics: **DP, BFS/DFS, trees, strings/character analysis, binary search, hash tables, intervals, stream processing**; prompts start straightforward and escalate through follow-ups. Verifiably attributed recent questions: **Maximum Profit in Job Scheduling (LC 1235), Insert Interval (LC 57), stream-processing class design, duplicate-character checks**. [medium confidence — prep-site + forum sources]
- **Communication is scored:** candidates fail by solving the wrong problem. Mock mode must enforce **clarify → state approach + complexity → code while narrating → test edge cases**. [3-0]
- **Killed claims** (do not build on): LeetCode's 4-tab layout, its editor stack (Monaco vs CodeMirror unverified either way), "2-hour phone screen", "database-internals twist", "must be microservices".

## 2. Architecture (MVP)

```
kayan-code/
├── app.py                  # FastAPI app (single process, serves API + static UI)
├── judge/
│   └── runner.py           # subprocess judge: 3s wall-time, memory cap (resource.setrlimit),
│                           #   stdout truncation, per-test verdict + runtime
├── problems/               # one folder per problem (self-contained, git-friendly)
│   └── 0545-boundary-of-binary-tree/
│       ├── problem.md      # statement, examples, constraints
│       ├── meta.json       # id, title, difficulty, topics, snowflake_priority (1-3),
│       │                   #   companies, follow_up_of (links warmup→extension pairs)
│       ├── starter.py      # function signature / class stub
│       ├── tests.json      # visible cases (editable in UI) + hidden cases
│       ├── hints.md        # 3 progressive hints (revealed one at a time)
│       └── editorial.md    # THE EXPERT TRACK — see §3
├── reviewer/
│   └── ai_review.py        # OpenRouter client — see §5
├── db.sqlite               # submissions, sessions, per-problem mastery state
├── static/                 # UI: problem list, workspace, mock mode, dashboard
└── .env                    # OPENROUTER_API_KEY (user-created, gitignored)
```

- **Backend:** FastAPI + SQLite. One process, `uvicorn app:app`, open `localhost:8000`.
- **Editor:** CodeMirror 6, Python mode. **Interview mode = autocomplete/lint/snippets OFF** (plain editor, like CoderPad with assists disabled). Practice mode may keep basic bracket matching.
- **Judge:** `subprocess.run` of a generated harness: imports user code, feeds each test case, compares against expected with type-aware comparison (order-insensitive option for set-like answers), reports per-case verdict + wall time. Limits mirror Piston's categories: 3s/test, memory cap, 10KB stdout cap.

## 3. Problem bank — full editorial format (the "make me an expert" part)

Every problem's `editorial.md` follows this fixed structure:

1. **Pattern recognition** — what in the statement signals the pattern ("k-th largest → heap or quickselect", "contiguous subarray + constraint → sliding window").
2. **Brute force first** — the naive solution, its complexity, and *exactly why* it's too slow for the constraints.
3. **The key insight** — the single observation that unlocks the optimal approach, stated in one sentence before any code.
4. **Step-by-step derivation** — brute force → optimal in explicit steps, each step answering *why*.
5. **Annotated Python solution** — clean, interview-ready, commented at decision points only.
6. **Complexity** — time + space, with the one-line justification you'd say out loud.
7. **Edge-case traps** — the specific inputs the follow-up question will target (empty input, single element, duplicates, punctuation/unicode, overflow, skewed tree…).
8. **DP problems additionally get both versions:** top-down memoized *and* bottom-up iterative, with the mechanical conversion recipe (the prep guide explicitly names this skill).
9. **Interviewer follow-up** — the likely extension and a sketch of how to adapt.

### Curated bank (~75 problems, Medium–Hard, Python) — `snowflake_priority: 1` = verified/reported, 2 = named in prep PDF topics, 3 = pattern support

| Topic | Problems |
|---|---|
| **Graph BFS/DFS** | Number of Islands 200 · Rotting Oranges 994 · Course Schedule 207 (+ II 210) · Clone Graph 133 · Pacific Atlantic 417 · Word Ladder 127 · Connected Components 323 · Shortest Path in Binary Matrix 1091 · Surrounded Regions 130 · Graph Valid Tree 261 |
| **Trees** | **Boundary of Binary Tree 545** ★ · Right Side View 199 · Level Order 102 · Zigzag 103 · Diameter 543 · LCA 236 · Validate BST 98 · Serialize/Deserialize 297 · Path Sum III 437 · Vertical Order Traversal 987 |
| **String parsing (edge-case heavy)** | **Count Vowel Substrings 2062** ★ · Valid Palindrome 125 · Reverse Words 151 · Simplify Path 71 · Decode String 394 · Basic Calculator II 227 · Group Anagrams 49 · Most Common Word 819 (punctuation!) · Reorder Log Files 937 · Compare Version Numbers 165 · String Compression 443 · Text Justification 68 · Valid Number 65 |
| **Top-K / Heap** | Kth Largest 215 (heap **and** quickselect) · Top K Frequent Elements 347 · Top K Frequent Words 692 · K Closest Points 973 · Merge K Sorted Lists 23 · Median from Data Stream 295 · Task Scheduler 621 · Reorganize String 767 |
| **Sliding window** | Longest Substring w/o Repeating 3 · **Minimum Window Substring 76** · Character Replacement 424 · Permutation in String 567 · Max Sliding Window 239 · Fruit Into Baskets 904 · Subarrays with K Distinct 992 · Min Size Subarray Sum 209 |
| **Two pointer** | 3Sum 15 · Container With Most Water 11 · Trapping Rain Water 42 · Sort Colors 75 · Remove Duplicates II 80 · Valid Palindrome II 680 · Two Sum II 167 |
| **DP (both versions each)** | House Robber 198 · Coin Change 322 · LIS 300 · Word Break 139 · Unique Paths 62 · LCS 1143 · Edit Distance 72 · Partition Equal Subset Sum 416 · Decode Ways 91 · Longest Palindromic Substring 5 · **Maximum Profit in Job Scheduling 1235** ★ (Snowflake-reported) |
| **Intervals** (Snowflake-reported) | **Insert Interval 57** ★ · Merge Intervals 56 · Non-overlapping Intervals 435 · Meeting Rooms II 253 · Employee Free Time 759 |
| **Stream / design** (Snowflake-reported pattern) | LRU Cache 146 · Moving Average 346 · Hit Counter 362 · Logger Rate Limiter 359 · Kth Largest in Stream 703 · Insert Delete GetRandom 380 |

★ = explicitly named in the prep PDF or verifiably reported at Snowflake.

Warmup→extension pairs are pre-linked in `meta.json` (e.g., Merge Intervals → Insert Interval → Employee Free Time; LC 3 → LC 76; House Robber → Job Scheduling 1235).

## 4. Mock Interview Mode (mirrors the real round exactly)

1. **Session start:** 60-minute countdown. Picks a warmup (Medium) + hidden harder extension from a linked pair, weighted toward `snowflake_priority` and your weak topics.
2. **Clarify gate (before editor unlocks):** you must write 2–3 clarifying questions (input bounds? empty input? duplicates? punctuation/case?) — mirrors PDF step 1.
3. **Approach gate:** one-paragraph approach + stated time/space complexity before coding — mirrors PDF step 2.
4. **Coding:** plain editor, **no autocomplete**, narration nudge every ~8 min ("say out loud what this block does").
5. **Follow-up reveal:** on submit-pass (or at T-25min), the harder extension appears — matching the reported "starts straightforward, escalates" pattern.
6. **Debrief:** self-review rubric (clarified? stated complexity? clean code? tested edges?) + **AI reviewer report** (§5) + result logged to history.

## 5. AI Reviewer (OpenRouter) — post-session coach

- **Default model:** `nvidia/nemotron-3-ultra-550b-a55b:free` (strongest free reasoning model, 1M ctx). **Fallback:** `openai/gpt-oss-20b:free` (fast, structured JSON output). Sent as OpenRouter `models: [default, fallback]` array for automatic failover.
- **Free-tier budget:** 20 req/min, 50 req/day (1,000/day if you've ever bought $10 credits) → **one review per submission**, cached in SQLite, never auto-fired on keystrokes.
- **Key handling:** `OPENROUTER_API_KEY` read from `.env` (gitignored). You create the file yourself; the key is never hardcoded or logged.
- **Review request:** problem statement + your code + judge results + (in mock mode) your clarifying questions and approach text.
- **Structured review output:** verdict on correctness beyond the tests · missed edge cases · complexity check (claimed vs actual) · code-cleanliness notes · "the follow-up an interviewer would ask" · one concrete drill suggestion.
- **Timing rule:** in mock mode the reviewer only runs **after** the session ends — practice conditions stay AI-free, like the real round.

## 6. Phase 2 (after MVP works)

- Spaced-repetition queue (failed/shaky problems resurface at 1/3/7-day intervals)
- Stats dashboard (per-topic mastery, solve times vs 25-min target per medium)
- "Whiteboard mode" (run disabled — some Snowflake interviewers disable execution in CoderPad; open research question)
- Judge0/Piston Docker judge if multi-language ever wanted
- Daily challenge + streak

## 7. Build order

1. Scaffold FastAPI + SQLite + static UI shell
2. Subprocess judge + 3 pilot problems end-to-end (run/submit/history)
3. Full problem bank authoring (75 problems: statements, tests, hints, editorials) — the bulk of the work, done topic-by-topic so you can start practicing graphs while DP is still being authored
4. Mock interview mode (timer, gates, pair reveal, rubric)
5. AI reviewer integration + review cache
6. Polish: dashboard, spaced repetition

## Caveats (honest)

- Snowflake findings come from prep sites + anonymous reports, none specific to the Applied AI track; the 60-min live-coding format is consistent, but the exact question pool for *this* track is unverified.
- Whether the real round lets you execute code in the shared editor is unknown — practice both with and without Run.
- Free OpenRouter models can be delisted without notice; the model list is config, not code.
