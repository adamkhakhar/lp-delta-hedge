class Derivative:
    def __init__(self, name, payoff_fun, bid, ask, info):
        self.name = name
        self.payoff_fun = payoff_fun
        self.deribit_info = info
        self.bid = bid
        self.ask = ask
