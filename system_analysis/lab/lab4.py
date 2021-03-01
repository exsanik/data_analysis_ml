import math

import numpy as np
import matplotlib.pyplot as plt


def b(p, q):
    return math.factorial(p - 1) * math.factorial(q - 1) / math.factorial(p + q - q)


def g(w, p, q):
    return (1 / b(p, q)) * w ** (p - 1) * (1 - w) ** (q - 1)


def k_valid(c1, c2, p, q, n, k):
    return c1/c2 * (p + q + n) - p - 1 <= k <= c1/c2 * (p + q + n) * p


def check_k(c1, c2, p, q, n):
    for k in range(0, n):
        if k_valid(c1, c2, p, q, n, k):
            return k


if __name__ == "__main__":
    w_arr = list(np.arange(0, 1, 0.05))
    g_arr = []
    p = 1
    q = 5

    for w in w_arr:
        g_arr.append(g(w, p, q))

    plt.plot(w_arr, g_arr)
    plt.savefig("mygraph.png")

    c1 = 180
    c2 = 2000
    n1 = 30
    n2 = 45

    k1 = check_k(c1, c2, p, q, n1)
    k2 = check_k(c1, c2, p, q, n2)

    print(f"{k1}|{n1}")
    print(f"{k2}|{n2}")
