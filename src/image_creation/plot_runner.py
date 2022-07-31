import os
import sys

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))}/utils/"
)
import image_creation


IL = lambda x: (2 * ((x + 1) ** 0.5) / (x + 2) - 1) * 100
image_creation.create_plot_from_fn(
    IL,
    -1,
    1,
    save_title="IL",
    xlabel=r"$\delta$",
    ylabel="Impermanent Loss (%)",
    title="Impermanent Loss",
)

LPPNL = lambda x: ((x + 1) ** 0.5 - 1) * 100
image_creation.create_plot_from_fn(
    LPPNL,
    -1,
    1,
    save_title="LPPNL",
    xlabel=r"$\delta$",
    ylabel="PNL (%)",
    title="Liquidity Position PNL",
)

image_creation.create_liquidity_plot(2)
image_creation.create_liquidity_plot(3)

image_creation.create_position_value_plot()


LPPNL_Uniswap_v2 = lambda x: 463.647 * (((x / 1613.68) ** 0.5) - 1)
image_creation.create_plot_from_fn(
    LPPNL_Uniswap_v2,
    0,
    5_000,
    save_title="experiment_v2_lppnl",
    xlabel=r"$p_{Ethereum;USDT}^f$",
    ylabel="PNL ($ Thousands)",
    title="ETH-USDT Liquidity Position PNL Uniswap v2",
)
Options_Portfolio_Target_PNL = lambda x: -463.647 * (((x / 1613.68) ** 0.5) - 1)
image_creation.create_plot_from_fn(
    Options_Portfolio_Target_PNL,
    0,
    5_000,
    save_title="experiment_v2_options_target_pnl",
    xlabel=r"$p_{Ethereum;USDT}^f$",
    ylabel="PNL ($ Thousands)",
    title="Target Options Portfolio PNL Uniswap v2",
)
