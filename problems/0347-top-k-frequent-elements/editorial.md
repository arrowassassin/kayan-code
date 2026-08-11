# Top K Frequent Elements — Editorial

## 1. Pattern recognition

"Most frequent" + "top k" + "any order" — three signals. "Most frequent" means a **counting pass with a hash map** comes first, no exceptions. "Top k" means the ranking step is the Top-K pattern you built in Kth Largest (this problem's warmup): rank a collection by a key without fully sorting it. And "any order" is the interviewer telling you not to waste effort producing a sorted answer — a hint that something cheaper than sorting exists.

## 2. Brute force first

Count with a `Counter`, then sort the distinct values by count descending and slice the first k: O(d log d) for d distinct values (worst case d = n = 10⁵). Honestly? It passes comfortably — `Counter(nums).most_common(k)` is one line. The reason to go further is the conversation: the interviewer picked this problem to hear you notice that (a) you only need k winners, not a full ranking → heap, and (b) the ranking *key* is a bounded integer → you can skip comparison-based methods entirely.

## 3. The key insight

**A frequency is an integer between 1 and n — a bounded key — so instead of comparing counts you can use the count as an array index: bucket sort gives O(n).**

## 4. Step-by-step derivation

1. Pass 1: `counts = Counter(nums)` — O(n), unavoidable, and it shrinks the problem from n elements to d distinct (value, count) pairs.
2. Heap version: keep a min-heap of size k keyed on count; each pair either beats the root (replace, O(log k)) or is discarded. O(d log k). In Python, `heapq.nlargest(k, counts, key=counts.get)` is precisely this loop — and remember `heapq` is a **min-heap**, which is what a top-k filter wants; no negation needed when you use `nlargest`.
3. Now interrogate the key: counts range over 1…n. Whenever the sort key is a small bounded integer, comparison sorting (and its log factor) is overkill — index by the key instead.
4. Build `buckets` where `buckets[f]` lists every value occurring exactly f times. A value can't occur more than n times, so n+1 buckets always suffice.
5. Walk buckets from index n down to 1, appending values until you've emitted k. Since the total bucket content is d values and the walk is one pass over n+1 slots, the whole algorithm is **O(n) time, O(n) space** — the log is gone.
6. Which to say in an interview? Lead with "count, then it's top-k — heap gives n log k", then upgrade: "but the keys are bounded integers, so bucket sort makes it linear." That ordering shows both the pattern and the ability to beat it.

## 5. Annotated Python solution

```python
from collections import Counter


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = Counter(nums)                          # O(n) counting pass

        # index = frequency; a count never exceeds len(nums),
        # so len(nums)+1 buckets always fit every possible key
        buckets = [[] for _ in range(len(nums) + 1)]
        for val, freq in counts.items():
            buckets[freq].append(val)

        res = []
        for freq in range(len(buckets) - 1, 0, -1):     # highest freq first
            for val in buckets[freq]:
                res.append(val)
                if len(res) == k:                       # stop the instant we have k
                    return res
        return res
```

Heap alternative (the O(n log k) answer, worth writing when asked):

```python
import heapq
from collections import Counter


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        counts = Counter(nums)
        # min-heap of (count, value): root = weakest of the current top k
        return [v for _, v in heapq.nlargest(k, ((c, v) for v, c in counts.items()))]
```

## 6. Complexity

- Bucket sort: **Time O(n)**, **Space O(n)** — "counting, bucketing, and the bucket walk are each one linear pass; there is no comparison sort anywhere."
- Heap: **Time O(n + d log k)**, **Space O(d)** — "count once, then each distinct value does at most one log-k heap operation."

## 7. Edge-case traps

- **k equals the number of distinct values** — the answer is every distinct value; the bucket walk must not stop early or run past bucket 1.
- **Single-element array / all elements identical** — one bucket at frequency n; the loop from the top must actually reach it.
- **Negative values** — they're hash-map keys, not indices; only *frequencies* index the buckets. Mixing that up is the classic bucket-sort bug.
- **Multiple values sharing one frequency** — buckets hold lists, not single slots; overwriting instead of appending silently drops answers.
- Heap version: pushing `(value, count)` instead of `(count, value)` ranks by value — a tuple-order bug that still returns *something* plausible.

## 8. Reusable template

Not DP. This trains **count-then-rank**: hash-map frequency pass feeding the top-k machinery — the same two-stage pipeline as Top K Frequent Words (the linked follow-up) and Sort Characters by Frequency.

## 9. Interviewer follow-up

- *"Now the elements are words, and ties break alphabetically"* — that's the linked follow-up (692): bucket sort still works but each bucket needs sorting, and the heap needs a two-field comparison with *opposite* directions; "any order" was doing more work here than it looked.
- *"The array is a stream / distributed across machines"* — per-machine partial counts merge by summation; then top-k over the merged map. Mention count-min sketch when exact counts don't fit in memory.
- *"O(1) extra space?"* — not possible while counting arbitrary values; with a bounded value range (here −10⁴…10⁴) a fixed-size count array replaces the hash map.
- *"Return them ordered by frequency?"* — bucket walk already produces that order for free; the heap version needs a final sort of k items, O(k log k).
