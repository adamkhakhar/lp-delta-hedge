from matplotlib import pyplot as plt
import numpy as np
import os
import math


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
    _, ax = plt.subplots()
    x = None
    y = None
    if type(f) == list:
        x = np.linspace(x_min, x_max, len(f))
        y = f
    else:
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
        zeros = np.zeros(len(x))
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

    if y_min is not None and y_max is not None:
        ax.set_ylim([y_min, y_max])

    plt.tight_layout()
    plt.grid(linestyle="--", alpha=0.25)
    plt.savefig(f"{save_path}/{save_title}", bbox_inches="tight")


def create_liquidity_plot(
    version,
    save_path=f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/results",
):
    if version == 2:
        x = np.linspace(0, 100, 100)
        y = [1] * 100
        fig, ax = plt.subplots()
        plt.plot(x, y, color="blue")
        ax.set_xticks([0, 100])
        ax.set_xticklabels([r"0", r"$\infty$"])
        xlab = ax.xaxis.get_label()
        ylab = ax.yaxis.get_label()
        xlab.set_style("italic")
        xlab.set_size(10)
        ylab.set_style("italic")
        ylab.set_size(10)
        ax.get_xticklabels()[-1].set_fontsize(15)
        ax.axes.yaxis.set_ticks([])
        ax.spines["right"].set_color((0.8, 0.8, 0.8))
        ax.spines["top"].set_color((0.8, 0.8, 0.8))
        plt.xlabel(r"$p_{a;b}$")
        plt.ylabel("Liquidity")
        plt.title("Uniform Liquidity")
        ax.set_ylim([0, 2])

        zeros = np.zeros(100)
        ax.fill_between(x, y, zeros, where=(y > zeros), color="lavender")
        ttl = ax.title
        ttl.set_weight("bold")
        plt.savefig(f"{save_path}/uniform_liquidity.png")
    if version == 3:
        y = np.random.normal(0, 1, size=100_000)
        fig, ax = plt.subplots()
        plt.hist(
            [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6],
            bins=7,
            histtype="bar",
            color="lavender",
            ec="blue",
        )
        xlab = ax.xaxis.get_label()
        ylab = ax.yaxis.get_label()
        xlab.set_style("italic")
        xlab.set_size(10)
        ylab.set_style("italic")
        ylab.set_size(10)
        ax.get_xticklabels()[-1].set_fontsize(15)
        ax.axes.yaxis.set_ticks([])
        ax.axes.xaxis.set_ticks([])
        ax.spines["right"].set_color((0.8, 0.8, 0.8))
        ax.spines["top"].set_color((0.8, 0.8, 0.8))
        plt.xlabel(r"$p_{a;b}$")
        plt.ylabel("Liquidity")
        plt.title("Concentrated Liquidity")

        ttl = ax.title
        ttl.set_weight("bold")
        plt.savefig(f"{save_path}/concentrated_liquidity.png")


def create_position_value_plot(
    save_path=f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/results",
):
    l = 10
    h = 70
    x = np.linspace(0, 100, 100)
    v = (
        lambda x: x
        if x < l
        else (
            math.sqrt(l * h)
            * (math.sqrt(x) - math.sqrt(l))
            / (math.sqrt(h) - math.sqrt(l))
            + math.sqrt(x * l)
            * (math.sqrt(h) - math.sqrt(x))
            / (math.sqrt(h) - math.sqrt(l))
        )
        if x < h
        else math.sqrt(l * h)
    )
    y = [v(x_0) for x_0 in x]
    fig, ax = plt.subplots()
    plt.plot(x, y, color="blue")
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_style("italic")
    xlab.set_size(10)
    ylab.set_style("italic")
    ylab.set_size(10)
    plt.ylim(ymax=math.sqrt(l * h) + l / 2, ymin=0)

    for x_0 in [l, h]:
        plt.axvline(
            x=x_0,
            ymin=0,
            ymax=v(x_0) / (math.sqrt(l * h) + l / 2),
            color="black",
            linestyle="dashed",
            alpha=1 / 12,
        )

    ax.set_yticks([math.sqrt(l * h)])
    ax.set_yticklabels([r"$\sqrt{p_{a;b}^l \times p_{a;b}^u}$"])
    ax.set_xticks([l, math.sqrt(l * h), h])
    ax.set_xticklabels(
        [r"$p_{a;b}^l$", r"$\sqrt{p_{a;b}^l \times p_{a;b}^u}$", r"$p_{a;b}^h$"]
    )

    # ax.get_xticklabels()[-1].set_fontsize(15)
    ax.spines["right"].set_color((0.8, 0.8, 0.8))
    ax.spines["top"].set_color((0.8, 0.8, 0.8))
    plt.xlabel(r"$p_{a;b}$")
    plt.ylabel("Final Value Pool Assets")
    plt.title("Final Value of Pool Assets Over Price Space")
    # ax.set_ylim([0, 2])

    zeros = np.zeros(100)
    ax.fill_between(x, y, zeros, where=(y > zeros), color="lavender")
    ttl = ax.title
    ttl.set_weight("bold")
    plt.tight_layout()
    plt.savefig(f"{save_path}/pool_assets_v3.png")
