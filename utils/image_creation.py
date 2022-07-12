from matplotlib import pyplot as plt
import numpy as np
import os


def create_plot_from_fn(
    f,
    x_min,
    x_max,
    y_min=None,
    y_max=None,
    save_path=f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/results",
    save_title="fn",
    xlabel=None,
    ylabel=None,
    title=None,
    x_axis_line=True,
    shade_pnl=True,
    num=1_000,
):
    fzig, ax = plt.subplots()
    x = np.linspace(x_min, x_max, num=num)
    y = [f(x_i) for x_i in x]
    plt.plot(x, y)
    ax.spines["right"].set_color((0.8, 0.8, 0.8))
    ax.spines["top"].set_color((0.8, 0.8, 0.8))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if x_axis_line:
        plt.axhline(y=0, color="black", linestyle="dotted", alpha=0.25)

    if shade_pnl:
        zeros = np.zeros(x.shape)
        ax.fill_between(x, y, zeros, where=(y < zeros), color="darkred", alpha=1 / 12)
        ax.fill_between(x, y, zeros, where=(y > zeros), color="darkgreen", alpha=1 / 12)

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
