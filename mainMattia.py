from pizza.parser import datareader
from pizza.parser.Pizza import Pizza
import utilities
import tqdm
import numpy as np
from random import randint


p = datareader.read_data("d_big.in")

splitCols = randint(0, p.c)
splitRows = randint(0, p.r)

subpizzas = list()
subpizzas.append(Pizza())



N_SORTS = 1000000

nums = list(range(p.l * 2, p.h + 1))
nums.reverse()

for h in nums:
    factors = utilities.factorize(h)
    n_facts = len(factors)

    for _ in tqdm.tqdm(range(N_SORTS)):
        try:
            sl = p.sort_random_slice(factors[np.random.randint(0, n_facts)])
            if p.is_feasible(sl):
                p.add_slice(sl)
        except Exception:
            pass


p.to_submission("randomsub_big.txt")