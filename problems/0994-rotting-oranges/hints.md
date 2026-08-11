## Hint 1

"Spreads one step per minute, simultaneously from every rotten orange" is a distance question, not a counting question. Which traversal explores a graph in order of distance from a source?

## Hint 2

There isn't one source — every rotten orange starts spreading at minute 0. Instead of running one BFS per rotten orange, seed a single queue with *all* of them before you start. All cells at BFS layer `k` rot at minute `k`.

## Hint 3

Count the fresh oranges up front. Process the queue layer by layer (snapshot `len(queue)` each round), marking a fresh orange rotten the moment you enqueue it and decrementing the fresh counter. The answer is the number of layers processed — unless fresh oranges remain at the end, which means `-1`. Watch the all-rotten-already case: it must return `0`, not `1`.
