import os
import sys

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/utils/"
)
import image_creation


IL = lambda x: 2 * (x + 1) ** 0.5 / (x + 2) - 1
image_creation.create_plot_from_fn(
    IL,
    -1,
    1,
    save_title="IL",
    xlabel=r"$\delta$",
    ylabel="Impremanent Loss",
    title="Impermanent Loss",
)

LPPNL = lambda x: (x + 1) ** 0.5 - 1
image_creation.create_plot_from_fn(
    LPPNL,
    -1,
    1,
    save_title="LPPNL",
    xlabel=r"$\delta$",
    ylabel="Liquidity Position PNL",
    title="Liquidity Position PNL",
)
