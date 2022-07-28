import os
import sys
import torch

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
from delta_hedge.OptionsOptimizer import OptionsOptimizer as OptionsOptimizer
from delta_hedge.Train import Train as Train
from delta_hedge.Derivative import Derivative as Derivative
from delta_hedge.AlgorithmicDataSet import AlgorithmicDataSet as AlgorithmicDataSet

if __name__ == "__main__":
    NAME = "identity"
    LR = 1e-1
    TARGET_FUN = lambda x: 4 * x + 7 * x**2
    LOWER_BOUND = 0
    UPPER_BOUND = 10
    NUM_SAMPLES = 10_000_000
    BATCH_SIZE = 2_000
    TEST_BATCH_SIZE = 100

    derivs = [
        Derivative("i", lambda x: x, None),
        Derivative("sqare", lambda x: x**2, None),
    ]
    model = OptionsOptimizer(derivs)

    train_loader = torch.utils.data.DataLoader(
        AlgorithmicDataSet(LOWER_BOUND, UPPER_BOUND, TARGET_FUN, NUM_SAMPLES),
        batch_size=BATCH_SIZE,
    )

    test_loader = torch.utils.data.DataLoader(
        AlgorithmicDataSet(LOWER_BOUND, UPPER_BOUND, TARGET_FUN, NUM_SAMPLES),
        batch_size=TEST_BATCH_SIZE,
    )

    optimizer = Train(
        NAME,
        model,
        train_loader,
        test_loader,
        LR,
        NUM_SAMPLES // BATCH_SIZE,
        log_every=100,
    )
    optimizer.train()

    # print results
    thetas = model.theta.tolist()
    for i in range(len(derivs)):
        print(f"Derivative : {derivs[i].name} | Qty : {thetas[i]}")
