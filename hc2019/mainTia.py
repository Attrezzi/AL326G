import numpy as np
from hc2019.parser.Parser import read_data
from hc2019.parser.Parser import HC2019Data
from hc2019.parser.Parser import Slide
from hc2019.parser.Parser import Picture
from numba import jit
from tqdm import tqdm
import random

@jit
def scores_matrix(data, n_common_tags):
    scores = np.zeros(shape=(data.n_images, data.n_images))

    for i in tqdm(range(data.n_images)):
        slide1 = Slide(data.images[i])
        for j in range(i+1, data.n_images):
            scores[i, j] = slide1.score(Slide(data.images[j]))

    return scores

@jit
def explore(matrix):
    steps = 1
    startx = random.randint(0, 101)
    starty = random.randint(0, 101) # it must be different from the first one
    sum = matrix[startx, starty]
    seq = [startx, starty]

    while steps <= 20000:
        if steps % 1000 == 0:
            print(steps)
            print(sum)



        if steps % 2 == 1: # steps odd, go down, search rows
            tmp = np.amax(matrix[:, starty])
            sum = sum + tmp
            steps = steps + 1
            matrix[startx, starty] = 0
            startx = matrix[:, starty].argmax()
            seq.append(startx)
        else:
            tmp = np.amax(matrix[startx, :])
            sum = sum + tmp
            steps = steps + 1
            matrix[startx, starty] = 0
            starty = matrix[startx, :].argmax()
            seq.append(starty)

    return seq


if __name__ == "__main__":
    data = read_data("b_lovely_landscapes.txt")
    # print(scores_matrix(data))

    n_common_tags = np.random.randint(low=0, high=50, size=(100, 100))

    seq = explore(n_common_tags)

    for i in seq:
        im = Slide(data.images[i])
        data.add_to_slideshow(im)

    data.to_submission("fl_mt.txt")