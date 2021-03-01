import numpy as np
import random


def generate_priority_vector(amount):
    matrix = np.zeros((amount, amount + 2), dtype=np.float)

    for i in range(0, amount):
        for j in range(0, amount):
            if i == j:
                matrix[i, j] = 1
            else:
                matrix[i, j] = random.randint(1, 9) / random.randint(1, 9)

    for i in range(0, amount):
        matrix[i][amount] = np.sum(matrix[i][:amount])

    sum_vectors = np.sum(matrix[:, amount])

    for i in range(0, amount):
        matrix[i][amount + 1] = matrix[i][amount] / sum_vectors

    return matrix[:, amount + 1]


if __name__ == "__main__":
    products = ['Злагода', 'Зареч’є', 'Добриня', 'Простоквашино', 'Селяньське']
    products_len = len(products)

    criterias = ['Жирність', 'Рослинні жири',
                 'Сертифікат єкологічної чистоти', 'Строк зберігання', 'Ціна']

    matrix_priors = np.zeros((products_len, products_len))
    for i in range(len(criterias)):
        matrix_priors[i, :] = generate_priority_vector(products_len)
        print(f'Priority vector for {criterias[i]}')
        print(matrix_priors[i, :], end="\n\n")

    vector_priors = generate_priority_vector(products_len)
    print(f'Criterias priority vector {vector_priors}')

    result = matrix_priors @ vector_priors
    for i in range(products_len):
        print(f"| {products[i]} |", end=" ")
    print()
    for i in range(products_len):
        print(f"| {round(result[i], 4)}{' ' * (len(products[i]) - 6)} |",
              end=" ")
    print()

    max_product_col = np.argmax(result)
    print(f"Best choice: {products[max_product_col]}")
