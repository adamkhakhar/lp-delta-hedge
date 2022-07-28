import torch
import torch.nn as nn


class OptionsOptimizer(nn.module):
    def __init__(self, derivatives):
        self.derivatives = derivatives
        self.parameters = nn.Linear(len(derivatives), 1, bias=False)

    def forward(self, x):
        derivatives_payoff = [d.payoff_fun(x) for d in self.derivatives]
        derivatives_payoff_tensor = torch.FloatTensor(derivatives_payoff)
        out = self.parameters(derivatives_payoff)
        return out
