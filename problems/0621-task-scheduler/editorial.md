# Task Scheduler — Editorial

## 1. Pattern recognition

"Schedule freely, cooldown between repeats, minimize total time" — a **greedy scheduling** problem where only the *frequency profile* matters (order is yours to choose, so the input sequence is noise). Problems in this family have two canonical solutions: a **greedy-with-max-heap simulation** ("always run the most-constrained task next") and a **closed-form counting argument** built around the most frequent element. Interviewers use this problem to see whether you can climb from the simulation to the formula — and its sibling, Reorganize String, is the same math with "cooldown 1, no idles allowed".

## 2. Brute force first

Search over all orderings — factorially hopeless. The honest first *real* answer is the simulation: count tasks, then tick time forward; at each tick run the eligible task with the most remaining copies (max-heap keyed on remaining count, plus a cooldown queue of tasks waiting to become eligible). That's O(T · log 26) for T total time units — perfectly fast here, and correct. The reason to keep thinking: the simulation ticks through *idle* units one by one, and with `n = 100` and three copies of one task, the schedule is 203 units of which 200 are idle — a hint that the answer is really a counting question, not a stepping question.

## 3. The key insight

**The most frequent task pins the schedule's skeleton: its `f` occurrences force `f-1` gaps of width at least `n`, and every other task either hides inside those gaps or extends the schedule so that no idle time remains at all.**

## 4. Step-by-step derivation

1. Let `f` be the maximum frequency and `ties` the number of task types achieving it. Lay the most frequent task out first: `X ... X ... X` — `f-1` blocks, each `n+1` wide (the task plus its cooldown window), then the final `X`.
2. Any max-frequency peer must also occupy one slot in every block *and* one after the last block — so the tail row holds `ties` tasks. Frame length: `(f-1)(n+1) + ties`. Nothing shorter can exist: the first max-frequency task alone needs that much room. That's the **lower bound** argument.
3. Now the filler tasks (frequency < f). Distribute them round-robin across the `f-1` gaps, always spreading a type over *different* gaps — a type with at most `f-1` copies never lands twice in one gap, so no cooldown is violated. If they all fit, idles fill the rest and the frame length stands.
4. If they *don't* fit, gaps widen beyond `n+1`. But widening means every unit is now busy — zero idles — so the schedule is exactly `len(tasks)` units, and no schedule can beat that (each task takes one unit). That's the second regime's lower bound.
5. Both regimes are simultaneously lower bounds and achievable, so the answer is simply `max(len(tasks), (f-1)(n+1) + ties)` — O(n) counting, O(1) space, no simulation.
6. In the interview: present the heap simulation as the "works for any cooldown rule" general tool, then derive the formula and say *why* it's safe. If the rules get richer (per-type cooldowns, priorities), the formula dies and the heap survives — knowing which tool generalizes is the senior-signal.

## 5. Annotated Python solution

```python
from collections import Counter


class Solution:
    def leastInterval(self, tasks: list[str], n: int) -> int:
        counts = Counter(tasks)
        f = max(counts.values())                      # dominant frequency
        ties = sum(1 for c in counts.values() if c == f)
        # Skeleton forced by a max-frequency task: (f-1) blocks of width n+1,
        # plus the final row of all tasks tied at frequency f.
        frame = (f - 1) * (n + 1) + ties
        # Overflow regime: fillers exceed the gaps -> zero idles -> just len(tasks).
        return max(len(tasks), frame)
```

## 6. Complexity

- **Time O(len(tasks))** — "one counting pass; the formula itself is O(26)."
- **Space O(1)** — "at most 26 counters, independent of input size."

## 7. Edge-case traps

- **`n = 0`** — no cooldown; the frame formula gives `f - 1 + ties` which is ≤ `len(tasks)`, so the `max` silently does the right thing — but only if you kept it.
- **More tasks than frame** (many distinct types) — forgetting the `max(len(tasks), ...)` is *the* classic bug; the formula alone undercounts.
- **Several types tied at the max frequency** — omitting `ties` (using `+1` instead) fails `["A","A","B","B"], n=2` → 5, not 4.
- **Huge `n`, tiny task set** (`["B","B","B"], n=100` → 203) — simulation loops 203 ticks; the formula doesn't care. Also a good sanity check that idles dominate.
- **Single task** — `(1-1)*(n+1) + 1 = 1` regardless of `n`; the cooldown never triggers after the last run.

## 8. Reusable template

Not DP. This trains the **most-frequent-element frame argument** (bound the schedule by the dominant item, then check the overflow regime) and its executable twin, the **greedy max-heap + cooldown queue simulation** — the exact pair you redeploy in Reorganize String and Rearrange String k Distance Apart.

## 9. Interviewer follow-up

- *"Return an actual schedule, not just its length"* — the formula only counts; switch to the heap simulation: pop up to `n+1` most-frequent eligible types per round, emit them, re-queue with decremented counts.
- *"Tasks must run in the given order"* — greedy choice disappears; it becomes a linear scan tracking each type's last execution time and inserting forced idles.
- *"Per-type cooldowns `n[t]`"* — formula dead; heap simulation with a time-keyed cooldown queue still works.
- *"Cooldown 1 and idles forbidden — when is it even possible?"* — that's Reorganize String (767): possible iff `f <= ceil(len/2)`, same frame argument with zero slack.
