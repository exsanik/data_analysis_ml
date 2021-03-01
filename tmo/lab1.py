import numpy as np
import pandas as pd
import math
import random
from collections import namedtuple
from itertools import tee
from functools import reduce
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", None, "display.max_columns", None)

MomentData = namedtuple('MomentData', ['ri', 'zi', 'tk'])


def count_z_i(lambda_value: float, random_moument: float):
    return -(math.log(random_moument) / lambda_value)


def generate_interval(t_start, t_finish, lambda_value):
    moments = []
    current_time = t_start
    while current_time <= t_finish:
        random_moment = random.random()
        step_between_moment = count_z_i(lambda_value, random_moment)
        current_time += step_between_moment
        md = MomentData(ri=random_moment,
                        zi=step_between_moment, tk=current_time)
        moments.append(md)
    return moments


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def interval_count(interval_amount, moments, start, finish):
    interval_table = pd.DataFrame(
        columns=pd.Series(
            np.arange(interval_amount),
            name='Interval number'))

    interval_row = pd.Series(np.zeros(interval_amount))
    interval_row.name = "x(t)"
    interval_table = interval_table.append(interval_row)
    intervals = np.linspace(start, finish + 1, interval_amount)

    for moment in moments:
        for idx, (x, y) in enumerate(pairwise(intervals)):
            if x <= moment.tk < y:
                interval_table.iloc[0][idx] += 1
                break
    return interval_table


def grouped_bar_plot(
        y_data_list, colors, y_data_names, x_label="Интервалы",
        y_label="Количество попаданий", title="Пример"):

    dpi = 100
    fig = plt.figure(dpi=dpi, figsize=(1280 / dpi, 526 / dpi))

    ax = plt.axes()
    ax.yaxis.grid(True, zorder=1)

    xs = range(1, 26)
    arr = []
    for i in xs:
        arr.append(str(i))
    width = 0.3
    for i in range(len(y_data_list)):
        plt.bar(
            [x + width * i for x in xs],
            y_data_list[i],
            width=width, color=colors[i],
            label=y_data_names[i])

    newXs = [x + 0.3 for x in xs]
    plt.xticks(newXs, arr)

    fig.autofmt_xdate(rotation=25)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.legend(y_data_names, loc='upper right')
    plt.show()


def main():
    group_number = 2
    list_number = 24
    lambda_value = 10 * group_number / list_number

    t_start = list_number + 1
    t_finish = list_number + 5

    tau = (t_finish - t_start) / 25

    lambda_1 = 9 * group_number / list_number
    lambda_2 = 13 * group_number / list_number

    moments_1 = generate_interval(t_start, t_finish, lambda_1)
    moments_2 = generate_interval(t_start, t_finish, lambda_2)
    table_1 = pd.DataFrame(moments_1)

    table_2 = pd.DataFrame(moments_2)

    interval_table_1 = interval_count(25, moments_1, t_start, t_finish)

    interval_table_2 = interval_count(25, moments_2, t_start, t_finish)

    row_1 = interval_table_1.iloc[0]
    row_1.name = "x1(t)"
    row_2 = interval_table_2.iloc[0]
    row_2.name = "x2(t)"
    row_1_2 = row_1 + row_2
    row_1_2.name = "x1 + x2"
    all_intervals = pd.DataFrame([row_1, row_2, row_1_2])

    grouped_bar_plot(
        [row_1, row_2, row_1_2],
        ['#0000ff', '#ff0000', '#00ff00'],
        ['x1(n)', 'x2(n)', 'x + y'])

    count_freq = row_1_2.value_counts()
    count_freq_table = pd.DataFrame(
        columns=np.arange(max(len(moments_1), len(moments_2))))

    count_freq_table = count_freq_table.append(count_freq)
    count_freq_table = count_freq_table.fillna(0)
    count_freq_table

    math_expectation = reduce(lambda acc, x: acc + x, count_freq, 0) / 25
    model_expectation = math_expectation / tau
    dispersion = reduce(
        lambda acc, x: acc + ((x - math_expectation) ** 2), count_freq, 0) / (25 - 1)
    print("Model expectation", model_expectation)
    print("Math expectation", math_expectation)
    print("Lambda", lambda_1 + lambda_2)
    print("Dispersion", dispersion)


if __name__ == "__main__":
    main()
