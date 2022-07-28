import torch
import torch.nn as nn


class OptionsOptimizer(nn.Module):
    def __init__(self, derivatives):
        super(OptionsOptimizer, self).__init__()
        self.derivatives = derivatives
        self.theta = torch.rand(len(derivatives), requires_grad=True)

    def forward(self, x):
        derivatives_payoff = [
            [d.payoff_fun(sample) for d in self.derivatives] for sample in x
        ]
        derivatives_payoff_tensor = torch.tensor(derivatives_payoff)
        out = torch.sum(self.theta * derivatives_payoff_tensor, dim=1)
        return out
