import os
import numpy as np
import pizza.parser.Pizza as pizz
import pizza.parser.Slice as Slice
DIRPATH = os.path.dirname(os.path.realpath(__file__))


def read_data(file):
    filepath = os.path.join(DIRPATH, "..", "datasets", file)
    lines = read_file(filepath, False)
    r = int(lines[0])
    c = int(lines[1])
    l = int(lines[2])
    h = int(lines[3])
    data = np.zeros([r, c])
    for i in range(4, r + 4):
        for j in range(len(lines[i])):
            if lines[i][j] == 'M':
                data[i-4][j] = 1
    return pizz.Pizza(r, c, l, h, data)


def read_file(path, verbose):
    if verbose:
        print("Reading dataset.")
    f = open(path, "r")
    b = f.readlines()
    if verbose:
        print(len(b), "samples read.")
    return b


if __name__ == "__main__":
    p = read_data("a_example.in")
    print(p.data)
    print(p.is_feasible(Slice.Slice(0, 0, 2, 1)))
    p.add_slice(Slice.Slice(0, 0, 2, 1))
    print(p.is_feasible(Slice.Slice(0, 0, 2, 1)))
    p.to_submission("test_small.txt")