import sys
import os
import numpy as np
import matplotlib.pyplot as plt

dirname = 'candidates'
try:
    dirname += sys.argv[1]
except IndexError:
    pass

rfis = np.load('rfi_freq_indexs.npz')['arr_0']
dirthings = os.listdir(dirname)
dirthings = sorted(dirthings)
for filename in dirthings:
    if filename.endswith('.npz'):
        data = np.load(os.path.join(dirname, filename))['data']
        for a, b in rfis:
            data[:, a:b] = 0
        data -= data[:300, :].mean(0)
        plt.imshow(np.clip(data.T, 0, 5), aspect='auto', 
                extent=[0, data.shape[0]*0.00256, 400, 800]
        )
        plt.suptitle(filename)
        plt.colorbar()
        plt.show()
        plt.close()

