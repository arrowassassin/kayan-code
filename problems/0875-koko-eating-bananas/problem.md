# Koko Eating Bananas

Koko has `piles` of bananas in front of her — `piles[i]` is the number of bananas in the i-th pile — and `h` hours before the guards return. She picks a fixed eating speed `k` (bananas per hour). Each hour she chooses one pile and eats `k` bananas from it; if fewer than `k` remain in that pile, she finishes the pile and eats nothing more that hour (she never splits an hour across two piles).

Return the **smallest** integer speed `k` that lets her finish every pile within `h` hours.

## Example 1

```
Input: piles = [3,6,7,11], h = 8
Output: 4
```

At speed 4 the piles take `1 + 2 + 2 + 3 = 8` hours — exactly the deadline. At speed 3 they would take `1 + 2 + 3 + 4 = 10` hours, too slow.

## Example 2

```
Input: piles = [30,11,23,4,20], h = 5
Output: 30
```

Five piles, five hours: every pile must be cleared in a single hour, so `k` must be at least the largest pile.

## Example 3

```
Input: piles = [30,11,23,4,20], h = 6
Output: 23
```

One spare hour lets the biggest pile take two hours, so `k` only needs to cover the second-largest in one sitting.

## Constraints

- `1 <= len(piles) <= 5 * 10^4`
- `1 <= piles[i] <= 10^9`
- `len(piles) <= h <= 10^9` (a valid speed always exists)
- The answer and all intermediate hour counts fit in a 64-bit integer.
