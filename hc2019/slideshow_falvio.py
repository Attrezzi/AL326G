from parser.Parser import read_data,Slide
import tensorflow as tf
import numpy as np
from tensorflow import SparseTensor

#dt = read_data("a_example.txt")
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
        coordinates_list.append([count,element])
        i_list.append(count)
        j_list.append(element)
    count = count + 1
        #one_hot_encoded_list[element] += 1

print('Starting tensors')
from scipy.sparse import  coo_matrix,csr_matrix,save_npz
mat = coo_matrix((np.ones(len(coordinates_list)), (i_list, j_list)), shape=(photo_number, token_number)).tocsr()

print(mat.shape)
print(mat.transpose().shape)

final_matrix = mat.dot(mat.transpose())
print(type(final_matrix))
#print(final_matrix)
#final_matrix.save('finalona.npy')
print('Final matrix created',final_matrix.shape)

print('Saving..')
save_npz('/sparse_matrix.npz', final_matrix)
print('Saved..')
###

'''
tensor = SparseTensor(indices=coordinates_list, values=np.ones(len(coordinates_list)), dense_shape=[photo_number, token_number])
T_tensor = tf.sparse.transpose(tensor)
print(type(T_tensor))
print('Starting tensors')

result = tf.sparse_matmul(tensor,T_tensor)
print('Starting tensors')
print(result.shape)
'''
#one_hot = SparseTensor(X)

#dt = read_data("c_memorable_moments.txt")
#dt = read_data("d_pet_pictures.txt")
#dt = read_data("e_shiny_selfies.txt")
#dt.print_all()

# convert token lists to token-id lists, e.g. [[1, 2], [2, 2]] here
# convert list of token-id lists to one-hot representation
# print(token_ids)

'''
image_list = other.images
sorted_image_list = sorted(image_list, key=lambda x: x.ntags, reverse=True)
photo_n_tags = []
for element in sorted_image_list:
    photo_n_tags.append(element.ntags)
import numpy as np
from tqdm import tqdm
for i in tqdm(range(0,len(sorted_image_list)-1)):
    if not initial_data.already_added(sorted_image_list[i].id):
        slide_i = Slide(sorted_image_list[i])
        #slide_i.print_slide()
        i_tags = sorted_image_list[i].tags
        for j in range(i+1,len(sorted_image_list)-1):
            if set(i_tags).intersection(sorted_image_list[j].tags) == np.floor(sorted_image_list[j].ntags)/2:
                slide_j = Slide(sorted_image_list[j])
                print('Matched: ',slide_j)
                initial_data.add_to_slideshow(slide_i)
                initial_data.add_to_slideshow(slide_j)

initial_data.print_slideshow()


def optimal(a,b):
    if a == b:
        return np.floor(a/2)
    if a > b:
        return np.floor(b/2)
    if b > a:
        return np.floor(a/2)

#print(optimal(4,3))
'''
