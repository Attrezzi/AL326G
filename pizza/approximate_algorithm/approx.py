from pizza.parser import datareader
import utilities
import tqdm
import numpy as np

N_SORTS = 200000
N_PIZZAS = 2
pizzas = []

for numpiz in range(N_PIZZAS):
    p = datareader.read_data("c_medium.in")
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
    pizzas.append(p)

for numpiz in range(1, N_PIZZAS):
    pizzas[0].merge_pizzas(pizzas[numpiz])

utilities.showimage(pizzas[0].occupied)
pizzas[0].fill_holes()

pizzas[0].to_submission("randomsub_med.txt")
utilities.showimage(pizzas[0].occupied)
