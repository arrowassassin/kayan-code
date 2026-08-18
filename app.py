"""KayanCode — local LeetCode-style practice platform.

Run:  uvicorn app:app          then open http://localhost:8000
"""
import hashlib
import json
import os
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import stubgen
from judge import runner
from reviewer import ai_review

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(ROOT, "problems")
DB_PATH = os.path.join(ROOT, "db.sqlite")
SRS_INTERVALS_DAYS = [1, 3, 7]

app = FastAPI(title="KayanCode")


# ---------------------------------------------------------------- database

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    return conn


def init_db():
    with db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT NOT NULL,
            code TEXT NOT NULL,
            verdict TEXT NOT NULL,
            passed INTEGER NOT NULL,
            total INTEGER NOT NULL,
            runtime_ms REAL,
            mode TEXT NOT NULL DEFAULT 'practice',
            mock_session_id TEXT,
            result_json TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reviews (
            submission_id INTEGER PRIMARY KEY,
            model TEXT,
            content TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS mock_sessions (
            id TEXT PRIMARY KEY,
            warmup_slug TEXT NOT NULL,
            followup_slug TEXT,
            stage TEXT NOT NULL DEFAULT 'clarify',
            clarify_text TEXT,
            approach_text TEXT,
            complexity_text TEXT,
            followup_revealed INTEGER NOT NULL DEFAULT 0,
            started_at TEXT NOT NULL,
            ends_at TEXT NOT NULL,
            finished_at TEXT,
            rubric_json TEXT
        );
        CREATE TABLE IF NOT EXISTS srs (
            slug TEXT PRIMARY KEY,
            due_at TEXT NOT NULL,
            interval_idx INTEGER NOT NULL DEFAULT 0,
            last_result TEXT,
            updated_at TEXT NOT NULL
        );
        """)
        # additive migrations for multi-language submissions
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(submissions)")}
        if "language" not in cols:
            conn.execute("ALTER TABLE submissions ADD COLUMN language TEXT"
                         " NOT NULL DEFAULT 'python'")
        if "transpiled_code" not in cols:
            conn.execute("ALTER TABLE submissions ADD COLUMN transpiled_code TEXT")
        if "elapsed_s" not in cols:
            # seconds from first keystroke to this submission (client-tracked)
            conn.execute("ALTER TABLE submissions ADD COLUMN elapsed_s INTEGER")


init_db()


def now():
    return datetime.now(timezone.utc)


def iso(dt):
    return dt.isoformat(timespec="seconds")


# ---------------------------------------------------------------- problem bank

def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


_bank_cache = {"stamp": None, "bank": {}}


def load_bank():
    """Bank metadata, cached against the problems dir's mtime signature so we
    don't re-parse 79 meta.json files on every request."""
    if not os.path.isdir(PROBLEMS_DIR):
        return {}
    names = os.listdir(PROBLEMS_DIR)
    metas = [os.path.join(PROBLEMS_DIR, n, "meta.json") for n in names]
    stamp = (len(names),
             max((os.path.getmtime(m) for m in metas if os.path.exists(m)),
                 default=0))
    if _bank_cache["stamp"] == stamp:
        return _bank_cache["bank"]
    bank = _scan_bank()
    _bank_cache.update(stamp=stamp, bank=bank)
    return bank


def _scan_bank():
    bank = {}
    for name in sorted(os.listdir(PROBLEMS_DIR)):
        pdir = os.path.join(PROBLEMS_DIR, name)
        meta_path = os.path.join(pdir, "meta.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            meta = json.loads(_read(meta_path))
        except json.JSONDecodeError:
            continue
        meta["slug"] = name
        meta["dir"] = pdir
        bank[name] = meta
    return bank


def get_problem_meta(slug):
    bank = load_bank()
    if slug not in bank:
        raise HTTPException(404, f"Unknown problem: {slug}")
    return dict(bank[slug])  # copy: callers mutate (pop "dir") freely


# ---------------------------------------------------------------- API: bank

@app.get("/api/problems")
def list_problems():
    bank = load_bank()
    with db() as conn:
        rows = conn.execute(
            "SELECT slug, MAX(verdict='AC') AS solved, COUNT(*) AS attempts,"
            " MAX(created_at) AS last_submitted_at,"
            " MIN(CASE WHEN verdict='AC' THEN elapsed_s END) AS solve_seconds "
            "FROM submissions GROUP BY slug").fetchall()
        state = {r["slug"]: r for r in rows}
        due_rows = conn.execute(
            "SELECT slug FROM srs WHERE due_at <= ?", (iso(now()),)).fetchall()
        due = {r["slug"] for r in due_rows}
    out = []
    for slug, meta in bank.items():
        s = state.get(slug)
        out.append({
            "slug": slug,
            "id": meta.get("id"),
            "title": meta.get("title"),
            "difficulty": meta.get("difficulty"),
            "topics": meta.get("topics", []),
            "priority": meta.get("priority", 3),
            "follow_up_of": meta.get("follow_up_of"),
            "follow_up": meta.get("follow_up"),
            "solved": bool(s and s["solved"]),
            "attempted": bool(s),
            "attempts": s["attempts"] if s else 0,
            "last_submitted_at": s["last_submitted_at"] if s else None,
            "solve_seconds": s["solve_seconds"] if s else None,
            "due_for_review": slug in due,
        })
    out.sort(key=lambda p: (p["priority"], p["id"] or 0))
    return out


@app.get("/api/problems/{slug}")
def get_problem(slug: str):
    meta = get_problem_meta(slug)
    pdir = meta.pop("dir")
    tests = json.loads(_read(os.path.join(pdir, "tests.json")))
    hints = []
    hints_path = os.path.join(pdir, "hints.md")
    if os.path.exists(hints_path):
        # hints.md: sections split by lines starting with '## '
        cur = []
        for line in _read(hints_path).splitlines():
            if line.startswith("## "):
                if cur:
                    hints.append("\n".join(cur).strip())
                cur = []
            else:
                cur.append(line)
        if cur:
            hints.append("\n".join(cur).strip())
        hints = [h for h in hints if h]
    return {
        **meta,
        "statement": _read(os.path.join(pdir, "problem.md")),
        "starter": _read(os.path.join(pdir, "starter.py")),
        "visible_tests": tests.get("visible", []),
        "hidden_count": len(tests.get("hidden", [])),
        "hints": hints,
    }


@app.get("/api/problems/{slug}/starter")
def get_starter(slug: str, language: str = "python"):
    meta = get_problem_meta(slug)
    source = _read(os.path.join(meta["dir"], "starter.py"))
    if language.lower() in ("python", "python3", "py"):
        return {"language": "python", "starter": source}
    generated = stubgen.generate(source, language.lower())
    if generated is None:
        raise HTTPException(404, f"No starter template for language: {language}")
    return {"language": language.lower(), "starter": generated}


@app.get("/api/problems/{slug}/editorial")
def get_editorial(slug: str):
    meta = get_problem_meta(slug)
    path = os.path.join(meta["dir"], "editorial.md")
    if not os.path.exists(path):
        raise HTTPException(404, "No editorial yet")
    return {"editorial": _read(path)}


# ---------------------------------------------------------------- API: judge

class RunRequest(BaseModel):
    slug: str
    code: str
    language: str = "python"
    cases: list | None = None  # user-edited visible cases


class SubmitRequest(BaseModel):
    slug: str
    code: str
    language: str = "python"
    mode: str = "practice"          # practice | interview | whiteboard | mock
    mock_session_id: str | None = None
    elapsed_s: int | None = None    # first-keystroke -> submit, client-tracked


def resolve_python_code(meta, code, language):
    """Non-Python solutions are AI-transpiled to judge-ready Python.
    Returns (python_code, transpiled_or_None)."""
    if language.lower() in ("python", "python3", "py"):
        return code, None
    pdir = meta["dir"]
    starter = _read(os.path.join(pdir, "starter.py"))
    try:
        python_code, _model = ai_review.transpile_to_python(
            code, language, starter, meta["judge"]["entry"])
    except ai_review.ReviewError as e:
        raise HTTPException(502, str(e))
    return python_code, python_code


@app.post("/api/run")
def run_code(req: RunRequest):
    meta = get_problem_meta(req.slug)
    code, transpiled = resolve_python_code(meta, req.code, req.language)
    custom = req.cases if req.cases else None
    try:
        result = runner.judge_submission(meta["dir"], code,
                                         include_hidden=False, custom_cases=custom)
    except ValueError as e:  # malformed/oversized custom cases
        raise HTTPException(422, str(e))
    if transpiled:
        result["transpiled_code"] = transpiled
    return result


@app.post("/api/submit")
def submit_code(req: SubmitRequest):
    meta = get_problem_meta(req.slug)
    if req.mock_session_id and req.language.lower() not in ("python", "python3", "py"):
        raise HTTPException(409, "Mock sessions are Python-only — the real "
                                 "round is Python, and mock mode enforces "
                                 "real conditions (no AI translation).")
    code, transpiled = resolve_python_code(meta, req.code, req.language)
    result = runner.judge_submission(meta["dir"], code, include_hidden=True)
    if result["status"] != "ok":
        if transpiled:
            result["transpiled_code"] = transpiled
        return result
    with db() as conn:
        cur = conn.execute(
            "INSERT INTO submissions (slug, code, verdict, passed, total, runtime_ms,"
            " mode, mock_session_id, result_json, created_at, language,"
            " transpiled_code, elapsed_s)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (req.slug, req.code, result["verdict"], result["passed"], result["total"],
             result["runtime_ms"], req.mode, req.mock_session_id,
             json.dumps(result), iso(now()), req.language.lower(), transpiled,
             req.elapsed_s))
        result["submission_id"] = cur.lastrowid
    if transpiled:
        result["transpiled_code"] = transpiled
    update_srs(req.slug, result["verdict"] == "AC")
    if req.mock_session_id and result["verdict"] == "AC":
        maybe_reveal_followup(req.mock_session_id, req.slug)
    return result


def update_srs(slug, passed):
    """Failed/shaky problems resurface at 1/3/7-day intervals."""
    with db() as conn:
        row = conn.execute("SELECT * FROM srs WHERE slug=?", (slug,)).fetchone()
        if not passed:
            due = now() + timedelta(days=SRS_INTERVALS_DAYS[0])
            conn.execute(
                "INSERT INTO srs (slug, due_at, interval_idx, last_result, updated_at)"
                " VALUES (?,?,0,'fail',?)"
                " ON CONFLICT(slug) DO UPDATE SET due_at=?, interval_idx=0,"
                " last_result='fail', updated_at=?",
                (slug, iso(due), iso(now()), iso(due), iso(now())))
        elif row:
            idx = min(row["interval_idx"] + 1, len(SRS_INTERVALS_DAYS) - 1)
            if row["interval_idx"] >= len(SRS_INTERVALS_DAYS) - 1:
                conn.execute("DELETE FROM srs WHERE slug=?", (slug,))  # graduated
            else:
                due = now() + timedelta(days=SRS_INTERVALS_DAYS[idx])
                conn.execute(
                    "UPDATE srs SET due_at=?, interval_idx=?, last_result='pass',"
                    " updated_at=? WHERE slug=?",
                    (iso(due), idx, iso(now()), slug))


@app.get("/api/submissions")
def list_submissions(slug: str | None = None, limit: int = 50):
    q = ("SELECT id, slug, verdict, passed, total, runtime_ms, mode, language,"
         " mock_session_id, created_at FROM submissions")
    args = []
    if slug:
        q += " WHERE slug=?"
        args.append(slug)
    q += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    with db() as conn:
        rows = conn.execute(q, args).fetchall()
        review_ids = {r["submission_id"] for r in
                      conn.execute("SELECT submission_id FROM reviews").fetchall()}
    return [{**dict(r), "has_review": r["id"] in review_ids} for r in rows]


@app.get("/api/submissions/{sid}")
def get_submission(sid: int):
    with db() as conn:
        row = conn.execute("SELECT * FROM submissions WHERE id=?", (sid,)).fetchone()
    if not row:
        raise HTTPException(404, "No such submission")
    out = dict(row)
    out["result"] = json.loads(out.pop("result_json") or "{}")
    return out


# ---------------------------------------------------------------- API: mock mode

class MockStartRequest(BaseModel):
    slug: str | None = None   # explicit warmup pick, else weighted random


class MockTextRequest(BaseModel):
    text: str
    complexity: str | None = None


MOCK_MINUTES = 60
FOLLOWUP_REVEAL_AT_REMAINING_MIN = 25


def pick_mock_pair(bank, explicit_slug=None):
    """Pick a warmup that has a linked follow-up, weighted by priority and
    weakness (unsolved/failed problems weigh more)."""
    pairs = [(slug, m["follow_up"]) for slug, m in bank.items()
             if m.get("follow_up") and m["follow_up"] in bank]
    if explicit_slug:
        if explicit_slug not in bank:
            raise HTTPException(404, "Unknown problem")
        fu = bank[explicit_slug].get("follow_up")
        return explicit_slug, fu if fu in bank else None
    if not pairs:
        raise HTTPException(500, "No linked warmup/follow-up pairs in the bank")
    with db() as conn:
        solved = {r["slug"] for r in conn.execute(
            "SELECT DISTINCT slug FROM submissions WHERE verdict='AC'").fetchall()}
    seed = uuid.uuid4().int
    weights = []
    for slug, fu in pairs:
        w = {1: 9, 2: 4, 3: 1}.get(bank[slug].get("priority", 3), 1)
        if slug not in solved:
            w *= 3
        weights.append(w)
    total = sum(weights)
    r = seed % total
    for (slug, fu), w in zip(pairs, weights):
        if r < w:
            return slug, fu
        r -= w
    return pairs[0]


@app.post("/api/mock/start")
def mock_start(req: MockStartRequest):
    bank = load_bank()
    warmup, followup = pick_mock_pair(bank, req.slug)
    sid = uuid.uuid4().hex[:12]
    start = now()
    with db() as conn:
        conn.execute(
            "INSERT INTO mock_sessions (id, warmup_slug, followup_slug, stage,"
            " started_at, ends_at) VALUES (?,?,?,?,?,?)",
            (sid, warmup, followup, "clarify", iso(start),
             iso(start + timedelta(minutes=MOCK_MINUTES))))
    return mock_state(sid)


def _mock(sid):
    with db() as conn:
        row = conn.execute("SELECT * FROM mock_sessions WHERE id=?", (sid,)).fetchone()
    if not row:
        raise HTTPException(404, "No such mock session")
    return dict(row)


@app.get("/api/mock/{sid}")
def mock_state(sid: str):
    m = _mock(sid)
    remaining = (datetime.fromisoformat(m["ends_at"]) - now()).total_seconds()
    m["remaining_seconds"] = max(0, int(remaining))
    # auto-reveal follow-up at T-25min
    if (not m["followup_revealed"] and m["followup_slug"]
            and m["stage"] == "coding"
            and remaining <= FOLLOWUP_REVEAL_AT_REMAINING_MIN * 60):
        with db() as conn:
            conn.execute("UPDATE mock_sessions SET followup_revealed=1 WHERE id=?", (sid,))
        m["followup_revealed"] = 1
    if not m["followup_revealed"]:
        m.pop("followup_slug")  # keep the harder extension hidden
    return m


@app.post("/api/mock/{sid}/clarify")
def mock_clarify(sid: str, req: MockTextRequest):
    m = _mock(sid)
    if m["stage"] != "clarify":
        raise HTTPException(400, "Clarify gate already passed")
    questions = [q.strip() for q in req.text.strip().splitlines() if q.strip()]
    if len(questions) < 2:
        raise HTTPException(422, "Write at least 2 clarifying questions "
                                 "(input bounds? empties? duplicates? case/punctuation?)")
    with db() as conn:
        conn.execute("UPDATE mock_sessions SET clarify_text=?, stage='approach'"
                     " WHERE id=?", (req.text, sid))
    return mock_state(sid)


@app.post("/api/mock/{sid}/approach")
def mock_approach(sid: str, req: MockTextRequest):
    m = _mock(sid)
    if m["stage"] != "approach":
        raise HTTPException(400, "Not at the approach gate")
    if len(req.text.strip()) < 60:
        raise HTTPException(422, "Describe your approach in a full paragraph")
    if not req.complexity or not req.complexity.strip():
        raise HTTPException(422, "State your expected time AND space complexity")
    with db() as conn:
        conn.execute(
            "UPDATE mock_sessions SET approach_text=?, complexity_text=?,"
            " stage='coding' WHERE id=?", (req.text, req.complexity, sid))
    return mock_state(sid)


def maybe_reveal_followup(sid, solved_slug):
    m = _mock(sid)
    if m["warmup_slug"] == solved_slug and not m["followup_revealed"]:
        with db() as conn:
            conn.execute("UPDATE mock_sessions SET followup_revealed=1 WHERE id=?",
                         (sid,))


class MockFinishRequest(BaseModel):
    rubric: dict


@app.post("/api/mock/{sid}/finish")
def mock_finish(sid: str, req: MockFinishRequest):
    _mock(sid)
    with db() as conn:
        conn.execute("UPDATE mock_sessions SET stage='done', finished_at=?,"
                     " rubric_json=? WHERE id=?",
                     (iso(now()), json.dumps(req.rubric), sid))
        subs = conn.execute(
            "SELECT slug, verdict FROM submissions WHERE mock_session_id=?",
            (sid,)).fetchall()
    m = _mock(sid)
    # shaky mock problems feed the spaced-repetition queue
    passed_slugs = {s["slug"] for s in subs if s["verdict"] == "AC"}
    for slug in {m["warmup_slug"], m.get("followup_slug")} - {None}:
        if slug not in passed_slugs:
            update_srs(slug, False)
    return m


@app.get("/api/mock")
def mock_history():
    with db() as conn:
        rows = conn.execute(
            "SELECT * FROM mock_sessions ORDER BY started_at DESC LIMIT 20").fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------- API: AI review

@app.post("/api/review/{sid}")
def create_review(sid: int):
    with db() as conn:
        cached = conn.execute("SELECT * FROM reviews WHERE submission_id=?",
                              (sid,)).fetchone()
        if cached:
            return {"cached": True, "model": cached["model"],
                    "review": json.loads(cached["content"])}
        sub = conn.execute("SELECT * FROM submissions WHERE id=?", (sid,)).fetchone()
    if not sub:
        raise HTTPException(404, "No such submission")

    # mock-mode timing rule: no AI while the session is live
    mock_ctx = None
    if sub["mock_session_id"]:
        m = _mock(sub["mock_session_id"])
        if m["stage"] != "done":
            raise HTTPException(409, "Mock session still running — the AI reviewer "
                                     "only runs after the session ends.")
        mock_ctx = {"clarifying_questions": m.get("clarify_text"),
                    "approach": m.get("approach_text"),
                    "stated_complexity": m.get("complexity_text")}

    meta = get_problem_meta(sub["slug"])
    statement = _read(os.path.join(meta["dir"], "problem.md"))
    result = json.loads(sub["result_json"] or "{}")
    try:
        review, model = ai_review.review_submission(
            statement=statement, code=sub["code"],
            judge_result=result, mock_context=mock_ctx)
    except ai_review.ReviewError as e:
        raise HTTPException(502, str(e))
    with db() as conn:
        conn.execute("INSERT OR REPLACE INTO reviews (submission_id, model, content,"
                     " created_at) VALUES (?,?,?,?)",
                     (sid, model, json.dumps(review), iso(now())))
    return {"cached": False, "model": model, "review": review}


@app.get("/api/review/{sid}")
def get_review(sid: int):
    with db() as conn:
        row = conn.execute("SELECT * FROM reviews WHERE submission_id=?",
                           (sid,)).fetchone()
    if not row:
        raise HTTPException(404, "No review yet")
    return {"cached": True, "model": row["model"], "review": json.loads(row["content"])}


# ---------------------------------------------------------------- API: study

STUDY_DIR = os.path.join(ROOT, "study")


def parse_frontmatter(text):
    """Minimal ----delimited frontmatter: key: value lines. Returns (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    try:
        _, fm, body = text.split("---", 2)
    except ValueError:
        return {}, text
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            v = v.strip().strip('"').strip("'")
            meta[k.strip()] = int(v) if v.isdigit() else v
    return meta, body.lstrip("\n")


@app.get("/api/study")
def study_index():
    """Tree of study sections -> ordered chapters (from .mdx frontmatter)."""
    if not os.path.isdir(STUDY_DIR):
        return []
    sections = {}
    for dirpath, _dirs, files in os.walk(STUDY_DIR):
        for fname in sorted(files):
            if not fname.endswith((".mdx", ".md")):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fname), STUDY_DIR)
            meta, _ = parse_frontmatter(_read(os.path.join(dirpath, fname)))
            section = meta.get("section") or os.path.dirname(rel) or "General"
            sections.setdefault(section, []).append({
                "path": rel.replace(os.sep, "/"),
                "title": meta.get("title", fname.rsplit(".", 1)[0]),
                "order": meta.get("order", 999),
                "minutes": meta.get("minutes"),
            })
    out = []
    for section, chapters in sections.items():
        chapters.sort(key=lambda c: (c["order"], c["title"]))
        out.append({
            "section": section,
            "order": min(c["order"] for c in chapters),
            "chapters": chapters,
        })
    out.sort(key=lambda s: s["order"])
    return out


@app.get("/api/study/{path:path}")
def study_chapter(path: str):
    full = os.path.normpath(os.path.join(STUDY_DIR, path))
    if not full.startswith(STUDY_DIR) or not os.path.isfile(full):
        raise HTTPException(404, "No such study chapter")
    meta, body = parse_frontmatter(_read(full))
    return {"path": path, "meta": meta, "content": body}


# ---------------------------------------------------------------- API: dashboard

@app.get("/api/stats")
def stats():
    bank = load_bank()
    topic_totals = {}
    for meta in bank.values():
        for t in meta.get("topics", []):
            topic_totals[t] = topic_totals.get(t, 0) + 1
    with db() as conn:
        subs = conn.execute(
            "SELECT slug, verdict, runtime_ms, created_at FROM submissions").fetchall()
        due = conn.execute(
            "SELECT slug, due_at, last_result FROM srs ORDER BY due_at").fetchall()
    solved, attempts = {}, {}
    for s in subs:
        attempts[s["slug"]] = attempts.get(s["slug"], 0) + 1
        if s["verdict"] == "AC":
            solved.setdefault(s["slug"], s["created_at"])
    topic_stats = {}
    for t, total in sorted(topic_totals.items()):
        slugs = [slug for slug, m in bank.items() if t in m.get("topics", [])]
        topic_stats[t] = {
            "total": total,
            "solved": sum(1 for s in slugs if s in solved),
            "attempted": sum(1 for s in slugs if s in attempts),
        }
    # activity: submissions per day, last 30 days
    activity = {}
    for s in subs:
        day = s["created_at"][:10]
        activity[day] = activity.get(day, 0) + 1
    with db() as conn:
        solve_rows = conn.execute(
            "SELECT slug, MIN(elapsed_s) AS seconds FROM submissions"
            " WHERE verdict='AC' AND elapsed_s IS NOT NULL"
            " GROUP BY slug ORDER BY seconds").fetchall()
    solve_times = [dict(r) for r in solve_rows]
    secs = sorted(r["seconds"] for r in solve_rows)
    median_solve = secs[len(secs) // 2] if secs else None
    return {
        "solve_times": solve_times,
        "median_solve_seconds": median_solve,
        "total_problems": len(bank),
        "solved": len(solved),
        "attempted": len(attempts),
        "submissions": len(subs),
        "topics": topic_stats,
        "review_queue": [dict(r) for r in due],
        "activity": activity,
    }


@app.get("/api/daily")
def daily_challenge():
    bank = load_bank()
    if not bank:
        raise HTTPException(500, "Empty problem bank")
    today = now().strftime("%Y-%m-%d")
    slugs = sorted(bank)
    # deterministic per-day pick, weighted toward priority 1-2
    weighted = []
    for s in slugs:
        w = {1: 4, 2: 2, 3: 1}.get(bank[s].get("priority", 3), 1)
        weighted += [s] * w
    h = int(hashlib.sha256(today.encode()).hexdigest(), 16)
    slug = weighted[h % len(weighted)]
    with db() as conn:
        solved_today = conn.execute(
            "SELECT 1 FROM submissions WHERE slug=? AND verdict='AC'"
            " AND created_at LIKE ?", (slug, today + "%")).fetchone()
        # streak: consecutive days ending today (or yesterday) with an AC
        days = {r["created_at"][:10] for r in conn.execute(
            "SELECT created_at FROM submissions WHERE verdict='AC'").fetchall()}
    streak = 0
    d = now().date()
    if today not in days:
        d -= timedelta(days=1)
    while d.strftime("%Y-%m-%d") in days:
        streak += 1
        d -= timedelta(days=1)
    return {"date": today, "slug": slug, "title": bank[slug].get("title"),
            "difficulty": bank[slug].get("difficulty"),
            "done": bool(solved_today), "streak": streak}


# ---------------------------------------------------------------- static UI
# The React app (frontend/) builds into frontend/dist; serve it with an SPA
# fallback so client-side routes deep-link correctly.

DIST = os.path.join(ROOT, "frontend", "dist")

if os.path.isdir(os.path.join(DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST, "assets")),
              name="assets")


@app.get("/{path:path}")
def spa(path: str):
    index = os.path.join(DIST, "index.html")
    if not os.path.exists(index):
        return JSONResponse(
            {"detail": "UI not built. Run: cd frontend && npm install && npm run build"},
            status_code=503)
    candidate = os.path.normpath(os.path.join(DIST, path))
    if path and candidate.startswith(DIST) and os.path.isfile(candidate):
        return FileResponse(candidate)
    return FileResponse(index)
