import os
import numpy as np
from numba import jit
from pizza.parser import Slice

class Pizza:

    def __init__(self, r, c, l, h, data, slices=None):
        self.r = r
        self.c = c
        self.l = l
        self.h = h
        self.data = data
        self.occupied = np.zeros([self.r, self.c])
        self.slices = slices
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def to_submission(self, name):
        file = open(os.path.join(self.dir, "..", "submissions", name), "w")
        file.write(str(len(self.slices)) + "\n")
        for sl in self.slices:
            file.write(str(sl.r1) + " " + str(sl.c1) + " " + str(sl.r2) + " " + str(sl.c2) + "\n")
        file.close()

    @jit
    def add_slice(self, slice_to_add):
        if self.slices is None:
            self.slices = [slice_to_add]
        else:
            self.slices.append(slice_to_add)
        self.occupied[slice_to_add.r1:slice_to_add.r2+1, slice_to_add.c1:slice_to_add.c2+1] = 1

    @jit
    def is_feasible(self, sl):
        dim = (sl.r2 - sl.r1 + 1) * (sl.c2 - sl.c1 + 1)
        s = np.sum(self.data[sl.r1:sl.r2+1, sl.c1:sl.c2+1])
        return dim <= self.h and s >= self.l and dim - s >= self.l and \
               np.sum(self.occupied[sl.r1:sl.r2+1, sl.c1:sl.c2+1]) == 0

    @jit
    def sort_random_slice(self, dim):
        r1 = np.random.randint(0, self.r - dim[0] + 1)
        c1 = np.random.randint(0, self.c - dim[1] + 1)
        r2 = r1 + dim[0] - 1
        c2 = c1 + dim[1] - 1
        return Slice.Slice(r1, c1, r2, c2)

