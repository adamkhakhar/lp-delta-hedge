import os
import sys
import json


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(BASE_DIR)
from delta_hedge.OptimizationRunner import OptimizationRunner as OptimizationRunner

ROOT_DIR = os.path.dirname(BASE_DIR)

if __name__ == "__main__":
    path_to_config = ROOT_DIR + "/configs/concentrated_liquidity_config.json"
    with open(path_to_config) as f:
        config = json.load(f)

    def final_value_pool_assets(final_price):
        notional = None
        if config["initial_asset_price"] < config["lp_lower_bound"]:
            notional = config["initial_asset_a_amt"]
        elif (
            config["initial_asset_price"] > config["lp_lower_bound"]
            and config["initial_asset_price"] < config["lp_upper_bound"]
        ):
            notional = (
                config["initial_asset_a_amt"]
                * (config["initial_asset_price"] / config["lp_lower_bound"]) ** 0.5
                * (
                    (config["lp_upper_bound"]) ** 0.5
                    - (config["lp_lower_bound"]) ** 0.5
                )
                / (
                    (config["lp_upper_bound"]) ** 0.5
                    - (config["initial_asset_price"]) ** 0.5
                )
            )
        else:
            notional = config["initial_asset_b_amt"] / (
                (config["lp_lower_bound"] * config["lp_upper_bound"]) ** 0.5
            )
        final_amount_a = None
        final_amount_b = None
        if final_price < config["lp_lower_bound"]:
            final_amount_a = notional
            final_amount_b = 0
        elif (
            final_price > config["lp_lower_bound"]
            and final_price < config["lp_upper_bound"]
        ):
            final_amount_a = (
                notional
                * (config["lp_lower_bound"] / final_price) ** 0.5
                * ((config["lp_upper_bound"]) ** 0.5 - (final_price) ** 0.5)
                / (
                    (config["lp_upper_bound"]) ** 0.5
                    - (config["lp_lower_bound"]) ** 0.5
                )
            )
            final_amount_b = (
                notional
                * ((config["lp_lower_bound"] * config["lp_upper_bound"]) ** 0.5)
                * (((final_price) ** 0.5) - ((config["lp_lower_bound"]) ** 0.5))
                / (
                    (config["lp_upper_bound"]) ** 0.5
                    - (config["lp_lower_bound"]) ** 0.5
                )
            )
        else:
            final_amount_a = 0
            final_amount_b = (
                notional * (config["lp_lower_bound"] * config["lp_upper_bound"]) ** 0.5
            )
        return final_amount_a * final_price + final_amount_b

    TARGET_FUN = lambda x: (
        final_value_pool_assets(-1 * x) / config["portfolio_initial_value"] - 1
    ) * (
        config["initial_asset_a_amt"] * config["initial_asset_price"]
        + config["initial_asset_b_amt"]
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
    runner.present_lppnl("WBTC-USDC Liquidity Position LPPNL", y_max=500_000)
    runner.train()
    print("Finished training...")
    runner.save_state()
    runner.pretty_print_results()
    runner.present_pnl("Options Portfolio Payoff - ETH USD - Concentrated Liquidity")
    runner.present_strategy_pnl(
        "ETH-USDC Delta-Hedged Liquidity Position PNL - Uniswap v3"
    )
