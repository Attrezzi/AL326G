import matplotlib.pyplot as mplt

def factorize(n):
    factors = []
    for i in range(1, n + 1):
        if int(n/i) == n/i:
            factors.append([i, int(n/i)])
    return factors


def showimage(image):
    """displays a single image in SciView"""
    mplt.figure()
    mplt.imshow(image)
    mplt.show()