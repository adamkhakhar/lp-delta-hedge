import os
import sys
import torch

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
import delta_hedge.OptionsOptimizer as OptionsOptimizer
import delta_hedge.Train as Train
import delta_hedge.Derivative as Derivative
import delta_hedge.AlgorithmicDataSet as AlgorithmicDataSet

if __name__ == "__main__":

    NAME = "identity"
    LR = 1e-3
    TARGET_FUN = lambda x: 4 * x
    LOWER_BOUND = 0
    UPPER_BOUND = 10
    NUM_SAMPLES = 1_000_000
    BATCH_SIZE = 2_000
    TEST_BATCH_SIZE = 100

    derivs = [Derivative("i", lambda x: x, None)]
    model = OptionsOptimizer(derivs)

    train_loader = torch.utils.data.DataLoader(
        AlgorithmicDataSet(LOWER_BOUND, UPPER_BOUND, TARGET_FUN, NUM_SAMPLES),
        batch_size=BATCH_SIZE,
    )

    test_loader = torch.utils.data.DataLoader(
        AlgorithmicDataSet(LOWER_BOUND, UPPER_BOUND, TARGET_FUN, NUM_SAMPLES),
        batch_size=TEST_BATCH_SIZE,
    )

    optimizer = Train(NAME, model, train_loader, test_loader, LR, log_every=10)
    optimizer.train()
