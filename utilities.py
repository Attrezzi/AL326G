def factorize(n):
    factors = []
    for i in range(1, n + 1):
        if int(n/i) == n/i:
            factors.append([i, int(n/i)])
    return factors
