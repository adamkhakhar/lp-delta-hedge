import torch
import numpy as np


class AlgorithmicDataSet:
    def __init__(self, price_lower, price_upper, fun, num_samples):
        self.price_lower = price_lower
        self.price_upper = price_upper
        self.fun = fun
        self.num_samples = num_samples

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        x = np.random.uniform(low=self.price_lower, high=self.price_upper)
        return {
            "sample": torch.tensor(x, dtype=torch.float),
            "target": torch.tensor(self.fun(x), dtype=torch.float),
        }
