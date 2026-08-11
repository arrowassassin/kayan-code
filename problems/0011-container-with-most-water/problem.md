# Container With Most Water

You are given `n` vertical lines drawn on a number line: line `i` stands at x-coordinate `i` and has height `height[i]`. Pick two of the lines; together with the x-axis they form an open-topped container. The water it can hold is

```
area = min(height[i], height[j]) * (j - i)
```

— the shorter line caps the water level, and the distance between the lines is the width. Return the **maximum** water any pair of lines can contain. The container must be flat-bottomed (you cannot tilt it), and lines between the chosen pair do not interfere.

## Example 1

```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
```

Lines at positions 1 and 8 (heights 8 and 7) give `min(8,7) * (8-1) = 49`.

## Example 2

```
Input: height = [1,1]
Output: 1
```

`min(1,1) * 1 = 1`.

## Constraints

- `2 <= len(height) <= 10^5`
- `0 <= height[i] <= 10^4`
