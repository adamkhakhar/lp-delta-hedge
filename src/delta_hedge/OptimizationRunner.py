import os
import sys
import torch
import time
import pickle
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(BASE_DIR)
from delta_hedge.OptionsOptimizer import OptionsOptimizer as OptionsOptimizer
from delta_hedge.Train import Train as Train
from delta_hedge.Derivative import Derivative as Derivative
from delta_hedge.AlgorithmicDataSet import AlgorithmicDataSet as AlgorithmicDataSet
from deribit.retrieve_instruments import retrieve_and_create_derivatives

ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)
from utils.image_creation import create_plot_from_fn


class OptimizationRunner:
    def __init__(self, name, target_fun, data_params, deriv_params, train_params):
        self.target_fun = target_fun
        keys_in_data_params = [
            "final_price_lower_bound",
            "final_price_upper_bound",
            "target_function",
        ]
        for key in keys_in_data_params:
            assert key in data_params
        keys_in_deriv_params = ["asset", "initial_asset_price", "long_only"]
        for key in keys_in_deriv_params:
            assert key in deriv_params
        keys_in_train_params = [
            "learning_rate",
            "num_samples",
            "batch_size",
            "test_batch_size",
            "log_every",
        ]
        for key in keys_in_train_params:
            assert key in train_params

        self.name = name
        start_time = time.time()
        self.derivs = retrieve_and_create_derivatives(
            deriv_params["asset"],
            deriv_params["initial_asset_price"],
            deriv_params["long_only"],
        )
        print(
            f"Derivatives fetched ({int(time.time() - start_time)} sec)...", flush=True
        )
        self.model = OptionsOptimizer(self.derivs)
        self.data_params = data_params
        self.train_loader = torch.utils.data.DataLoader(
            AlgorithmicDataSet(
                data_params["final_price_lower_bound"],
                data_params["final_price_upper_bound"],
                data_params["target_function"],
                train_params["num_samples"],
            ),
            batch_size=train_params["batch_size"],
        )
        self.test_loader = torch.utils.data.DataLoader(
            AlgorithmicDataSet(
                data_params["final_price_lower_bound"],
                data_params["final_price_upper_bound"],
                data_params["target_function"],
                train_params["num_samples"],
            ),
            batch_size=train_params["test_batch_size"],
        )
        self.optimizer = Train(
            self.name,
            self.model,
            self.train_loader,
            self.test_loader,
            train_params["learning_rate"],
            train_params["num_samples"] // train_params["batch_size"],
            log_every=train_params["log_every"],
        )
        self.learned_theta = None

    def train(self):
        self.optimizer.train()
        self.learned_theta = self.model.theta.tolist()

    def pretty_print_results(self):
        for i in range(len(self.derivs)):
            print(f"Derivative : {self.derivs[i].name} | Qty : {self.learned_theta[i]}")

    def present_lppnl(self, title, y_min=None, y_max=None):
        lppnl_fun = lambda x: -1 * self.data_params["target_function"](x)
        create_plot_from_fn(
            lambda x: lppnl_fun(x) / 1000,
            self.data_params["final_price_lower_bound"],
            self.data_params["final_price_upper_bound"],
            y_min=y_min,
            y_max=y_max,
            save_title=self.name + "_lppnl_plot",
            xlabel=r"$p_{a;b}^f$",
            ylabel="PNL ($ Thousands)",
            title=title,
            x_axis_line=True,
            shade_pnl=True,
            num=1_000,
        )

    def present_pnl(self, title):
        # display options portfolio PNL as a function of price
        pnl_fun = self.get_pnl_fun()
        create_plot_from_fn(
            lambda x: pnl_fun(x) / 1000,
            self.data_params["final_price_lower_bound"],
            self.data_params["final_price_upper_bound"],
            y_min=None,
            y_max=None,
            save_title=self.name + "_options_pnl_plot",
            xlabel=r"$p_{a;b}^f$",
            ylabel="PNL ($ Thousands)",
            title=title,
            x_axis_line=True,
            shade_pnl=True,
            num=1_000,
        )

    def get_pnl_fun(self):
        return lambda x: sum(
            [
                self.learned_theta[i] * (self.derivs[i].payoff_fun(x))
                for i in range(len(self.derivs))
            ]
        )

    def get_combined_pnl_fun(self):
        return (
            lambda x: (-1 * self.target_fun(x) + self.get_pnl_fun()(x))
            / self.data_params["portfolio_initial_value"]
            * 100
        )

    def present_strategy_pnl(self, title):
        create_plot_from_fn(
            self.get_combined_pnl_fun(),
            self.data_params["final_price_lower_bound"],
            self.data_params["final_price_upper_bound"],
            y_min=None,
            y_max=None,
            save_title=self.name + "_combined_pnl_plot",
            xlabel=r"$p_{a;b}^f$",
            ylabel="PNL (%)",
            title=title,
            x_axis_line=True,
            shade_pnl=True,
            num=1_000,
        )

    def _store_data(self, fname, data):
        with open(fname, "wb") as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def save_state(self):
        fname = f"{ROOT_DIR}/results/{self.name}_model_save_state.bin"
        torch.save(self.model.state_dict(), fname)
        deriv_list = []
        for d in self.derivs:
            deriv_list.append(
                {
                    "name": d.name,
                    "deribit_info": d.deribit_info,
                    "bid": d.bid,
                    "ask": d.ask,
                }
            )
        combined_pnl = self.get_combined_pnl_fun()
        deriv_list.append(
            {
                "combined_pnl": [
                    combined_pnl(x)
                    for x in np.linspace(
                        self.data_params["final_price_lower_bound"],
                        self.data_params["final_price_upper_bound"],
                        1_000,
                    )
                ]
            }
        )
        pnl_fun = self.get_pnl_fun()
        deriv_list.append(
            {
                "pnl_fun": [
                    pnl_fun(x)
                    for x in np.linspace(
                        self.data_params["final_price_lower_bound"],
                        self.data_params["final_price_upper_bound"],
                        1_000,
                    )
                ]
            }
        )
        fname = f"{ROOT_DIR}/results/{self.name}_deriv_save_state.json"
        with open(fname, "w") as f:
            f.write(json.dumps(deriv_list))
