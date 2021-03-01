import random
from typing import DefaultDict, Iterable, List, Tuple, Union
from collections import defaultdict


def count_line_len(file_name: str) -> int:
    with open(file_name, 'r') as file:
        return sum(1 for line in file)


def count_attr_len(file_name: str) -> int:
    with open(file_name, 'r') as file:
        line = file.readline()
        return len(line.split(','))


def read_line(file_name: str, line_index: int) -> List[str]:
    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            if i == line_index:
                return line.strip().split(',')


def get_attr(line: Union[str, List[str]],
             attr_index: int) -> Union[str, float]:
    if(type(line) == str):
        line = line.strip().split(',')

    attr = line[min(attr_index, len(line) - 1)]
    return float(attr) if attr.replace('.', '', 1).isdigit() else attr


def random_sort(file_name: str, lines_amount: int, attr_index: int, amount=20) -> List[List[str]]:
    random_indices = sorted(random.sample(
        range(0, lines_amount),
        min(lines_amount, amount)))
    lines = []

    indices_ind = 0
    with open(file_name, 'r') as file:
        for i, line in enumerate(file):
            if i == random_indices[indices_ind]:
                indices_ind += 1
                if len(line.strip()) == 0:
                    continue
                lines.append(line.strip().split(','))

            if indices_ind == len(random_indices):
                break

    lines.sort(key=lambda line: get_attr(line, attr_index))
    return lines


def mathematical_expectation(
        attr_list: Iterable[Union[str, float]],
        attr_index: int) -> float:
    attr_sum = 0
    lines_amount = 0
    for line in attr_list:
        if type(line) == str:
            if len(line.strip()) == 0:
                continue

        attr = get_attr(line, attr_index)
        if type(attr) == str:
            raise ValueError(
                "Can't count mathematical expectation for attrubute of string type")

        attr_sum += attr
        lines_amount += 1

    return attr_sum / lines_amount


def standard_deviation(
        attr_list: Iterable[Union[str, float]],
        attr_index: int,
        math_expectation: float) -> float:
    attr_sum = 0
    lines_amount = 0
    for line in attr_list:
        if type(line) == str:
            if len(line.strip()) == 0:
                continue

        attr = get_attr(line, attr_index)
        if type(attr) == str:
            raise ValueError(
                "Can't count mathematical expectation for attrubute of string type")

        attr_sum += (attr - math_expectation) ** 2
        lines_amount += 1

    return (attr_sum / (lines_amount - 1)) ** 0.5


def dispersion(
        attr_list: Iterable[Union[str, float]],
        attr_index: int,
        math_expectation: float) -> float:
    return standard_deviation(attr_list, attr_index, math_expectation) ** 2


ByClassDict = DefaultDict[str, Tuple[List[List[str]],
                                     List[float],
                                     List[float]]]


def classification_precalc(file_name, class_index=-1) -> ByClassDict:
    # [0]: initial data, [1]: list[mathematical_expectation], [2]: list[dispersion]
    by_class_dict: ByClassDict = defaultdict(lambda: ([], [], []))

    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip().split(',')
            if len(line) == 0:
                continue

            class_name = line[class_index]
            if len(class_name.strip()) == 0:
                continue
            by_class_dict[class_name][0].append(line[0:-1])

    for class_name in by_class_dict:
        for i, _ in enumerate(by_class_dict[class_name][0][0]):
            math_exp = mathematical_expectation(
                by_class_dict[class_name][0], i)
            disper = dispersion(
                by_class_dict[class_name][0], i, math_exp)

            by_class_dict[class_name][1].append(math_exp)
            by_class_dict[class_name][2].append(disper)

    return by_class_dict


def input_set(attr_len: int) -> List[float]:
    input_data = input().strip().split(',')
    return list(map(float, input_data))


def classify_set(set_item: List[float], by_class_dict: ByClassDict) -> str:
    deviation_by_class = dict()
    for class_name in by_class_dict:
        deviation_sum = 0
        for i, value in enumerate(set_item):
            deviation = min(abs(value - by_class_dict[class_name][1][i] - by_class_dict[class_name][2][i]), abs(
                value - by_class_dict[class_name][1][i] + by_class_dict[class_name][2][i]))

            deviation_sum += deviation
        deviation_by_class[class_name] = deviation_sum

    class_name, _ = min(deviation_by_class.items(), key=lambda x: x[1])
    return class_name


def main():
    file_name = 'iris.data'
    lines_len = count_line_len(file_name)
    attr_len = count_attr_len(file_name)

    print("Task 1: access to element")
    print(read_line(file_name, random.randint(0, lines_len)))
    print()

    print("Task 2: random sort")
    random_lines = random_sort(file_name, lines_len, 2)
    print(*random_lines, sep='\n')
    print()

    print("Task 3: math expectation and dispersion")
    math_expectation = mathematical_expectation(random_lines, 2)
    print("Math expectation: ", math_expectation)
    print("Dispersion: ", dispersion(random_lines, 2, math_expectation))
    print()

    print("Task 4: classification")
    by_class_dict = classification_precalc(file_name)
    set_item = input_set(attr_len)

    # Input: 7.7,2.8,6.7,2.0  Output: Iris-virginica
    print(classify_set(set_item, by_class_dict))
    print()


if __name__ == "__main__":
    main()
