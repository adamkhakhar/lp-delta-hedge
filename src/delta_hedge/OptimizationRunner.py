import os
import sys
import torch

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
    def __init__(self, name, data_params, deriv_params, train_params):
        keys_in_data_params = [
            "final_price_lower_bound",
            "final_price_upper_bound",
            "target_function",
        ]
        for key in keys_in_data_params:
            assert key in data_params
        keys_in_deriv_params = ["asset", "expired"]
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
        self.derivs = retrieve_and_create_derivatives(
            deriv_params["asset"], expired=deriv_params["expired"]
        )
        self.model = OptionsOptimizer(self.derivs)
        self.train_loader = torch.utils.data.DataLoader(
            AlgorithmicDataSet(
                data_params["final_price_lower_bound"],
                data_params["final_price_upper_bound"],
                data_params["target_function"],
                train_params["num_samples"],
            ),
            batch_size=train_params["batch_sze"],
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
            train_params["num_samples"] // train_params["batch_sze"],
            log_every=train_params["log_every"],
        )
        self.learned_theta = None

    def train(self):
        self.optimizer.train()
        self.learned_theta = self.model.theta.tolist()

    def pretty_print_results(self):
        for i in range(len(self.derivs)):
            print(f"Derivative : {self.derivs[i].name} | Qty : {self.learned_theta[i]}")

    def present_pnl(self, title):
        # display options portfolio PNL as a function of price
        create_plot_from_fn(
            self.get_pnl_fun(),
            self.data_params["final_price_lower_bound"],
            self.data_params["final_price_upper_bound"],
            y_min=None,
            y_max=None,
            save_title=self.name,
            xlabel=f"{self.deriv_params['asset']} Price",
            ylabel="Options Portfolio Payoff",
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
