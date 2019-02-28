import os
import numpy as np
from numba import jit
import utilities
import tqdm
DIRPATH = os.path.dirname(os.path.realpath(__file__))


class HC2019Data:

    def __init__(self, n_images, images):
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.slideshow = []
        self.used = np.zeros(n_images)
        self.images = images
        self.n_images = n_images

    def print_slideshow(self):
        for slide in self.slideshow:
            slide.print_slide()


    @jit
    def add_to_slideshow(self, slide):
        self.slideshow.append(slide)
        self.used[slide.im1.id] = 1
        if not slide.single:
            self.used[slide.im2.id] = 1

    @jit
    def already_added(self, id):
        return self.used[id] == 1

    def print_all(self):
        print("N_IMAGES ", self.n_images)
        for im in self.images:
            print(im.id, im.ntags, im.tags, im.is_horizontal())

    def to_submission(self, name):
        file = open(os.path.join(self.dir, "..", "submissions", name), "w")
        file.write(str(len(self.slideshow)) + "\n")
        for sl in self.slideshow:
            if sl.single:
                file.write(str(sl.im1.id) + "\n")
            else:
                file.write(str(sl.im1.id) + " " + str(sl.im2.id) + "\n")
        file.close()

    @jit
    def create_good_slides(self):
        slides = []
        used = np.zeros(self.n_images)
        for im in tqdm.tqdm(self.images):
            if im.is_horizontal():
                slides.append(Slide(im))
            else:
                im2 = self.get_best_vertical_couple(im, used)
                slides.append(Slide(im, im2))
        return slides

    @jit
    def get_best_vertical_couple(self, im, used):
        imbest = None
        n_tags_best = 0
        for i in range(self.n_images):
            if not used[i] == 1 and not self.images[i].is_horizontal():
                sl = Slide(im, self.images[i])
                if sl.ntags > n_tags_best:
                    imbest = i
                    n_tags_best = sl.ntags
        return self.images[imbest]



def read_data(file):
    filepath = os.path.join(DIRPATH, "..", "datasets", file)
    lines = read_file(filepath, False)
    n_ims = int(lines[0])
    ims = []
    for i in range(1, 1 + n_ims):
        linespl = lines[i].split('\n')[0].split(" ")
        h = linespl.pop(0) == 'H'
        ntags = int(linespl.pop(0))
        id = i - 1
        ims.append(Picture(id, set(linespl), h, ntags))
    return HC2019Data(n_ims, ims)


def read_file(path, verbose):
    if verbose:
        print("Reading dataset.")
    f = open(path, "r")
    b = f.readlines()
    if verbose:
        print(len(b), "samples read.")
    return b


class Picture:
    def __init__(self, id, tags, h, ntags):
        self.h = h
        self.tags = tags
        self.ntags = ntags
        self.id = id

    def is_horizontal(self):
        return self.h

    def n_common_tags(self, im2):
        return len(self.tags.intersection(im2.tags))


class Slide:
    def __init__(self, im1, im2=None):
        self.im1 = im1
        self.im2 = im2
        self.single = im2 is None
        self.tags = im1.tags if im2 is None else im1.tags.union(im2.tags)
        self.ntags = len(self.tags)

    def n_common_tags(self, slide2):
        return len(self.tags.intersection(slide2.tags))

    def score(self, slide2):
        n = self.n_common_tags(slide2)
        return min(n, self.ntags - n, slide2.ntags - n)

    def print_slide(self):
        if self.im2 is not None:
            print('[V|V] tags: {}, ntags: {}'.format(self.tags,self.ntags))
        else:
            print('[H] tags: {}, ntags: {}'.format(self.tags,self.ntags))
if __name__ == '__main__':
    dt = read_data("a_example.txt")
    dt.print_all()
