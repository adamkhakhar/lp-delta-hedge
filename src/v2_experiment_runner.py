import os
import sys
import json


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(BASE_DIR)
from delta_hedge.OptimizationRunner import OptimizationRunner as OptimizationRunner

ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR + "/utils")
from image_creation import create_plot_from_fn

ROOT_DIR = os.path.dirname(BASE_DIR)

if __name__ == "__main__":
    path_to_config = ROOT_DIR + "/configs/uniform_liquidity_config.json"
    TARGET_FUN = lambda x: -463_647 * (((x / 1613.68) ** 0.5) - 1)
    with open(path_to_config) as f:
        config = json.load(f)

    data_params = {
        "final_price_lower_bound": config["final_price_lower_bound"],
        "final_price_upper_bound": config["final_price_upper_bound"],
        "target_function": TARGET_FUN,
    }
    deriv_params = {"asset": config["asset"], "expired": config["expired"]}
    train_params = {
        "learning_rate": config["learning_rate"],
        "num_samples": config["num_samples"],
        "batch_size": config["batch_size"],
        "test_batch_size": config["batch_size"],
        "log_every": config["log_every"],
    }
    runner = OptimizationRunner(config["name"], data_params, deriv_params, train_params)
    runner.train()
    runner.pretty_print_results()
    runner.present_pnl("Options Portfolio Payoff - ETH USD - Uniform Liquidity")
    options_portfolio_pnl_fun = runner.get_pnl_fun()
    combined_pnl = lambda x: (TARGET_FUN(x) + options_portfolio_pnl_fun(x)) / 1000
    create_plot_from_fn(
        combined_pnl,
        config["final_price_lower_bound"],
        config["final_price_upper_bound"],
        y_min=None,
        y_max=None,
        save_title="experiment_v2_combined_lppnl_options",
        xlabel=r"p_{a;b}^f",
        ylabel="PNL ($ Thousands)",
        title="ETH-USDT Delta-Hedged Liquidity Position PNL - Uniswap v2",
        x_axis_line=True,
        shade_pnl=True,
        num=1_000,
    )
