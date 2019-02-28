from hc2019.parser import Parser
import numpy as np

dt = Parser.read_data("d_pet_pictures.txt")

slides = dt.create_good_slides()
nslides = len(slides)
print(nslides)

tagsdict = {}
for i in range(nslides):
    slide = slides[i]
    for tag in slide.tags:
        try:
            tagsdict[tag].append(i)
        except Exception:
            tagsdict[tag] = [i]
# print(tagsdict)

APPROX = 0.4

ran = np.random.randint(0, nslides)
used = np.zeros(nslides)
prev = slides[ran]
used[ran] = 1
dt.add_to_slideshow(prev)

count = 0
while True:
    found = False
    assigned = False
    print(count)
    for i in range(nslides):
        if used[i] == 0:
            bestsl = slides[i]
            best_sc = bestsl.score(prev)
            i_ind = i
            found = True
            break
    if not found:
        break
    for tag in prev.tags:
        for imm in tagsdict[tag]:
            if used[imm] == 0:
                sl = slides[imm]
                scorenew = prev.score(sl)
                if scorenew > best_sc:
                    bestsl = sl
                    best_sc = scorenew
                    i_ind = imm
                    if scorenew >= APPROX * prev.ntags / 2:
                        assigned = True
                        break
        if assigned:
            break


    count += 1
    dt.add_to_slideshow(bestsl)
    prev = bestsl
    used[i_ind] = 1

dt.to_submission("e.txt")





