from hc2019.parser import Parser
import numpy as np
import tqdm

dt = Parser.read_data("c_memorable_moments.txt")

slides = dt.create_good_slides()
used = np.zeros()
prev = slides[np.random.randint(0, len(slides))]
dt.add_to_slideshow(prev)

for sl in tqdm.tqdm(slides):

