import os
import numpy as np
from numba import jit
import utilities
import tqdm
DIRPATH = os.path.dirname(os.path.realpath(__file__))


class HC2019Data:

    def __init__(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def to_submission(self, name):
        file = open(os.path.join(self.dir, "..", "submissions", name), "w")
        #file.write(str(len(self.slices)) + "\n")
        #for sl in self.slices:
        #    file.write(str(sl.r1) + " " + str(sl.c1) + " " + str(sl.r2) + " " + str(sl.c2) + "\n")
        #file.close()



def read_data(file):
    filepath = os.path.join(DIRPATH, "..", "datasets", file)
    lines = read_file(filepath, False)
    pass
    # return pizz.Pizza(r, c, l, h, data)


def read_file(path, verbose):
    if verbose:
        print("Reading dataset.")
    f = open(path, "r")
    b = f.readlines()
    if verbose:
        print(len(b), "samples read.")
    return b

