import pandas as pd
import numpy as np
import math
pd.options.mode.chained_assignment = None  # default='warn'


def calc_positive_negative(dataset, negative_value, positive_value):
    counted_frame = dataset.value_counts()
    negative = counted_frame[negative_value] if negative_value in counted_frame else 0
    positive = counted_frame[positive_value] if positive_value in counted_frame else 0
    return (positive, negative)


def calc_entropy(positive, negative):
    if positive == 0 or negative == 0:
        return 0
    elif positive == negative:
        return 1

    total = positive + negative
    return (-positive / total) * math.log2(positive / total) - (negative / total) * math.log2(negative / total)


def count_levels(sampled, valued):
    levels = []
    prev_class = None
    prev_value = None
    for class_value, value in zip(sampled, valued):
        if prev_class != class_value and prev_class is not None:
            levels.append((prev_value + value) / 2)
        prev_class = class_value
        prev_value = value
    return levels


def sample_dataframe(data):
    for ind in range(1, len(data.columns)):
        print("Initial:")
        print(data)
        data = data.sort_values(data.columns[ind], ascending=False)
        print("Sorted:")
        print(data)

        current_series = data.iloc[:, ind].copy()
        prev_series = data.iloc[:, ind - 1]

        levels = count_levels(prev_series, current_series)
        print("Levels:", levels)
        pos_neg = calc_positive_negative(prev_series, '-', '+')
        entire_entropy = calc_entropy(*pos_neg)
        print("Entire entropy:", entire_entropy)

        levels_gain = []
        for level in levels:
            less_level = data.loc[current_series < level]
            more_level = data.loc[current_series > level]
            pos_neg_less_level = calc_positive_negative(
                less_level[prev_series.name], '-', '+')
            pos_neg_more_level = calc_positive_negative(
                more_level[prev_series.name], '-', '+')
            less_level_entropy = calc_entropy(*pos_neg_less_level)
            more_level_entropy = calc_entropy(*pos_neg_more_level)

            gain = entire_entropy - (len(less_level) / len(current_series) *
                                     less_level_entropy + len(more_level) /
                                     len(current_series) * more_level_entropy)
            levels_gain.append(gain)
        print("Level gains:", levels_gain)

        max_gain_level_ind = np.argmax(levels_gain)
        max_gain_level = levels[max_gain_level_ind]

        data.iloc[:, ind].loc[current_series <= max_gain_level] = '+'
        data.iloc[:, ind].loc[current_series > max_gain_level] = '-'

        print("Sampled: ")
        print(data, '\n\n')
    return data


if __name__ == "__main__":
    data = pd.read_csv('./data.csv')
    data = sample_dataframe(data)
