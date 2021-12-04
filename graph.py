import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
def scatter_plot(timeframe, bandwidth):
    plt.scatter(timeframe,bandwidth)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Brandwidth (Gb/s)")
    plt.savefig("THROUGHPUT_GRAPH.png")