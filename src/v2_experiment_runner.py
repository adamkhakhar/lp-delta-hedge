import os
import sys
import json


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(BASE_DIR)
from delta_hedge.OptimizationRunner import OptimizationRunner as OptimizationRunner

ROOT_DIR = os.path.dirname(BASE_DIR)

if __name__ == "__main__":
    TARGET_FUN = lambda x: x
    with open(ROOT_DIR + "/configs/config.json") as f:
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
