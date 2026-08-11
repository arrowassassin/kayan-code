# Course Schedule

A degree program offers `numCourses` courses, labeled `0` through `numCourses - 1`. Some courses gate others: the pair `prerequisites[i] = [a, b]` means you must pass course `b` before you may take course `a`.

Decide whether it is possible to complete **every** course. You may take courses in any order and as many in parallel as you like — the only obstacle is a prerequisite chain that loops back on itself.

Return `true` if all courses can be finished, `false` otherwise.

## Example 1

```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
```

Take course 0, then course 1.

## Example 2

```
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
```

Course 1 needs course 0 first, but course 0 needs course 1 first — a deadlock.

## Constraints

- `1 <= numCourses <= 2000`
- `0 <= len(prerequisites) <= 5000`
- `prerequisites[i] = [a, b]` with `0 <= a, b < numCourses`
- All prerequisite pairs are distinct
- A course may even list itself as its own prerequisite (that is an automatic deadlock)
