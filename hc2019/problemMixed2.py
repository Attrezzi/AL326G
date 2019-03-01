import copy
import numpy as np
from tqdm import tqdm
from hc2019.parser.Parser import *

dataset = read_data("d_pet_pictures.txt")

# Sorting
dataset.images.sort(key = lambda x: x.ntags, reverse=True)


# count = 0
# for i in range(0, len(dataset.images)):
#     count = count + dataset.images[i].ntags

# avg_tag_images = int(count / len(dataset.images))

slides = []

vertical_images  = []
horizontal_images = []

for i in range(0, len(dataset.images)):
    if dataset.images[i].is_horizontal():
        horizontal_images.append(dataset.images[i])
    else:
        vertical_images.append(dataset.images[i])

for i in range(0, int(len(horizontal_images))):
    slides.append(Slide(im1=horizontal_images[i]))

for i in range(0, int(len(vertical_images) / 2)):
    slides.append(Slide(im1=vertical_images[i], im2=vertical_images[len(vertical_images) - i - 1]))

dataset.add_to_slideshow(slides[0])
slides.pop(0)

while len(slides) > 1:
    max_index = 0
    m = 0

    for j in range(0, len(slides), 10):
        value = dataset.slideshow[-1].score(slide2=slides[j])
        if value > m:
            max_index = j
            m = value
    dataset.add_to_slideshow(slides[max_index])
    slides.pop(max_index)
    if len(slides) % 100 == 0:
        print(len(slides))

dataset.to_submission("bois_d_pet_pictures.txt")