from matplotlib import pyplot as plt
import numpy as np
import os


def create_plot_from_fn(
    f,
    x_min,
    x_max,
    y_min=None,
    y_max=None,
    save_path=os.path.dirname(os.path.realpath(__file__)),
    save_title="fn",
    xlabel=None,
    ylabel=None,
    title=None,
):
    fzig, ax = plt.subplots()
    x = np.linspace(x_min, x_max, num=1_000)
    y = [f(x_i) for x_i in x]
    plt.plot(x, y)
    ax.spines["right"].set_color((0.8, 0.8, 0.8))
    ax.spines["top"].set_color((0.8, 0.8, 0.8))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # add more ticks
    # ax.set_xticks([1, 5, 10, 20, 50, 100])

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_style("italic")
    xlab.set_size(10)
    ylab.set_style("italic")
    ylab.set_size(10)

    # tweak the title
    ttl = ax.title
    ttl.set_weight("bold")

    plt.grid(linestyle="--", alpha=0.25)
    plt.savefig(f"{save_path}/{save_title}")
