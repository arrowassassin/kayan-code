# Coin Change

You are given a list of coin denominations `coins` and a target `amount`. You have an unlimited supply of every denomination. Return the **fewest** number of coins whose values sum to exactly `amount`.

If no combination of coins can reach the amount exactly, return `-1`. An amount of `0` requires `0` coins.

## Example 1

```
Input: coins = [1,2,5], amount = 11
Output: 3
```

`11 = 5 + 5 + 1` — three coins. No two coins reach 11.

## Example 2

```
Input: coins = [2], amount = 3
Output: -1
```

Even values only; 3 is unreachable.

## Example 3

```
Input: coins = [1,3,4], amount = 6
Output: 2
```

`6 = 3 + 3`. Note that greedily taking the largest coin first (`4 + 1 + 1`) uses three coins.

## Constraints

- `1 <= len(coins) <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`

Denominations may be larger than `amount` and may contain duplicates.
