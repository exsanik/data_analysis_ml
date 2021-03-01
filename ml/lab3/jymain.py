# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import math
from treelib import Node, Tree
from functools import reduce


# %%
def calc_entropy(*attrs):
    np_attrs = np.array(attrs)
    if len(np_attrs[np_attrs > 0]) == 1:
        return 0
    elif np.all(np_attrs == attrs[0]):
        return 1

    total = np.sum(attrs)
    return reduce(
        lambda acc, x: acc + (-x / total) * math.log2(x / total),
        np_attrs[np_attrs > 0], 0.0)


# %%
def calc_average_info(parts_total, parts_entropy, total):
    parts = np.dstack((parts_total, parts_entropy))[0]
    return np.array(
        list(map(lambda item: (item[0] / total) * item[1],
                 parts))).sum()


# %%
def calc_different(dataset, header, unique_amount):
    counted_frame = dataset[header].value_counts().values
    missing_items = unique_amount - len(counted_frame)
    return np.append(counted_frame, np.zeros(missing_items, dtype=np.int32)) if missing_items > 0 else counted_frame


# %%
def count_avarage_information(
        dataset, header, entire_dataset_total, unique_amount, show_log=True):
    grouped_by_attr = dataset.groupby(header)
    parts_total = []
    parts_entropy = []
    for key, _item in grouped_by_attr:
        group = grouped_by_attr.get_group(key)
        different = calc_different(group, target_col_name, unique_amount)
        parts_total.append(np.sum(different))
        parts_entropy.append(calc_entropy(*different))

        if show_log:
            print("Different: ", different)
            print(group, "\n\n")
    return calc_average_info(parts_total, parts_entropy, entire_dataset_total)


# %%
def build_decision_tree(dataset, unique_amount, parent=None, tree=Tree()):
    entire_different = calc_different(dataset, target_col_name, unique_amount)
    print("Entire different: ", entire_different)
    entire_dataset_total = np.sum(entire_different)
    entropy = calc_entropy(*entire_different)
    print("Entropy: ", entropy)

    average_info = pd.Series([0] * len(dataset.columns[:-1]), dtype=np.float32)
    average_info.index = dataset.columns[:-1]
    for header in dataset.columns[:-1]:
        average_info.set_value(header, count_avarage_information(
            dataset, header, entire_dataset_total, unique_amount))

    average_info = entropy - average_info
    max_impact = average_info.idxmax()
    tree_node_id = f"{max_impact}_{np.random.normal()}"
    tree.create_node(max_impact, tree_node_id, parent=parent)

    grouped_by_max_impact = dataset.groupby(max_impact)

    for key, _item in grouped_by_max_impact:
        group = grouped_by_max_impact.get_group(key).copy()
        different = calc_different(group, target_col_name, unique_amount)
        group_entropy = calc_entropy(*different)

        group_value = group[max_impact].iloc[0]
        group_value_tree_id = f"{group_value}_{np.random.normal()}"
        tree.create_node(group_value, group_value_tree_id, parent=tree_node_id)
        if group_entropy == 0:
            tree.create_node(
                group[target_col_name].iloc[0],
                f"{group_value}_{np.random.normal()}",
                parent=group_value_tree_id)
        else:
            del group[max_impact]
            if len(group.columns) > 1:
                build_decision_tree(
                    group, unique_values, parent=group_value_tree_id,
                    tree=tree)
            else:
                tree.create_node(
                    group[target_col_name].iloc[0],
                    f"{group_value}_{np.random.normal()}",
                    parent=group_value_tree_id)
    return tree


if __name__ == "__main__":
    credit_data = pd.read_csv("data.csv")
    target_col_name = 'Риск'
    credit_data = credit_data[[col for col in credit_data.columns
                               if col != target_col_name] + [target_col_name]]
    unique_values = len(credit_data[target_col_name].unique())

    tree = build_decision_tree(credit_data, unique_values)
    tree.show()
