import os
import sys
import requests

LP_DELTA_HEDGE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
sys.path.append(LP_DELTA_HEDGE_PATH + "/src")

from delta_hedge.Derivative import Derivative


def retrieve_instruments(currency, expired=False):
    assert currency in ["ETH", "SOL", "BTC"]
    expired = "true" if expired else "false"
    instruments = requests.get(
        f"https://deribit.com/api/v2/public/get_book_summary_by_currency?currency={currency}&kind=option"
    ).json()["result"]
    return instruments


def create_derivatives_for_instrument(instrument_data, initial_asset_price):
    name = instrument_data["instrument_name"]
    if (
        not (name.endswith("C") or name.endswith("P"))
        or (instrument_data["bid_price"] is None)
        or (instrument_data["ask_price"] is None)
    ):
        return None, None
    strike = int(name.split("-")[-2])
    best_bid = instrument_data["bid_price"] * initial_asset_price
    best_ask = instrument_data["ask_price"] * initial_asset_price
    info = {"instrument_data": instrument_data}
    long_payoff_fun = None
    short_payoff_fun = None
    # call
    if name.endswith("C"):
        # long
        long_payoff_fun = lambda x: max(0, x - strike) - best_ask
        # short
        short_payoff_fun = lambda x: best_bid - max(0, x - strike)
    else:  # put
        # long
        long_payoff_fun = lambda x: max(0, strike - x) - best_ask
        # short
        short_payoff_fun = lambda x: best_bid - max(0, strike - x)
    long_deriv = Derivative(name + "_LONG", long_payoff_fun, best_bid, best_ask, info)
    short_deriv = Derivative(
        name + "_SHORT", short_payoff_fun, best_bid, best_ask, info
    )
    return long_deriv, short_deriv


def create_derivatives_from_instrument_data(data, initial_asset_price, long_only):
    assert type(data) == list
    derivatives = []
    for instrument in data:
        long_deriv, short_deriv = create_derivatives_for_instrument(
            instrument, initial_asset_price
        )
        if long_deriv is None or short_deriv is None:
            continue
        derivatives.append(long_deriv)
        if not long_only:
            derivatives.append(short_deriv)
    return derivatives


def retrieve_and_create_derivatives(currency, initial_asset_price, long_only):
    instruments = retrieve_instruments(currency)
    derivs = create_derivatives_from_instrument_data(
        instruments, initial_asset_price, long_only
    )
    return derivs
