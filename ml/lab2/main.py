import numpy as np


def find_s(data):
    specific = data[0]
    for i in range(1, len(data)):
        diff_vector = specific != data[i]
        specific[diff_vector] = '?'
    return specific


def candidate_elimination(data):
    positive = data[data[:, -1] == 'yes'][:, :-1]
    negative = data[data[:, -1] != 'yes'][:, :-1]
    vector_len = len(positive[0])

    specific = find_s(positive)

    no_match_ids = np.array([], dtype=np.int)
    for negative_vector in negative:
        fail_ids = np.where((specific != '?') & (negative_vector != specific))
        no_match_ids = np.append(no_match_ids, fail_ids)
    no_match_ids = np.unique(no_match_ids)

    general = np.full((len(no_match_ids), vector_len), '?', dtype="U10")
    for i, attr_id in enumerate(no_match_ids):
        general[i][attr_id] = specific[attr_id]

    return (specific, general)


def main():
    data = np.genfromtxt('data.csv', delimiter=',', dtype="U10")
    header = data[0]
    print("Data headers:")
    print(header)
    param_data = data[1:]
    print("Attributes data: ")
    print(param_data)
    filtered_negative = param_data[param_data[:, -1] == 'yes'][:, :-1]
    print()
    print("Find S Algorithm:")
    print(find_s(filtered_negative))
    print()
    specific, general = candidate_elimination(param_data)
    print('Candidate Elimination algorithm:')
    print("Specific: ", specific)
    print("General: ")
    print(general)


if __name__ == "__main__":
    main()
