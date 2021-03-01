import math
from functools import reduce

import pandas as pd
import numpy as np


def bellman_ford(graph, source):
    distance, predecessor = dict(), dict()
    for node in graph:
        distance[node], predecessor[node] = float('inf'), None
    distance[source] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbour in graph[node]:
                if distance[neighbour] > distance[node] + graph[node][neighbour]:
                    distance[neighbour], predecessor[neighbour] = distance[node] + graph[node][neighbour], node

    for node in graph:
        for neighbour in graph[node]:
            assert distance[neighbour] <= distance[node] + \
                graph[node][neighbour], "Negative weight cycle."

    return distance, predecessor


def bernulli(n, m, p):
    return (math.factorial(n) / (math.factorial(m) * math.factorial((n - m)))) *\
        (p ** m) * ((1 - p) ** (n - m))


def count_states_price(take_price, return_price, points):
    table = [[0 for __ in range(points + 1)] for _ in range(points + 1)]
    for i in range(points + 1):
        for j in range(points + 1):
            table[i][j] = (i * take_price) + (max(0, j - i) * return_price)
    return table


if __name__ == '__main__':
    graph = {
        '1': {'2': 3, '3': 7, '4':  2},
        '2': {'7':  5, '6':  11, '5':  9},
        '3': {'5': 5, '6': 10},
        '4': {'6':  15, '7':  13},
        '5': {'8': 7, '9': 5},
        '6': {'7': 7, '8': 3},
        '7': {'8': 7, '9': 1},
        '8': {'10': 1},
        '9': {'10': 4},
        '10': {}
    }
    broke_possibility = 0.1
    take_price = 800
    return_price = 1200

    distance, predecessor = bellman_ford(graph, source='1')

    current_vertex = '10'
    count_vertex = 1
    print('Path: ', current_vertex, end=' ')
    while current_vertex != '1':
        current_vertex = predecessor[current_vertex]
        print(' -> ', current_vertex, end=' ')
        count_vertex += 1
    print()

    print("Price: ", distance['10'])
    print('Path length: ', count_vertex)

    price_table = pd.DataFrame(count_states_price(
        take_price, return_price, count_vertex))
    print(price_table)

    bernulli_possibly = [
        bernulli(count_vertex, x, broke_possibility)
        for x in range(count_vertex + 1)]
    print("Bernulli expectations: ", bernulli_possibly, end="\n\n")

    math_expectations = [0] * (count_vertex + 1)
    for i in range(count_vertex + 1):
        math_expectations[i] = (price_table.iloc[i] * bernulli_possibly).sum()

    print("Math expectations: ", math_expectations, end="\n\n")
    best_strategy = np.argmin(math_expectations)
    print(
        f"Best strategy is to take {best_strategy} blocks with cost: {math_expectations[best_strategy]}")

    min_spends = (price_table.iloc[0] * bernulli_possibly).sum()
    full_info_spends = reduce(
        lambda acc, i: acc + (price_table.iloc[i][i] * bernulli_possibly[i]),
        range(0, count_vertex + 1),
        0)
    info_price = min_spends - full_info_spends
    print("Information price: ", info_price)
