# %%
import numpy as np
from numpy.core.function_base import linspace
import pandas as pd
import math
import matplotlib.pyplot as plt
import random
import time
# %%


def fnc(x, lam=0.4):
    y = (lam * x) * (1-x)
    return y


def drawLogMap(lambdaEndpoint):
    t = time.time()
    size1 = 10000
    size2 = 500
    arr = np.zeros((size1, size2))
    lamArr = np.linspace(0, lambdaEndpoint, size1)
    for i in range(size1):
        x0 = random.random()
        for j in range(size2):
            # x1 = x0+1
            x1 = fnc(x0, lam=lamArr[i])
            arr[i][j] = x1
            x0 = x1

    # for j in range(size2):

    print(f'Time to calculate: {time.time()-t}')
    return(lamArr, arr)


# %%
# if __name__ == '__main__':
[lamArr, arr] = drawLogMap(3.95)
# %%
t0 = time.time()
size2 = 200
inputlambda = 3.9
ratio = ((inputlambda) / 3.8)
endIndex = int(ratio*len(lamArr))
print(endIndex)
plt.plot(lamArr[0:endIndex], arr[0:endIndex, size2-5:size2],
         'r o', linewidth=0.1, markersize=0.07)
plt.show()
print(f'TOTAL ELAPSED TIME: {time.time()-t0}')
# plt.scatter(lamArr, arr[:, 50:size2])
# plt.scatter(np.arange(size2+1), arr)
# print(arr)
# plt.show()
# pass
