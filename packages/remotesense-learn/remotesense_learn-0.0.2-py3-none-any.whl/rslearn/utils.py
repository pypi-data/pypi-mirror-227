from functools import reduce,partial
import numpy as np

def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


bsq_to_bip=partial(np.transpose,axes=[1,2,0])

bsq_to_bil=partial(np.transpose,axes=[1,0,2])

bip_to_bsq=partial(np.transpose,axes=[2,0,1])

bip_to_bil=partial(np.transpose,axes=[0,2,1])

bil_to_bip=partial(np.transpose,axes=[0,2,1])

bil_to_bsq=partial(np.transpose,axes=[1,0,2])