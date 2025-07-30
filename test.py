def count_ways():
    dp = [[0 for _ in range(16)] for _ in range(50)]
    dp[0][0] = 1  # start at position 0 with 0 moves

    for moves in range(15):  # up to 14 moves to add the next one
        for pos in range(50):
            if dp[pos][moves] > 0:
                for step in range(1, 6):  # step from 1 to 5
                    next_pos = pos + step
                    if next_pos < 50:
                        dp[next_pos][moves + 1] += dp[pos][moves]

    # Now sum all ways to reach position 49 in 1 to 15 moves
    m = sum(dp[49][moves] for moves in range(1, 16))
    return m % 1000  # last 3 digits

print(count_ways())
