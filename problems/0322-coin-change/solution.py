class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        INF = amount + 1                      # can never need more than `amount` coins
        dp = [0] + [INF] * amount             # dp[a] = fewest coins summing to a
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1     # last coin is c, best for the rest is dp[a-c]
        return dp[amount] if dp[amount] != INF else -1
