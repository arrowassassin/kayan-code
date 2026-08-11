# Trapping Rain Water

You are given an elevation profile as an array `height`, where `height[i]` is the height of the terrain column at position `i` (each column has width 1). After a heavy rain, water settles in every dip of the profile — it is held wherever taller terrain stands on both sides, and it drains off the two open ends of the array.

Return the total number of unit cells of water the profile retains.

## Example 1

```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

Water collects in the dip at index 2 (1 unit), and in the basin between the walls of height 2 and 3 (5 units).

## Example 2

```
Input: height = [4,2,0,3,2,5]
Output: 9
```

## Constraints

- `0 <= len(height) <= 10^5 + 1`
- `0 <= height[i] <= 10^5`

A column of terrain at height `h` under a water level `w` holds `w - h` units of water at that position. Positions at the extreme ends can never hold water.
