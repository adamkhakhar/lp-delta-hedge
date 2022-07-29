import time
import torch
import torch.nn as nn
import pickle
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Train:
    """
    Class used to implement training of parameters in optimization.

    ...
    Methods
    -------
    instantiate(start_time):
        Creates model, train loader, and optimizer
    calculate_loss(outputs, targets):
        Calculates loss of a minibatch
    iteration_update(i, features, outputs, targets, loss):
        Is called every minibatch. Used for logging.
    save_state(loss):
        Saves state of model
    train():
        Trains model using base_model_runner train method
    """

    def __init__(
        self,
        name,
        model,
        train_loader,
        test_loader,
        learning_rate,
        num_grad_steps,
        l1_lambda=0.01,
        log_every=100,
        device=None,
        print_every=False,
    ):
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.log_every = log_every
        self.device = (
            f"cuda:{device}"
            if torch.cuda.is_available() and device is not None
            else "cpu"
        )
        self.print_every = print_every
        self.model = model.to(self.device)
        self.optimizer = torch.optim.Adam([self.model.theta], lr=learning_rate)
        self.l1_lambda = l1_lambda
        self.num_grad_steps = num_grad_steps

        self.curr_loss = 0
        self.start_time = None
        self.name = name
        self.train_loss_lst = []
        self.time_lst = []
        self.soft_error_lst = []
        print(self.name, "starting to train...")

    def instantiate(self, start_time):
        """Creates model, train loader, and optimizer

        Parameters
        ----------
        start_time : float
            time that train method was started

        Returns
        -------
        tuple
            model, train_loader, optimizer
        """
        self.start_time = start_time
        return self.model, self.train_loader, self.optimizer

    def calculate_loss(self, outputs, targets):
        """Calculates loss of a minibatch

        Parameters
        ----------
        outputs : tensor
            prediction of model

        targets : tensor
            correct answer for model's predictions

        Returns
        -------
        tensor
            scalar loss
        """
        mse_loss = nn.MSELoss()(outputs, targets)
        l1_regularization = self.l1_lambda * (sum(self.model.theta.abs()))
        return mse_loss + l1_regularization

    def iteration_update(self, i, features, outputs, targets, loss):
        """Is called every minibatch. Used for logging.

        Parameters
        ----------
        i : int
            minibatch iteration

        features : tensor
            tensor of features

        outputs : tensor
            prediction of model

        targets : tensor
            correct answer for model's predictions

        loss : tensor
            current loss of model
        """
        with torch.no_grad():
            self.curr_loss += loss.item()
            # save data and print metrics every few iterations
            if i % self.log_every == 0 and i != 0:
                scaled_curr_loss = self.curr_loss / self.log_every
                self.train_loss_lst.append(scaled_curr_loss)
                self.time_lst.append(time.time() - self.start_time)
                total_soft_error = 0

                data = next(iter(self.test_loader))
                targets = data["target"]
                outputs = self.model(data["sample"])
                for j in range(targets.shape[0]):
                    pred = outputs[j]
                    target = targets[j]
                    soft_error = (pred - target) ** 2

                    total_soft_error += soft_error

                total_soft_error /= targets.shape[0]
                self.soft_error_lst.append(total_soft_error)
                iteration_update_data = {
                    "train_loss": self.train_loss_lst,
                    "time": self.time_lst,
                    "soft_error": self.soft_error_lst,
                }
                print(
                    f"[{i} / {self.num_grad_steps}] Train Loss: {scaled_curr_loss} | Time {int(time.time() - self.start_time)}",
                    flush=True,
                )
                self.curr_loss = 0

    def store_data(self, fname, data):
        with open(fname, "wb") as f:
            pickle.dump(data, f)

    def save_state(self, loss):
        """Saves state of model

        Parameters
        ----------
        loss : scalar tensor
            current loss of model
        """
        experiment_data = {
            "loss": loss,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
        }
        self.store_data(
            f"{ROOT_DIR}/results/{self.name}_save_state.bin", experiment_data
        )

    def train(self):
        """
        Trains model using base_model_runner train method
        """
        start_time = time.time()
        model, train_loader, optimizer = self.instantiate(start_time)
        for i, data in enumerate(train_loader, 0):
            if self.print_every:
                print(i, int(time.time() - start_time))
            features = data["sample"].to(self.device)
            targets = data["target"].to(self.device)
            optimizer.zero_grad()
            outputs = model(features)
            loss = self.calculate_loss(outputs, targets)
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                self.iteration_update(i, features, outputs, targets, loss)
        self.save_state(loss)
