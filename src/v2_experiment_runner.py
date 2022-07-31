import os
import sys
import json


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(BASE_DIR)
from delta_hedge.OptimizationRunner import OptimizationRunner as OptimizationRunner

ROOT_DIR = os.path.dirname(BASE_DIR)

if __name__ == "__main__":
    path_to_config = ROOT_DIR + "/configs/uniform_liquidity_config.json"
    with open(path_to_config) as f:
        config = json.load(f)
    TARGET_FUN = (
        lambda x: -1
        * config["portfolio_initial_value"]
        * (((x / config["initial_asset_price"]) ** 0.5) - 1)
    )
    data_params = {
        "final_price_lower_bound": config["final_price_lower_bound"],
        "final_price_upper_bound": config["final_price_upper_bound"],
        "target_function": TARGET_FUN,
        "portfolio_initial_value": config["portfolio_initial_value"],
    }
    deriv_params = {
        "asset": config["asset"],
        "initial_asset_price": config["initial_asset_price"],
        "long_only": config["long_only"],
    }
    train_params = {
        "learning_rate": config["learning_rate"],
        "num_samples": config["num_samples"],
        "batch_size": config["batch_size"],
        "test_batch_size": config["batch_size"],
        "log_every": config["log_every"],
    }
    runner = OptimizationRunner(
        config["name"], TARGET_FUN, data_params, deriv_params, train_params
    )
    runner.train()
    print("Finished training...")
    runner.save_state()
    runner.pretty_print_results()
    runner.present_pnl("Options Portfolio Payoff - ETH USD - Uniform Liquidity")
    runner.present_strategy_pnl(
        "ETH-USDT Delta-Hedged Liquidity Position PNL - Uniswap v2"
    )
