# Task Scheduler

A single CPU must execute a batch of tasks, given as an array `tasks` of uppercase letters — each letter names a task type. Executing any task takes exactly one time unit, and in each unit the CPU either runs one task or sits **idle**.

The catch is a cooldown: after running a task of some type, the CPU must wait at least `n` time units before running *another task of that same type* (different types are fine in between, as are idle units).

Tasks may be executed in any order. Return the **minimum total number of time units** (tasks + idles) needed to finish everything.

## Example 1

```
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
```

One optimal schedule: `A B idle A B idle A B` — each pair of same-type runs is separated by at least 2 units.

## Example 2

```
Input: tasks = ["A","A","A","B","B","B"], n = 0
Output: 6
```

No cooldown — just run all six tasks back to back.

## Constraints

- `1 <= len(tasks) <= 10^4`
- `tasks[i]` is an uppercase letter `'A'`–`'Z'` (at most 26 distinct types)
- `0 <= n <= 100`
