import copy
import numpy as np
from tqdm import tqdm
from hc2019.parser.Parser import *

dataset = read_data("e_shiny_selfies.txt")

# Sorting
dataset.images.sort(key = lambda x: x.ntags, reverse=True)


# count = 0
# for i in range(0, len(dataset.images)):
#     count = count + dataset.images[i].ntags

# avg_tag_images = int(count / len(dataset.images))

slides = []

for i in range(0, int(len(dataset.images) / 2)):
    slides.append(Slide(im1=dataset.images[i], im2=dataset.images[len(dataset.images) - i - 1]))

dataset.add_to_slideshow(slides[0])
slides.pop(0)

while len(slides) > 1:
    max_index = 0
    m = 0

    for j in range(0, len(slides)):
        value = dataset.slideshow[-1].score(slide2=slides[j])
        if value > m:
            max_index = j
            m = value
    dataset.add_to_slideshow(slides[max_index])
    slides.pop(max_index)
    if len(slides) % 100 == 0:
        print(len(slides))

dataset.to_submission("e_shiny_selfies.txt")