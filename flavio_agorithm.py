import numpy as np
from pizza.parser.datareader import read_data
from pizza.parser.Slice import  Slice
pizza = read_data("d_big.in")


def find_least_frequent(pizza):
    mean = np.mean(pizza.data)
    if mean >= 0.5:
        return 0
    else:
        return 1

def find_most_frequent(pizza):
    mean = np.mean(pizza.data)
    if mean >= 0.5:
        return 1
    else:
        return 0

print(np.mean(pizza.data))

def find_element(pizza, minimum_element):
    min_rows, min_cols = np.where(pizza.data == minimum_element)
    return min_rows[0], min_cols[0]


def explore_direction(pizza,start_index,row_delta, column_delta):
    if start_index[0] - row_delta < 0:
        return False
    if start_index[1] - column_delta< 0:
        return False
    else:
        return True


def cut_slices(input_pizza, slice_list):
    start_index = find_element(input_pizza, find_least_frequent(input_pizza))
    new_slice = None
    print(start_index)
    unfeasible = False

    # Logic for exploring the pizza slices.
    starting_slice = Slice(start_index[0],start_index[1],start_index[0],start_index[1])

    if explore_direction(input_pizza, start_index, 0, -1):
        adding_element = input_pizza.data[start_index[0], start_index[1] - 1]
        if adding_element == 0:
            new_slice = Slice(starting_slice.r1-1,starting_slice.c1,starting_slice.r2,starting_slice.c2)

    if new_slice is not None:
        slice_list.append(new_slice)

    # here we cut the slice and go further
    matrix = input_pizza.data
    for i in range(new_slice.r1, new_slice.r2):
        for j in range(new_slice.c1, new_slice.c2):
            matrix[i, j] = -1
    input_pizza.data = matrix

    if unfeasible:
        return slice_list
    else:
        cut_slices(input_pizza, slice_list)

#print(cut_slices(pizza, []))
