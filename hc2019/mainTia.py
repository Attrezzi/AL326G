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

    from parser.Parser import read_data, Slide
    import tensorflow as tf
    import numpy as np
    from tensorflow import SparseTensor

    # dt = read_data("a_example.txt")
    dataset = "b_lovely_landscapes.txt"
    initial_data = read_data(dataset)
    other = read_data(dataset)
    tag_list = []

    for element in initial_data.images:
        tag_list.append(element.tags)

    flat_list = [item for sublist in tag_list for item in sublist]
    token_set = set()
    for item in flat_list:
        token_set.add(item)
    token_set = list(token_set)
    token_number = (len(token_set))
    from numpy import array

    # define example

    word_to_id = {token: idx for idx, token in enumerate(set(token_set))}
    token_ids = [[word_to_id[token] if token != "''" else 0 for token in tokens_doc] for tokens_doc in tag_list]
    X = []
    """
    for lst in token_ids:
        one_hot_encoded_list = np.zeros(len(word_to_id))
        for element in lst:
            one_hot_encoded_list[element] += 1
        X.append(one_hot_encoded_list)
    """
    coordinates_list = []
    count = 0

    photo_number = len(token_ids)
    print(photo_number)

    i_list = []
    j_list = []
    for lst in token_ids:
        one_hot_encoded_list = np.zeros(len(word_to_id))
        for element in lst:
            coordinates_list.append([count, element])
            i_list.append(count)
            j_list.append(element)
        count = count + 1
        # one_hot_encoded_list[element] += 1

    print('Starting tensors')
    from scipy.sparse import coo_matrix, csr_matrix, save_npz

    mat = coo_matrix((np.ones(len(coordinates_list)), (i_list, j_list)), shape=(photo_number, token_number)).tocsr()

    print(mat.shape)
    print(mat.transpose().shape)

    final_matrix = mat.dot(mat.transpose()).todense()
    seq = explore(final_matrix)

    for i in seq:
        im = Slide(data.images[i])
        data.add_to_slideshow(im)

    data.to_submission("fl_mt.txt")