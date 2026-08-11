import heapq


# ListNode is predefined: val/next
class Solution:
    def mergeKLists(self, lists: list) -> "ListNode":
        # Min-heap of one node per list: the global next node is always
        # the smallest current head. (val, idx) because ListNode objects
        # aren't comparable — idx breaks value ties.
        heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
        heapq.heapify(heap)                       # O(k)

        dummy = ListNode()                        # noqa: F821 - judge-provided
        tail = dummy
        while heap:
            _, i, node = heapq.heappop(heap)      # smallest head overall
            tail.next = node
            tail = node
            if node.next:                         # refill from the same list
                heapq.heappush(heap, (node.next.val, i, node.next))
        return dummy.next
