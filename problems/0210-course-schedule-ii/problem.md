# Course Schedule II

Same setting as Course Schedule: `numCourses` courses labeled `0` to `numCourses - 1`, and `prerequisites[i] = [a, b]` meaning course `b` must be completed before course `a`.

This time, don't just decide feasibility — produce a plan. Return **any** ordering of all `numCourses` courses in which every course appears after all of its prerequisites. If no such ordering exists (the prerequisites contain a cycle), return an empty list.

Any valid ordering is accepted; the shown expected output is just one of possibly many.

## Example 1

```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
```

Course 0 unlocks course 1.

## Example 2

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,1,2,3]
```

`[0,2,1,3]` would be accepted too — both respect every prerequisite.

## Example 3

```
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: []
```

Deadlock: no ordering exists.

## Constraints

- `1 <= numCourses <= 2000`
- `0 <= len(prerequisites) <= 5000`
- `prerequisites[i] = [a, b]` with `0 <= a, b < numCourses`
- All prerequisite pairs are distinct
- A course may even list itself as its own prerequisite (that is an automatic deadlock)
