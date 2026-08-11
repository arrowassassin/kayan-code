# Merge K Sorted Lists — Editorial

## 1. Pattern recognition

"k **sorted** sources, produce one sorted output" is the **k-way merge** — the heap pattern's second face. Top-K problems use a heap as a *filter* (keep the best k); k-way merge uses it as a *dispatcher* (repeatedly hand me the smallest of k current candidates). The tell is sortedness of each source: at any instant only the k current heads can possibly be next, so the problem reduces to "extract-min over a set of k that refills itself" — the literal job description of a priority queue. This is also the engine inside external-sort and log-stream merging, which is why data-infrastructure interviews love it.

## 2. Brute force first

Collect every value into one array, sort, rebuild a list: O(N log N) for N total nodes, and it discards the gift that each list is already sorted. Second naive option: merge list 1 with list 2, the result with list 3, and so on. Each merge re-walks the accumulated result, so the total is O(N·k) — with N = 10⁵ and k = 10⁴ that's ~10⁹ node visits, a clean TLE. Both attempts fail the same interview question: *where is the sortedness being used?*

## 3. The key insight

**The next output node is always the smallest of the k current heads — so a min-heap holding exactly one node per list dispenses the entire merged order in O(log k) per node.**

## 4. Step-by-step derivation

1. Sortedness means each list's candidates arrive in order; globally, the only possible next node is one of the k current heads. So we never need more than k candidates in play.
2. Put those heads in a min-heap. Pop the minimum → that node is the next output. The popped node's successor becomes its list's new head → push it. The heap's size only shrinks (when a list runs dry), never exceeds k.
3. Python trap: `ListNode` defines no `__lt__`, and when two tuples tie on `val`, tuple comparison falls through to the next field — comparing nodes and crashing. Push `(val, list_index, node)`: the integer index settles ties before a node is ever compared. Say this *before* it bites; it's the most common live-coding failure on this problem.
4. Stitch output nodes behind a **dummy head** so the empty result and the first append need no special case; return `dummy.next`.
5. Each of N nodes is pushed and popped exactly once: **O(N log k)**. Seeding the heap with `heapify` is O(k) — linear, worth stating.
6. Alternative with the same bound: **divide and conquer** — merge lists pairwise in rounds (1&2, 3&4, …), halving k each round; log k rounds of O(N) work. No heap, no comparability trap, and O(1) auxiliary structure. Offer it when the interviewer asks "without a priority queue?".

## 5. Annotated Python solution

```python
import heapq


# ListNode is predefined: val/next
class Solution:
    def mergeKLists(self, lists: list) -> "ListNode":
        # One candidate per list: its current head. (val, idx, node) —
        # idx breaks value ties so ListNodes are never compared directly.
        heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
        heapq.heapify(heap)                       # O(k), linear

        dummy = ListNode()                        # dummy head: no empty-result special case
        tail = dummy
        while heap:
            _, i, node = heapq.heappop(heap)      # global minimum among the k heads
            tail.next = node                      # splice the node itself — no copying
            tail = node
            if node.next:                         # that list's next node becomes its candidate
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next
```

## 6. Complexity

- **Time O(N log k)** — "every one of the N nodes passes through the heap exactly once, and the heap never holds more than k entries."
- **Space O(k)** for the heap — "output reuses the existing nodes, so only the k candidates cost extra memory."

## 7. Edge-case traps

- **`lists` empty, or containing only empty lists** (`[]`, `[[]]`, `[[],[]]`) — the seeding comprehension must skip `None` heads and the loop must fall through to return `None`.
- **Duplicate values across lists** — this is exactly where the missing tie-breaker crashes with `TypeError: '<' not supported between instances of 'ListNode'`; a test with `[[5,5,5],[5,5]]` exists to catch it.
- **One list vastly longer than the rest** — after the others drain, the heap has one entry and the loop must still relink the tail correctly.
- **Sequential pairwise merging** — correct but O(N·k); the stress test with k = 50 lists of 200 nodes is sized so the heap flies and quadratic accumulation feels the heat.
- Rebuilding nodes instead of relinking them — allocates N new nodes and usually reverses nothing, but in an interview it signals discomfort with pointers.

## 8. Reusable template

Not DP. This trains the **k-way merge via refilling min-heap** — the same dispatcher powers Employee Free Time, Smallest Range Covering K Lists, Kth Smallest in a Sorted Matrix, and every external-sort merge phase.

## 9. Interviewer follow-up

- *"The k sources are unbounded streams, and I want running order statistics"* — you can no longer buffer and merge; balancing *two* heaps against each other maintains a running median. That is the linked follow-up, Find Median from Data Stream (295).
- *"No heap allowed"* — divide-and-conquer pairwise merge: log k rounds, O(N log k) total, using only the two-list merge you already know.
- *"Lists don't fit in memory"* — this is external sort's merge phase verbatim: buffered reads per source, one output buffer, the same heap over k buffer heads.
- *"k is huge, nodes per list tiny"* — heap cost is per-node log k either way; mention a tournament/loser tree as the classic constant-factor optimization in database mergers.
