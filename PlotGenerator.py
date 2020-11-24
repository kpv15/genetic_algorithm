import numpy as np
import matplotlib.pyplot as plt


class PlotGenerator:
    @staticmethod
    def generate(value_history, minimum):
        avgs = []
        bests = []
        stds = []
        for v in value_history:
            avgs.append(np.mean(v))
            if minimum:
                bests.append(np.min(v))
            else:
                bests.append(np.max(v))
            stds.append(np.std(v))

        plt.clf()
        plt.plot(range(len(value_history)), avgs)
        plt.ylabel('avgs')
        plt.xlabel('epochs')
        plt.savefig('avgs.png')

        plt.clf()
        plt.plot(range(len(value_history)), bests)
        plt.ylabel('bests')
        plt.xlabel('epochs')
        plt.savefig('bests.png')

        plt.clf()
        plt.plot(range(len(value_history)), stds)
        plt.ylabel('stds')
        plt.xlabel('epochs')
        plt.savefig('stds.png')
