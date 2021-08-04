# %%
import time
import numpy as np
import random
from multiprocessing.sharedctypes import Value, Array
from multiprocessing import Pool, Process, Lock
from ctypes import Structure, c_double
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class getLogMap(object):

    def __init__(self, parameters):

        self.parameters = parameters
        self.size1 = self.parameters['size1']
        self.lambdaEndpoint = self.parameters['lambdaEndpoint']
        self.size2 = self.parameters['size2']
        self.lamIndex = 0
        self.arr = np.zeros((self.size1, self.size2))  # Evolution matrix
        self.lamArr = np.linspace(0, self.lambdaEndpoint, self.size1)
        self.testArr = []
        self.timeArr = np.arange(self.size2)

    def fnc(self, x, lam=0.4):
        # evolution Function over one iteration (generation)
        y = (lam * x) * (1-x)
        return y

    def evolvePopulation(self, lamindex):
        t = time.time()
        x0 = random.random()
        lam = self.lamArr[lamindex]
        # Evolve single population over size2 generations
        for j in range(self.size2):
            x1 = self.fnc(x0, lam)
            self.arr[lamindex][j] = x1
            x0 = x1

        return 1

    def populateMatrix(self):
        # Loop over all lambdas
        for i in range(self.size1):
            self.evolvePopulation(i)

    def getData(self, inputlambda=3.5):

        # Get ratio of input lambda to graph with respect to the lambda end point
        ratio = ((inputlambda) / self.lambdaEndpoint)
        # get the end index
        endIndex = int(ratio*self.size1)
        # desired section from lambda array
        x = self.lamArr[0:endIndex]
        # desired section from evolution array
        y = self.arr[0:endIndex, self.size2-1:self.size2]
        z = self.arr[endIndex-1, :]
        print(endIndex)

        return x, y, z

    def updatePlot(self):
        lam = self.s_lambda.val
        [x, y, z] = self.getData(lam)
        for i in range(len(self.f_d)):
            self.f_d[i].set_data(x, y)
        self.s_d[0].set_data(self.timeArr, z)
        self.fig.canvas.draw_idle()

    def plotter(self):
        self.fig = plt.figure(figsize=(6, 4))
        # Create main axis
        ax = self.fig.add_subplot(211)
        # Create secondary axis
        ax2 = self.fig.add_subplot(212)
        self.fig.subplots_adjust(bottom=0.2, top=0.75)

        # Create axes for sliders
        ax_lambda = self.fig.add_axes([0.3, 0.85, 0.4, 0.05])
        ax_lambda.spines['top'].set_visible(True)
        ax_lambda.spines['right'].set_visible(True)

        # Create slider
        self.s_lambda = Slider(ax=ax_lambda, label=r'$\lambda$ Values', valmin=0, valmax=3.95, valinit=0.1,
                               valfmt=r'$\lambda$=%1.2f ', facecolor='#cc7000')

        # Get data for initial plotting condition
        [x0, y0, z0] = self.getData(inputlambda=0.1)
        w0 = np.zeros((len(x0), 15))

        # Plot default data
        self.f_d = ax.plot(x0, w0, 'r o', linewidth=0.1, markersize=0.3)
        ax.set_xlim([0, 4.1])
        ax.set_ylim([-0.1, 1.1])
        ax2.set_ylim([-0.1, 1.1])
        # Plot default data
        self.s_d = ax2.plot(self.timeArr, z0, 'r o',
                            linewidth=0.5, markersize=2)
        self.s_lambda.on_changed(self.updatePlot)
        plt.show()


        # %%
if __name__ == '__main__':

    parameters = {
        'lambdaEndpoint': 3.95,
        'size1': 20000,
        'size2': 500,
    }
    logMaptest = getLogMap(parameters)
    t1 = time.time()
    logMaptest.populateMatrix()
    print(f'elapsed time: {time.time()-t1}')
    # %%
    logMaptest.plotter()
    # t2 = time.time()
    # logMaptest.plotLogMap(1.2)
    # print(f'PLOTTING TIME: {time.time()-t2}')
    # lamArr = np.linspace(0, lambdaEndpoint, size1)
